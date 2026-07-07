"""Documents API router — OCR and document verification via Groq Vision."""
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel

router = APIRouter(prefix="/documents", tags=["Documents"])

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


class DocumentOCRResponse(BaseModel):
    """Response schema for document OCR."""

    status: str
    filename: str
    extracted_data: dict


@router.post(
    "/upload",
    response_model=DocumentOCRResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload document for OCR and verification",
)
async def upload_document(file: UploadFile = File(...)) -> DocumentOCRResponse:
    """Upload a government ID document (Aadhaar, PAN, DL) for OCR verification.

    Uses Groq Vision (llama-3.2-11b-vision-preview) to extract structured
    data from the uploaded image.
    """
    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{file.content_type}'. "
                   f"Allowed: {', '.join(sorted(ALLOWED_MIME_TYPES))}",
        )

    # Read and validate file size
    image_data = await file.read()
    if len(image_data) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE_BYTES // (1024*1024)} MB.",
        )

    # Invoke Groq Vision
    try:
        from agents.vision_agent import extract_document_ocr
        result = extract_document_ocr(image_data, file.content_type)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OCR service temporarily unavailable: {exc}",
        ) from exc

    return DocumentOCRResponse(
        status=result.get("status", "success"),
        filename=file.filename or "unknown",
        extracted_data=result,
    )


@router.post(
    "/analyze-complaint",
    summary="Analyze complaint image via AI vision",
)
async def analyze_complaint_image(file: UploadFile = File(...)) -> dict:
    """Upload an image of a civic issue for AI-powered complaint generation.

    Uses Groq Vision to identify the issue category, severity, and description.
    """
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type. Allowed: {', '.join(sorted(ALLOWED_MIME_TYPES))}",
        )

    image_data = await file.read()
    if len(image_data) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum size is 5 MB.",
        )

    try:
        from agents.vision_agent import analyze_complaint_image as vision_analyze
        result = vision_analyze(image_data, file.content_type)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Vision service temporarily unavailable: {exc}",
        ) from exc

    return result
