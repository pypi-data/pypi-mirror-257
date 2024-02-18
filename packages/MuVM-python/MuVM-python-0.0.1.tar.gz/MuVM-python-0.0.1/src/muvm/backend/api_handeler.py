import io
import time
from pathlib import Path

import numpy as np
import torch
import uvicorn
from .api_classes import BaseModel, ImageVariationRequest, ImageTextToImageRequest, ImageToImageRequest
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from ..algorithms import (
    ImageVariationPipeline,
    LDMSuperResolutionPipeline,
    BriaRMBG,
    postprocess_image,
    preprocess_image
)
from torchvision import transforms
from PIL import Image


class EnhancerAlgoAPI:
    def __init__(
            self
    ):
        self.api = FastAPI()
        self.api.post("/variation_api")(self.image_variation)
        self.api.post("/image_to_image_api")(self.image_to_image)
        self.api.post("/image_text_to_image_api")(self.image_text_to_image)
        self.api.post("/image_upscaler_api")(self.image_upscaler)
        self.api.post("/image_background_remover_api")(self.image_background_remover)
        self.variation_model = None
        self.upscaler_model = None
        self.background_remover_model = None
        # self.variation_model.enable_model_cpu_offload()

    async def get_variation_model(self) -> ImageVariationPipeline:
        if self.variation_model is None:
            variation_model = ImageVariationPipeline.from_pretrained(
                "LucidBrains/image-variations",
                torch_dtype=torch.float32
            )
            variation_model.run_safety_checker = lambda image, device, _: (image, None)
            self.variation_model = variation_model
        return self.variation_model

    async def get_upscaler_model(self) -> LDMSuperResolutionPipeline:
        if self.upscaler_model is None:
            upscaler_model = LDMSuperResolutionPipeline.from_pretrained(
                "CompVis/ldm-super-resolution-4x-openimages",
                torch_dtype=torch.float32
            )
            self.upscaler_model = upscaler_model
        return self.upscaler_model

    async def get_background_remover_model(self) -> LDMSuperResolutionPipeline:
        if self.background_remover_model is None:
            background_remover_model = BriaRMBG.from_pretrained(
                "LucidBrains/BGRM",
            )
            background_remover_model.eval()
            background_remover_model.to("cuda:0")
            self.background_remover_model = background_remover_model
        return self.background_remover_model

    async def image_background_remover(self, image: UploadFile = File(...)):
        input_image = Image.open(
            io.BytesIO(
                await image.read()
            )
        ).convert("RGB")
        model = await self.get_background_remover_model()

        model_input_size = [1024, 1024]
        orig_im = np.array(input_image)
        orig_im_size = orig_im.shape[0:2]
        image = preprocess_image(orig_im, model_input_size).to("cuda:0")
        result = model(image)
        result_image = postprocess_image(result[0][0], orig_im_size)

        pil_im = Image.fromarray(result_image)
        no_bg_image = Image.new("RGBA", pil_im.size, (0, 0, 0, 0))
        no_bg_image.paste(input_image, mask=pil_im)
        out = no_bg_image
        out.save("response_image.png", bitmap_format="png")
        return FileResponse(Path("response_image.png"))

    async def image_text_to_image(self, request: ImageTextToImageRequest):
        ...

    async def image_to_image(self, request: ImageToImageRequest):
        ...

    async def image_upscaler(self, image: UploadFile = File(...)):
        input_image = Image.open(
            io.BytesIO(
                await image.read()
            )
        ).convert("RGB").resize((128, 128))
        # h, w = input_image.size
        # input_image = input_image.resize((h // 2, w // 2))
        model = await self.get_upscaler_model()
        out = model(
            input_image, num_inference_steps=100, eta=1
        )

        out["images"][0].save("response_image.png", bitmap_format="png")
        input_image.save("response_image.png", bitmap_format="png")
        return FileResponse(Path("response_image.png"))

    async def image_variation(self, image: UploadFile = File(...)):
        tform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize(
                (224, 224),
                interpolation=transforms.InterpolationMode.BICUBIC,
                antialias=False,
            ),
            transforms.Normalize(
                [0.48145466, 0.4578275, 0.40821073],
                [0.26862954, 0.26130258, 0.27577711]),
        ])
        out = self.variation_model(
            tform(
                Image.open(
                    io.BytesIO(
                        await image.read()
                    )
                )
            ).to("cpu").unsqueeze(0), guidance_scale=3
        )
        out["images"][0].save("response_image.png", bitmap_format="png")
        return FileResponse(Path("response_image.png"))

    def fire(self):
        uvicorn.run(self.api, host="0.0.0.0", port=8000)
