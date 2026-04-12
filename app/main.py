from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .config import get_settings
from .middleware.rate_limiter import limiter
from .middleware.queue_manager import queue_manager
from .routes import image_route, pdf_route, docx_route, health_route, image_text_route

settings = get_settings()

app = FastAPI(
    title="MedAssist.CommonOcr",
    description="OCR and document conversion service for extracting markdown text from images, PDFs, and DOCX files.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

queue_manager.initialize()

app.include_router(image_route.router)
app.include_router(pdf_route.router)
app.include_router(docx_route.router)
app.include_router(health_route.router)
app.include_router(image_text_route.router)


@app.on_event("startup")
async def startup_event():
    queue_manager.initialize()


@app.get("/")
async def root():
    return {
        "service": "MedAssist.CommonOcr",
        "version": "1.0.0",
        "docs": "/docs"
    }
