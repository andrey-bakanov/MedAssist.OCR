import httpx
from fastapi import APIRouter, UploadFile, File, Request
from ..models.schemas import ConversionResponse
from ..services.image_service import ImageService
from ..middleware.rate_limiter import limiter
from ..middleware.queue_manager import queue_manager
from ..config import get_settings

router = APIRouter(prefix="/convert", tags=["Image"])
image_service = ImageService()


@router.post("/image-markdown", response_model=ConversionResponse)
@limiter.limit(get_settings().rate_limit_requests)
async def convert_image_to_markdown(request: Request, file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return ConversionResponse(
            success=False,
            error="Unsupported file type. Only JPEG and PNG images are supported."
        )

    try:
        image_data = await file.read()
        mime_type = image_service.get_mime_type(file.filename)

        await queue_manager.acquire()
        try:
            markdown = await image_service.process_image(image_data, mime_type)
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
