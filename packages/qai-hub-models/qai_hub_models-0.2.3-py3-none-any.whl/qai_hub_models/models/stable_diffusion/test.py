import numpy as np
import pytest
from diffusers import StableDiffusionPipeline

from qai_hub_models.models.stable_diffusion.app import StableDiffusionApp
from qai_hub_models.models.stable_diffusion.demo import DEFAULT_DEMO_PROMPT
from qai_hub_models.models.stable_diffusion.demo import main as demo_main
from qai_hub_models.models.stable_diffusion.model import (
    DEFAULT_VERSION,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    SDTextEncoder,
    SDUNet,
    SDVAEDecoder,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.testing import skip_clone_repo_check

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID,
    MODEL_ASSET_VERSION,
    "CompVis-v1-4/a-high-quality-photo-of-a-surfing-dog-pytorch-seed42-steps2.png",
)


@pytest.mark.skip(reason="Uses a large amount of memory and is often killed by OOM.")
@skip_clone_repo_check
def test_e2e_numerical():
    """
    Verify our PyTorch driver produces the correct image.
    """
    # Not sufficient for a sensible image, but enough for a test.
    num_steps = 2
    seed = 42

    pipe = StableDiffusionPipeline.from_pretrained(DEFAULT_VERSION, use_auth_token=True)

    # Construct all the networks
    text_encoder = SDTextEncoder(pipe).eval()
    vae_decoder = SDVAEDecoder(pipe).eval()
    unet = SDUNet(pipe).eval()

    # Save the tokenizer and scheduler
    tokenizer = pipe.tokenizer
    scheduler = pipe.scheduler

    app = StableDiffusionApp(
        text_encoder=text_encoder,
        vae_decoder=vae_decoder,
        unet=unet,
        tokenizer=tokenizer,
        scheduler=scheduler,
    )

    ref_image_pil = load_image(IMAGE_ADDRESS)
    ref_image_np = np.array(ref_image_pil).astype(np.float32) / 255.0

    image = app.generate_image(DEFAULT_DEMO_PROMPT, num_steps=num_steps, seed=seed)

    np.allclose(image.detach().numpy(), ref_image_np)


@pytest.mark.skip(reason="Uses a large amount of memory and is often killed by OOM.")
@skip_clone_repo_check
def test_demo():
    demo_main(is_test=True)
