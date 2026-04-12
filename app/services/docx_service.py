import subprocess
import tempfile
import os
from ..config import get_settings


class DocxService:
    def __init__(self):
        self.settings = get_settings()

    async def process_docx(self, docx_data: bytes) -> str:
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as docx_file:
            docx_file.write(docx_data)
            docx_path = docx_file.name

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as md_file:
            md_path = md_file.name

        try:
            pandoc_cmd = [
                self.settings.pandoc_path,
                docx_path,
                "-f", "docx",
                "-t", "markdown",
                "-o", md_path
            ]
            subprocess.run(
                pandoc_cmd,
                check=True,
                capture_output=True
            )

            with open(md_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()

            return markdown_content
        finally:
            if os.path.exists(docx_path):
                os.unlink(docx_path)
            if os.path.exists(md_path):
                os.unlink(md_path)
