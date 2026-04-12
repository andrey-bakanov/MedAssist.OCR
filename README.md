# MedAssist.CommonOcr

A Python FastAPI service that extracts text in markdown format from images, PDFs, and DOCX files.

## Features

- **Image OCR (LLM)**: Extract text from JPEG/PNG images using LLM vision model
- **Image OCR (Tesseract)**: Extract Russian text from images using Tesseract OCR
- **PDF to Markdown**: Convert PDF documents to markdown format
- **DOCX to Markdown**: Convert Word documents to markdown format
- **Rate Limiting**: Configurable request rate limiting (default: 10 requests/second)
- **Queue Management**: Semaphore-based queue limiting concurrent model connections (default: 4)
- **Swagger UI**: Interactive API documentation at `/docs`

## Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│                              API Gateway                                │
│                    (Rate Limiter + Queue Manager)                       │
├─────────────┬─────────────────┬─────────────────┬─────────────────────┤
│ /image-md   │ /image-text     │ /pdf-markdown   │ /docx-markdown/hlth│
├─────────────┴─────────────────┴─────────────────┴─────────────────────┤
│                             Service Layer                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │
│  │ ImageOCR    │ │ImageText    │ │ PdfConvert  │ │ DocxConvert │    │
│  │ Service     │ │ Service     │ │ Service     │ │ Service     │    │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘    │
├───────────────────────────────────────────────────────────────────────┤
│                           External Services                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │
│  │ LLM API     │ │ Tesseract   │ │ pdftotext   │ │ pandoc      │    │
│  │ (localhost) │ │ OCR         │ │             │ │             │    │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘    │
└───────────────────────────────────────────────────────────────────────┘
```

## API Endpoints

### 1. POST `/convert/image-markdown`

Extract text from images (JPEG/PNG) using OCR.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` - Image file (jpg, png)

**Response:**
```json
{
  "success": true,
  "markdown": "# Extracted Text\n\n..."
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/convert/image-markdown \
  -F "file=@image.png"
```

### 2. POST `/convert/image-text`

Extract text from images (JPEG/PNG) using Tesseract OCR with Russian language support.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` - Image file (jpg, png)

**Response:**
```json
{
  "success": true,
  "markdown": "# Extracted Text\n\n..."
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/convert/image-text \
  -F "file=@image.png"
```

### 4. POST `/convert/pdf-markdown`

Convert PDF files to markdown format.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` - PDF file

**Response:**
```json
{
  "success": true,
  "markdown": "# Document Title\n\n..."
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/convert/pdf-markdown \
  -F "file=@document.pdf"
```

### 5. POST `/convert/docx-markdown`

Convert DOCX files to markdown format.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` - DOCX file

**Response:**
```json
{
  "success": true,
  "markdown": "# Document Title\n\n..."
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/convert/docx-markdown \
  -F "file=@document.docx"
```

### 6. GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "MedAssist.CommonOcr"
}
```

## Configuration

All configuration is managed via `.env` file:

```env
# Model Configuration (not exposed via API)
LM_API_TOKEN=your_token_here
MODEL_NAME=qwen/qwen3-vl-4b
MODEL_CONTEXT_LENGTH=2048
MODEL_TEMPERATURE=0
MODEL_API_URL=http://localhost:1234/api/v1/chat

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=false

# Rate Limiting
RATE_LIMIT_REQUESTS=10
QUEUE_MAX_CONNECTIONS=4

# Paths
PANDOC_PATH=/usr/bin/pandoc
PDFTOTEXT_PATH=/usr/bin/pdftotext
```

## Rate Limiting & Queue

- **Rate Limiter**: Limits incoming requests to 10 per second (configurable via `RATE_LIMIT_REQUESTS`)
- **Queue Manager**: Semaphore-based queue that allows only 4 concurrent connections to the LLM model (configurable via `QUEUE_MAX_CONNECTIONS`)

## Running with Docker

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Using Dockerfile

```bash
docker build -t medassist-common-ocr .
docker run -p 8000:8000 --env-file .env medassist-common-ocr
```

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure `.env` file (copy from `.env.example`)

3. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
MedAssist.CommonOcr/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Configuration from .env
│   ├── routes/
│   │   ├── image_route.py      # /convert/image-markdown
│   │   ├── image_text_route.py # /convert/image-text
│   │   ├── pdf_route.py        # /convert/pdf-markdown
│   │   ├── docx_route.py       # /convert/docx-markdown
│   │   └── health_route.py     # /health
│   ├── services/
│   │   ├── image_service.py    # OCR proxy logic (LLM)
│   │   ├── image_text_service.py # Tesseract OCR logic
│   │   ├── pdf_service.py      # PDF to markdown logic
│   │   └── docx_service.py     # DOCX to markdown logic
│   ├── middleware/
│   │   ├── rate_limiter.py     # Rate limiting (10 req/s)
│   │   └── queue_manager.py    # Queue with semaphore (4 connections)
│   └── models/
│       └── schemas.py          # Pydantic models
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Dependencies

- **FastAPI** - Web framework
- **uvicorn** - ASGI server
- **python-multipart** - File uploads
- **pydantic** - Data validation
- **slowapi** - Rate limiting
- **httpx** - HTTP client for model API
- **python-docx** - DOCX reading
- **pytesseract** - Python wrapper for Tesseract OCR
- **Pillow** - Python Imaging Library
- **poppler-utils** - PDF text extraction (pdftotext)
- **pandoc** - Document conversion
- **tesseract-ocr** - OCR engine with Russian language support
