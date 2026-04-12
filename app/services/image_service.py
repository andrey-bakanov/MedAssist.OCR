import base64
import httpx
from typing import Optional
from ..config import get_settings


class ImageService:
    def __init__(self):
        self.settings = get_settings()

    async def process_image(self, image_data: bytes, mime_type: str) -> str:
        base64_image = base64.b64encode(image_data).decode("utf-8")
        data_url = f"data:{mime_type};base64,{base64_image}"

        payload = {
            "model": self.settings.model_name,
            "input": [
                {
                    "type": "image",
                    "data_url": data_url
                },
                {
                    "type": "text",
                    "content": "Extract all text content from this image. Return the text in markdown format. Preserve headings, lists, and formatting where possible."
                }
            ],
            "context_length": self.settings.model_context_length,
            "temperature": self.settings.model_temperature
        }

        headers = {
            "Authorization": f"Bearer {self.settings.lm_api_token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                self.settings.model_api_url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()

        content = result.get("output", [{}])[0].get("content", "")
        return content

    def get_mime_type(self, filename: str) -> str:
        ext = filename.lower().split(".")[-1]
        mime_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png"
        }
        return mime_types.get(ext, "image/png")
