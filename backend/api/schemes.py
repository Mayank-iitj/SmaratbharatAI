from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/schemes", tags=["Schemes"])

class Scheme(BaseModel):
    id: int
    name: str
    description: str
    eligibility_criteria: str
    official_link: str

@router.get("/", response_model=List[Scheme])
async def list_schemes():
    """
    Retrieve all government schemes.
    In production, this would query the Supabase PostgreSQL database.
    """
    return [
        {
            "id": 1,
            "name": "PM Kisan Samman Nidhi",
            "description": "Income support to farmers",
            "eligibility_criteria": "Landholding farmers",
            "official_link": "https://pmkisan.gov.in"
        }
    ]

@router.get("/recommendations")
async def get_recommendations(user_id: str):
    """
    Get personalized scheme recommendations for a specific user.
    Uses vector search over embeddings in production.
    """
    # Integrate with Scheme Recommender Agent logic here
    return {"status": "success", "recommendations": []}
