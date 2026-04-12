import tempfile
from fastapi import APIRouter, UploadFile, File, Request
from ..models.schemas import ConversionResponse
from ..services.pdf_service import PdfService
from ..middleware.rate_limiter import limiter
from ..config import get_settings

router = APIRouter(prefix="/convert", tags=["PDF"])
pdf_service = PdfService()


@router.post("/pdf-markdown", response_model=ConversionResponse)
@limiter.limit(get_settings().rate_limit_requests)
async def convert_pdf_to_markdown(request: Request, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return ConversionResponse(
            success=False,
            error="Unsupported file type. Only PDF files are supported."
        )

    try:
        pdf_data = await file.read()
        markdown = await pdf_service.process_pdf(pdf_data)
        return ConversionResponse(success=True, markdown=markdown)
    except Exception as e:
        return ConversionResponse(success=False, error=str(e))
