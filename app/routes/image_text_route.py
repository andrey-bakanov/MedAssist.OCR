from fastapi import APIRouter, UploadFile, File, Request
from ..models.schemas import ConversionResponse
from ..services.image_text_service import ImageTextService
from ..middleware.rate_limiter import limiter
from ..config import get_settings

router = APIRouter(prefix="/convert", tags=["Image Text"])


@router.post("/image-text", response_model=ConversionResponse)
@limiter.limit(get_settings().rate_limit_requests)
async def convert_image_to_text(request: Request, file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return ConversionResponse(
            success=False,
            error="Unsupported file type. Only JPEG and PNG images are supported."
        )

    try:
        image_data = await file.read()
        image_text_service = ImageTextService()
        markdown = await image_text_service.process_image(image_data)
        return ConversionResponse(success=True, markdown=markdown)
    except Exception as e:
        return ConversionResponse(success=False, error=str(e))
