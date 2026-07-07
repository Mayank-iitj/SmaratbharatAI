from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/complaints", tags=["Complaints"])

class ComplaintCreate(BaseModel):
    category: str
    description: str
    location: str
    image_url: Optional[str] = None

@router.post("/")
async def submit_complaint(complaint: ComplaintCreate):
    """
    Submit a new civic complaint.
    In production, this would upload images to Supabase Storage and record in the DB.
    """
    return {"status": "success", "complaint_id": 101, "message": "Complaint registered successfully."}

@router.get("/{complaint_id}")
async def track_complaint(complaint_id: int):
    """
    Track status of a complaint.
    """
    return {"complaint_id": complaint_id, "status": "In Progress", "estimated_resolution": "2 Days"}
