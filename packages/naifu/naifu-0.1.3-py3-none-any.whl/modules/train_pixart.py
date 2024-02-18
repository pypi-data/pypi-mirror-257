import torch
import os
import lightning as pl

from omegaconf import OmegaConf
from PIL import Image
from safetensors.torch import save_file
from transformers import T5EncoderModel, T5Tokenizer
from diffusers import AutoencoderKL, DPMSolverMultistepScheduler
from lightning.pytorch.utilities.model_summary import ModelSummary

from common.utils import load_torch_file, rank_zero_print, get_class
from common.dataset import AspectRatioDataset, worker_init_fn

from models.pixart.dit import DiT_XL_2, get_model_kwargs
from models.pixart.diffusion import SpacedDiffusion, get_named_beta_schedule, space_timesteps
from models.pixart.diffusion import ModelVarType, ModelMeanType, LossType


def setup(fabric: pl.Fabric, config: OmegaConf) -> tuple:
    model_path = config.trainer.model_path
    model = DiffusionModel(
        model_path=model_path, 
        config=config, 
        device=fabric.device
    )
    dataset = AspectRatioDataset(
        batch_size=config.trainer.batch_size,
        rank=fabric.global_rank,
        dtype=torch.float32,
        base_len=config.trainer.resolution,
        **config.dataset,
    )
    dataloader = torch.utils.data.DataLoader(
        dataset,
        sampler=None,
        batch_size=None,
        persistent_workers=False,
        num_workers=config.dataset.get("num_workers", 4),
        worker_init_fn=worker_init_fn,
        shuffle=False,
        pin_memory=True,
    )
    
    params_to_optim = [{'params': model.model.parameters()}]
    optim_param = config.optimizer.params
    optimizer = get_class(config.optimizer.name)(
        params_to_optim, **optim_param
    )
    scheduler = None
    if config.get("scheduler"):
        scheduler = get_class(config.scheduler.name)(
            optimizer, **config.scheduler.params
        )
        
    if fabric.is_global_zero and os.name != "nt":
        print(f"\n{ModelSummary(model, max_depth=1)}\n")
        
    model, optimizer = fabric.setup(model, optimizer)
    dataloader = fabric.setup_dataloaders(dataloader)
    return model, dataset, dataloader, optimizer, scheduler


class DiffusionModel(pl.LightningModule):
    def __init__(self, model_path, config, device):
        super().__init__()
        self.config = config
        self.model_path = model_path
        self.target_device = device
        self.init_model()

    def init_model(self):
        t5_model_path = self.config.trainer.get("t5_model_path", "PixArt-alpha/PixArt-XL-2-1024-MS")
        vae_model_path = self.config.trainer.get("vae_model_path", "stabilityai/sd-vae-ft-mse")
        self.tokenizer = T5Tokenizer.from_pretrained(
           t5_model_path, 
           legacy=False, 
           subfolder="tokenizer"
        )
        self.text_encoder = T5EncoderModel.from_pretrained(
            t5_model_path, 
            torch_dtype=torch.bfloat16,
            use_safetensors=True, 
            subfolder="text_encoder"
        )
        self.vae = AutoencoderKL.from_pretrained(vae_model_path)
        self.text_encoder.requires_grad_(False)
        self.vae.requires_grad_(False)
        
        dit_state_dict = load_torch_file(self.model_path)
        betas = get_named_beta_schedule(
            schedule_name="linear", 
            num_diffusion_timesteps=1000
        )
        timesteps = space_timesteps(
            num_timesteps=1000,
            section_counts=[1000]
        )
        self.diffusion = SpacedDiffusion(
            use_timesteps=timesteps,
            betas=betas,
            model_mean_type=ModelMeanType.EPSILON,
            model_var_type=ModelVarType.LEARNED_RANGE,
            loss_type=LossType.MSE,
            snr=False,
            return_startx=False,
            # rescale_timesteps=rescale_timesteps,
        )
        
        base = self.config.trainer.resolution
        self.model = DiT_XL_2(input_size=base//8, interpolation_scale=base//512)
        self.model.to(memory_format=torch.channels_last).train()
    
        rank_zero_print("Loading weights from checkpoint: DiT-XL-2-1024-MS.pth")
        result = self.model.load_state_dict(dit_state_dict, strict=False)
        assert result.unexpected_keys == ['pos_embed'], f"Unexpected keys: {result.unexpected_keys}, Missing keys: {result.missing_keys}"

    @torch.no_grad()
    def encode_tokens(self, prompts):
        with torch.autocast("cuda", enabled=False):
            text_encoder = self.text_encoder
            text_inputs = self.tokenizer(
                prompts,
                padding="max_length",
                max_length=120,
                truncation=True,
                add_special_tokens=True,
                return_tensors="pt",
            )
            text_input_ids = text_inputs.input_ids.to(text_encoder.device)
            prompt_attention_mask = text_inputs.attention_mask.to(text_encoder.device)

            prompt_embeds = text_encoder(
                text_input_ids, attention_mask=prompt_attention_mask
            )[0]
            return prompt_embeds, prompt_attention_mask

    def forward(self, batch):

        prompts = batch["prompts"]
        prompt_embeds, prompt_attention_mask = self.encode_tokens(prompts)
        
        if not batch["is_latent"]:
            self.vae.to(self.target_device)
            latent_dist = self.vae.encode(batch["pixels"]).latent_dist
            latents = latent_dist.sample() * self.vae.config.scaling_factor
            if torch.any(torch.isnan(latents)):
                rank_zero_print("NaN found in latents, replacing with zeros")
                latents = torch.where(torch.isnan(latents), torch.zeros_like(latents), latents)
        else:
            self.vae.cpu()
            latents = batch["pixels"]
            
        model_dtype = next(self.model.parameters()).dtype
        bsz = latents.shape[0]
        
        # Forward pass through the model
        timesteps = torch.randint(0, 1000, (bsz,), device=latents.device).long()
        latents = latents.to(model_dtype)
        model_kwg = get_model_kwargs(latents, self.model)
        loss = self.diffusion.training_losses(
            self.model, latents, timesteps, 
            model_kwargs=dict(
                y=prompt_embeds.to(self.target_device, dtype=model_dtype), 
                encoder_mask=prompt_attention_mask.to(self.target_device, dtype=model_dtype),
                **model_kwg,
            )
        )['loss'].mean()
        
        if torch.isnan(loss).any() or torch.isinf(loss).any():
            raise FloatingPointError("Error infinite or NaN loss detected")
        
        return loss

    @torch.no_grad()
    def sample(
        self, 
        prompt="1girl, solo", 
        negative_prompt="lowres, low quality, text, error, extra digit, cropped",
        size=(1152, 832),
        steps = 28,
        guidance_scale=6.5,
    ):
        self.model.eval()
        
        prompt = prompt.replace("_", " ").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "").lower()
        scheduler = DPMSolverMultistepScheduler()
        prompt_embeds, prompt_attention_mask = self.encode_tokens(
            [negative_prompt, prompt]
        )

        latents = torch.randn(1, 4, size[0] // 8, size[1] // 8, device=self.target_device)
        scheduler.set_timesteps(steps)
        timesteps = scheduler.timesteps
        latents = latents * scheduler.init_noise_sigma
        
        for i, t in enumerate(timesteps):
            # expand the latents if we are doing classifier free guidance
            latent_model_input = torch.cat([latents] * 2)
            latent_model_input = scheduler.scale_model_input(latent_model_input, t)

            noise_pred = self.model(
                x=latent_model_input, 
                t=torch.stack([t] * latents.shape[0]).to(latents.device),
                y=prompt_embeds.to(latents.device, dtype=latents.dtype), 
                encoder_mask=prompt_attention_mask.to(latents.device, dtype=latents.dtype),
                **get_model_kwargs(latents, self.model),
            )
            noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)  # uncond by negative prompt
            noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

            # compute the previous noisy sample x_t -> x_t-1
            noise_pred = noise_pred.chunk(2, dim=1)[0]
            latents = scheduler.step(noise_pred, t, latents, return_dict=False)[0]

        decoded = self.vae.decode(latents / self.vae.config.scaling_factor).sample
        image = torch.clamp((decoded + 1.0) / 2.0, min=0.0, max=1.0).detach().float()
        image = image.cpu().permute(0, 2, 3, 1).float().numpy()
        
        image = (image * 255).round().astype("uint8")
        image = [Image.fromarray(im) for im in image]
        
        self.model.train()
        return image
    
    def save_checkpoint(self, model_path):
        cfg = self.config.trainer
        string_cfg = OmegaConf.to_yaml(self.config)
        if cfg.get("save_format") == "safetensors":

            model_path += ".safetensors"
            state_dict = self.model.state_dict()
            # check if any keys startswith modules. if so, remove the modules. prefix
            if any([key.startswith("module.") for key in state_dict.keys()]):
                state_dict = {
                    key.replace("module.", ""): value
                    for key, value in state_dict.items()
                }
            save_file(state_dict, model_path, metadata={"trainer_config": string_cfg})
        else:
            model_path += ".ckpt"
            torch.save(
                model_path,
                {"state_dict": self.model.state_dict(), "trainer_config": string_cfg},
            )
        rank_zero_print(f"Saved model to {model_path}")