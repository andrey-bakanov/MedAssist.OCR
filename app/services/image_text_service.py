import io
from PIL import Image
import pytesseract
from ..config import get_settings


class ImageTextService:
    def __init__(self):
        self.settings = get_settings()

    async def process_image(self, image_data: bytes) -> str:
        image = Image.open(io.BytesIO(image_data))
        
        text = pytesseract.image_to_string(image, lang='rus')
        
        markdown = self._format_as_markdown(text)
        return markdown

    def _format_as_markdown(self, text: str) -> str:
        lines = text.split('\n')
        markdown_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                markdown_lines.append('')
                continue
            
            if stripped.isupper() and len(stripped) > 3:
                markdown_lines.append(f"## {stripped}")
            elif stripped.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                markdown_lines.append(f"- {stripped}")
            else:
                markdown_lines.append(stripped)
        
        return '\n'.join(markdown_lines)

    def get_mime_type(self, filename: str) -> str:
        ext = filename.lower().split(".")[-1]
        mime_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png"
        }
        return mime_types.get(ext, "image/png")
