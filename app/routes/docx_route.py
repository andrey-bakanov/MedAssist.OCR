from fastapi import APIRouter, UploadFile, File, Request
from ..models.schemas import ConversionResponse
from ..services.docx_service import DocxService
from ..middleware.rate_limiter import limiter
from ..config import get_settings

router = APIRouter(prefix="/convert", tags=["DOCX"])
docx_service = DocxService()


@router.post("/docx-markdown", response_model=ConversionResponse)
@limiter.limit(get_settings().rate_limit_requests)
async def convert_docx_to_markdown(request: Request, file: UploadFile = File(...)):
    if file.content_type not in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    ]:
        return ConversionResponse(
            success=False,
            error="Unsupported file type. Only DOCX files are supported."
        )

    try:
        docx_data = await file.read()
        markdown = await docx_service.process_docx(docx_data)
        return ConversionResponse(success=True, markdown=markdown)
    except Exception as e:
        return ConversionResponse(success=False, error=str(e))
