import subprocess
import tempfile
import os
from ..config import get_settings


class PdfService:
    def __init__(self):
        self.settings = get_settings()

    async def process_pdf(self, pdf_data: bytes) -> str:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
            pdf_file.write(pdf_data)
            pdf_path = pdf_file.name

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as txt_file:
            txt_path = txt_file.name

        try:
            pdftotext_cmd = [
                self.settings.pdftotext_path,
                "-layout",
                pdf_path,
                txt_path
            ]
            subprocess.run(
                pdftotext_cmd,
                check=True,
                capture_output=True
            )

            with open(txt_path, "r", encoding="utf-8") as f:
                text_content = f.read()

            markdown = self._convert_to_markdown(text_content)
            return markdown
        finally:
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)
            if os.path.exists(txt_path):
                os.unlink(txt_path)

    def _convert_to_markdown(self, text_content: str) -> str:
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8", delete=False) as input_file:
            input_file.write(text_content)
            input_path = input_file.name

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as output_file:
            output_path = output_file.name

        try:
            pandoc_cmd = [
                self.settings.pandoc_path,
                input_path,
                "-f", "commonmark",
                "-t", "markdown",
                "-o", output_path
            ]
            subprocess.run(
                pandoc_cmd,
                check=True,
                capture_output=True
            )

            with open(output_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()

            return markdown_content
        finally:
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
