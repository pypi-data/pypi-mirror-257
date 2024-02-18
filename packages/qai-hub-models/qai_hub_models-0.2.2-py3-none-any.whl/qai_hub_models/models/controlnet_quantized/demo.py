import argparse

import numpy as np
import qai_hub as hub
from diffusers import DPMSolverMultistepScheduler, UNet2DConditionModel
from PIL import Image
from transformers import CLIPTokenizer

from qai_hub_models.models.controlnet_quantized.app import ControlNetApp
from qai_hub_models.models.controlnet_quantized.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    ClipVITTextEncoder,
    ControlNet,
    Unet,
    VAEDecoder,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.base_model import BasePrecompiledModel
from qai_hub_models.utils.inference import HubModel
from qai_hub_models.utils.qai_hub_helpers import can_access_qualcomm_ai_hub

INPUT_IMAGE = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/test_bird_image.png"
).fetch()

DEFAULT_DEMO_PROMPT = "Big colorful bird in high resolution, 4K"
DEFAULT_DEVICE_NAME = "Samsung Galaxy S23 Ultra"


def _get_hub_model(input_model: BasePrecompiledModel, device_name=DEFAULT_DEVICE_NAME):
    if not can_access_qualcomm_ai_hub():
        raise RuntimeError(
            "ControlNet on-device demo requires access to QAI-Hub.\n"
            "Please visit https://qaihub.qualcomm.com/ and sign-up."
        )

    # Upload model
    uploaded_model = hub.upload_model(input_model.get_target_model_path())
    inputs = list(input_model.get_input_spec().keys())
    return HubModel(uploaded_model, inputs, hub.Device(name=device_name))


# Run ControlNet end-to-end on a given prompt and input image.
# The demo will output an AI-generated image based on the given inputs.
def main(is_test: bool = False):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        type=str,
        default=DEFAULT_DEMO_PROMPT,
        help="Prompt to generate image from.",
    )
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE,
        help="Input image to extract edges from.",
    )
    parser.add_argument(
        "--num_steps",
        type=int,
        default=5,
        help="The number of diffusion iteration steps (higher means better quality).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Path to output file. By default show it interactively.",
    )
    parser.add_argument(
        "--guidance_scale",
        type=float,
        default=7.5,
        help="Strength of guidance (higher means more influence from prompt).",
    )
    parser.add_argument(
        "--device-name",
        type=str,
        default=DEFAULT_DEVICE_NAME,
        help="Device to run stable-diffusion demo on.",
    )
    args = parser.parse_args([] if is_test else None)

    if not is_test:
        print(f"\n{'-' * 100}")
        print(
            f"** Performing image generation on-device({args.device_name}) with ControlNet - Stable Diffusion **"
        )
        print()
        print("Prompt:", args.prompt)
        print("Image:", args.image)
        print("Number of steps:", args.num_steps)
        print("Guidance scale:", args.guidance_scale)
        print("Seed:", args.seed)
        print()
        print(
            "Note: This reference demo uses significant amounts of memory and may take a few minutes to run."
        )
        print(f"{'-' * 100}\n")

    print(f"Downloading model assets\n{'-' * 50}")
    # Load components
    text_encoder = ClipVITTextEncoder.from_precompiled()
    unet = Unet.from_precompiled()
    vae_decoder = VAEDecoder.from_precompiled()
    controlnet = ControlNet.from_precompiled()

    # Create four HubModel instances to prepare for on-device inference.
    # This is similar to initializing PyTorch model to call forward method later.
    # Instead of forward, we later submit inference_jobs on QAI-Hub for
    # on-device evaluation.
    print(f"Uploading model assets on QAI-Hub\n{'-' * 50}")
    text_encoder = _get_hub_model(text_encoder, args.device_name)
    unet = _get_hub_model(unet, args.device_name)
    vae_decoder = _get_hub_model(vae_decoder, args.device_name)
    controlnet = _get_hub_model(controlnet, args.device_name)

    # Create tokenizer, scheduler and time_embedding required
    # for control-net pipeline.
    tokenizer = CLIPTokenizer.from_pretrained(
        "stabilityai/stable-diffusion-2-1-base", subfolder="tokenizer", revision="main"
    )

    scheduler = DPMSolverMultistepScheduler(
        beta_start=0.00085,
        beta_end=0.012,
        beta_schedule="scaled_linear",
        num_train_timesteps=1000,
    )

    embedding = UNet2DConditionModel.from_pretrained(
        "runwayml/stable-diffusion-v1-5", subfolder="unet"
    ).time_embedding

    # Load Application
    app = ControlNetApp(
        text_encoder=text_encoder,
        vae_decoder=vae_decoder,
        unet=unet,
        controlnet=controlnet,
        tokenizer=tokenizer,
        scheduler=scheduler,
        time_embedding=embedding,
    )

    # Generate image
    image = app.generate_image(
        args.prompt,
        load_image(args.image),
        num_steps=args.num_steps,
        seed=args.seed,
        guidance_scale=args.guidance_scale,
    )

    pil_img = Image.fromarray(np.round(image.numpy() * 255).astype(np.uint8)[0])

    if not is_test:
        # Save or show image
        if args.output is None:
            pil_img.show()
        else:
            pil_img.save(args.output)
            print()
            print("Image saved to", args.output)
            print()


if __name__ == "__main__":
    main()
