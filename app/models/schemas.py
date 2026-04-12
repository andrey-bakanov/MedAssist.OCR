from pydantic import BaseModel
from typing import Optional


class ConversionResponse(BaseModel):
    success: bool
    markdown: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    service: str = "MedAssist.CommonOcr"
