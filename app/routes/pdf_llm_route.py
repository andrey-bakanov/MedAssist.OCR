import httpx
from fastapi import APIRouter, UploadFile, File, Request
from ..models.schemas import ConversionResponse
from ..services.pdf_llm_service import PdfLlmService
from ..middleware.rate_limiter import limiter
from ..middleware.queue_manager import queue_manager
from ..config import get_settings

router = APIRouter(prefix="/convert", tags=["PDF"])
pdf_llm_service = PdfLlmService()


@router.post("/pdf-markdown-llm", response_model=ConversionResponse)
@limiter.limit(get_settings().rate_limit_requests)
async def convert_pdf_to_markdown_llm(request: Request, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return ConversionResponse(
            success=False,
            error="Unsupported file type. Only PDF files are supported."
        )

    try:
        pdf_data = await file.read()

        await queue_manager.acquire()
        try:
            markdown = await pdf_llm_service.process_pdf(pdf_data)
        finally:
            queue_manager.release()

        return ConversionResponse(success=True, markdown=markdown)
    except httpx.HTTPStatusError as e:
        return ConversionResponse(
            success=False,
            error=f"Model API error: {e.response.status_code}"
        )
    except Exception as e:
        return ConversionResponse(success=False, error=str(e))
