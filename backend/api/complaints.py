"""Complaints API router."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional

router = APIRouter(prefix="/complaints", tags=["Complaints"])

VALID_CATEGORIES = {
    "Pothole", "Garbage", "Streetlight", "Water Leak",
    "Sewage", "Road Damage", "Park Maintenance", "Other"
}


class ComplaintCreate(BaseModel):
    """Schema for creating a new civic complaint."""

    category: str = Field(..., min_length=1, max_length=64, description="Complaint category")
    description: str = Field(..., min_length=10, max_length=1000, description="Detailed description")
    location: str = Field(..., min_length=3, max_length=256, description="Location of the issue")
    image_url: Optional[str] = Field(None, max_length=512, description="Optional image URL")

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        """Ensure category is from allowed set."""
        if v not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(sorted(VALID_CATEGORIES))}")
        return v

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, v: str) -> str:
        """Strip whitespace."""
        return v.strip()

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        """Strip whitespace."""
        return v.strip()


class ComplaintResponse(BaseModel):
    """Response schema after submitting a complaint."""

    status: str
    complaint_id: int
    message: str


class ComplaintStatus(BaseModel):
    """Status of an existing complaint."""

    complaint_id: int
    status: str
    estimated_resolution: str


@router.post(
    "/",
    response_model=ComplaintResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a civic complaint",
)
async def submit_complaint(complaint: ComplaintCreate) -> ComplaintResponse:
    """Submit a new civic complaint.

    In production, uploads images to Supabase Storage and records in PostgreSQL.
    """
    # TODO: persist to database
    return ComplaintResponse(
        status="success",
        complaint_id=101,
        message="Complaint registered successfully. You will be notified of updates.",
    )


@router.get(
    "/{complaint_id}",
    response_model=ComplaintStatus,
    summary="Track complaint status",
)
async def track_complaint(complaint_id: int) -> ComplaintStatus:
    """Retrieve the current status of a submitted complaint."""
    if complaint_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint ID must be a positive integer.",
        )
    # TODO: fetch from database
    return ComplaintStatus(
        complaint_id=complaint_id,
        status="In Progress",
        estimated_resolution="2 Days",
    )
