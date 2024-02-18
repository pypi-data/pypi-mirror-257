from setuptools import setup, find_packages

setup(
    name='naifu',
    version='0.1.3',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    py_modules=['trainer'],
    description='naifu is designed for training generative models with various configurations and features.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=open('requirements.txt').read().splitlines(),
    url='https://github.com/mikubill/naifu-diffusion',
    entry_points={
        'console_scripts': [
            'naifu = trainer:main',
        ],
    },
    author='Mikubill',
    author_email='31246794+Mikubill@users.noreply.github.com'
)