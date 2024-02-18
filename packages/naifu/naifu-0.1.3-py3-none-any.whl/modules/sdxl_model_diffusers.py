import torch
import torch.utils.checkpoint
import lightning as pl

from pathlib import Path
from common.utils import rank_zero_print
from diffusers import StableDiffusionXLPipeline
from diffusers import EulerDiscreteScheduler, DDPMScheduler
from lightning.pytorch.utilities import rank_zero_only
from modules.sdxl_utils import get_hidden_states_sdxl

# define the LightningModule
class StableDiffusionModel(pl.LightningModule):
    def __init__(self, model_path, config, device):
        super().__init__()
        self.config = config
        self.model_path = model_path
        self.target_device = device
        self.init_model()

    def init_model(self):
        trainer_cfg = self.config.trainer
        config = self.config
        advanced = config.get("advanced", {})
        
        rank_zero_print(f"Loading model from {self.model_path}")
        p = StableDiffusionXLPipeline
        if Path(self.model_path).is_dir():
            self.pipeline = pipeline = p.from_pretrained(self.model_path)
        else:
            self.pipeline = pipeline = p.from_single_file(self.model_path)
            
        self.vae, self.unet = pipeline.vae, pipeline.unet
        self.text_encoder_1, self.text_encoder_2, self.tokenizer_1, self.tokenizer_2 = (
            pipeline.text_encoder,
            pipeline.text_encoder_2,
            pipeline.tokenizer,
            pipeline.tokenizer_2,
        )
        self.max_prompt_length = 225 + 2
        self.vae.requires_grad_(False)
        self.text_encoder_1.requires_grad_(False)
        self.text_encoder_2.requires_grad_(False)
        self.scale_factor = 0.13025

        self.unet.enable_gradient_checkpointing()
        if trainer_cfg.use_xformers:
            self.unet.enable_xformers_memory_efficient_attention()

        if advanced.get("train_text_encoder_1"):
            self.text_encoder_1.requires_grad_(True)
            self.text_encoder_1.gradient_checkpointing_enable()

        if advanced.get("train_text_encoder_2"):
            self.text_encoder_2.requires_grad_(True)
            self.text_encoder_2.gradient_checkpointing_enable()

        self.noise_scheduler = DDPMScheduler(
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            num_train_timesteps=1000,
            clip_sample=False,
        )
        self.batch_size = self.config.trainer.batch_size
        self.vae_encode_bsz = self.config.get("vae_encode_batch_size", self.batch_size)
        if self.vae_encode_bsz < 0:
            self.vae_encode_bsz = self.batch_size
            
    def encode_pixels(self, inputs):
        feed_pixel_values = inputs
        latents = []
        for i in range(0, feed_pixel_values.shape[0], self.vae_encode_bsz):
            with torch.autocast("cuda", enabled=False):
                lat = self.vae.encode(feed_pixel_values[i : i + self.vae_encode_bsz]).latent_dist.sample()
            latents.append(lat)
        latents = torch.cat(latents, dim=0)
        latents = latents * self.vae.config.scaling_factor
        return latents
        
    def encode_prompt(self, batch):
        prompt = batch["prompts"]
        hidden_states1, hidden_states2, pool2 = get_hidden_states_sdxl(
            prompt,
            self.max_prompt_length,
            self.tokenizer_1,
            self.tokenizer_2,
            self.text_encoder_1,
            self.text_encoder_2,
        )
        text_embedding = torch.cat([hidden_states1, hidden_states2], dim=2)
        return text_embedding, pool2
    
    def compute_time_ids(self, original_size, crops_coords_top_left, target_size):
        # Adapted from pipeline.StableDiffusionXLPipeline._get_add_time_ids
        add_time_ids = torch.cat([original_size, crops_coords_top_left, target_size])
        add_time_ids = add_time_ids.to(self.target_device)
        return add_time_ids

    @torch.inference_mode()
    @rank_zero_only
    def sample(
        self,
        prompt,
        negative_prompt="lowres, low quality, text, error, extra digit, cropped",
        generator=None,
        size=(1024, 1024),
        steps=20,
        guidance_scale=6.5,
    ):
        self.vae.to(self.target_device)
        scheduler = EulerDiscreteScheduler(
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            num_train_timesteps=1000,
        )
        pipeline = StableDiffusionXLPipeline(
            unet=self.unet,
            vae=self.vae,
            text_encoder=self.text_encoder_1,
            text_encoder_2=self.text_encoder_2,
            noise_scheduler=scheduler,
        )
        image = pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=size[0],
            height=size[1],
            steps=steps,
            generator=generator,
            guidance_scale=guidance_scale,
            return_dict=False,
        )[0]
        return image

    def save_checkpoint(self, model_path):
        self.pipeline.save_pretrained(model_path)
        rank_zero_print(f"Saved model to {model_path}")

    def forward(self, batch):
        raise NotImplementedError
