from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, Image) for verification and OCR processing.
    """
    # Mock OCR and Verification logic
    return {
        "status": "success",
        "filename": file.filename,
        "extracted_data": {
            "document_type": "Aadhaar",
            "name": "Rahul Sharma",
            "is_valid": True
        }
    }
