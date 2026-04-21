import base64
import httpx
from ..config import get_settings


class PdfLlmService:
    def __init__(self):
        self.settings = get_settings()

    async def process_pdf(self, pdf_data: bytes) -> str:
        base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
        data_url = f"data:application/pdf;base64,{base64_pdf}"

        payload = {
            "model": self.settings.model_name,
            "input": [
                {
                    "type": "file",
                    "data_url": data_url
                },
                {
                    "type": "text",
                    "content": "Extract all text content from this PDF document. Return the text in markdown format. Preserve headings, lists, tables, and formatting where possible."
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
