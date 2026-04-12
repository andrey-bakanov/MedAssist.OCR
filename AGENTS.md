# AGENTS.md

## Project Overview
MedAssist.CommonOcr is a FastAPI service that extracts text in markdown format from images, PDFs, and DOCX files. It acts as a proxy service for OCR and document conversion.

## Key Commands

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker commands
```bash
docker-compose up -d      # Start with docker-compose
docker build -t medassist-common-ocr .  # Build image
```

### Run tests
```bash
pytest tests/ -v
```

## Code Conventions

- Use async/await for all I/O operations
- Each endpoint has its own service class
- Configuration from .env using pydantic-settings
- Response format: `ConversionResponse(success, markdown, error)`
- Rate limiting via slowapi decorator
- Queue management via asyncio.Semaphore

## File Organization

- `app/routes/` - API endpoint definitions
- `app/services/` - Business logic (ImageService, PdfService, DocxService)
- `app/middleware/` - RateLimiter and QueueManager
- `app/models/` - Pydantic schemas
