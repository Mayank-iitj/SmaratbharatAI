"""Schemes API router."""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List

router = APIRouter(prefix="/schemes", tags=["Schemes"])


class Scheme(BaseModel):
    """Representation of a government scheme."""

    id: int = Field(..., description="Unique scheme identifier")
    name: str = Field(..., description="Scheme name")
    description: str = Field(..., description="Short description")
    eligibility_criteria: str = Field(..., description="Who can apply")
    official_link: str = Field(..., description="Official government URL")
    category: str = Field(default="General", description="Scheme category")


SEED_SCHEMES: list[Scheme] = [
    Scheme(
        id=1,
        name="PM Kisan Samman Nidhi",
        description="Income support of Rs. 6000/- per year to all landholding farmer families.",
        eligibility_criteria="Landholding farmers with cultivable land",
        official_link="https://pmkisan.gov.in",
        category="Agriculture",
    ),
    Scheme(
        id=2,
        name="Stand-Up India Scheme",
        description="Facilitates bank loans between 10 lakh and 1 Crore for SC/ST and women entrepreneurs.",
        eligibility_criteria="SC/ST borrowers and women setting up greenfield enterprises",
        official_link="https://www.standupmitra.in",
        category="Entrepreneurship",
    ),
    Scheme(
        id=3,
        name="Pradhan Mantri Awas Yojana",
        description="Housing for all — provides subsidies for building homes for lower income groups.",
        eligibility_criteria="Economically weaker sections and low-income groups without pucca house",
        official_link="https://pmaymis.gov.in",
        category="Housing",
    ),
    Scheme(
        id=4,
        name="Sukanya Samriddhi Yojana",
        description="Small deposit savings scheme for the girl child under Beti Bachao Beti Padhao.",
        eligibility_criteria="Parents/guardians of girl child below 10 years",
        official_link="https://www.indiapost.gov.in",
        category="Women & Child",
    ),
    Scheme(
        id=5,
        name="Post Matric Scholarship for Minorities",
        description="Financial assistance to meritorious minority students for higher education.",
        eligibility_criteria="Students from Muslim, Christian, Sikh, Buddhist, Jain or Parsi communities",
        official_link="https://scholarships.gov.in",
        category="Education",
    ),
]


@router.get(
    "/",
    response_model=List[Scheme],
    summary="List all government schemes",
)
async def list_schemes(
    category: str = Query(None, description="Filter by scheme category"),
) -> List[Scheme]:
    """Retrieve all available government schemes, optionally filtered by category."""
    if category:
        filtered = [s for s in SEED_SCHEMES if s.category.lower() == category.lower()]
        return filtered
    return SEED_SCHEMES


@router.get(
    "/{scheme_id}",
    response_model=Scheme,
    summary="Get scheme details",
)
async def get_scheme(scheme_id: int) -> Scheme:
    """Retrieve details of a specific government scheme by ID."""
    for scheme in SEED_SCHEMES:
        if scheme.id == scheme_id:
            return scheme
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scheme with ID {scheme_id} not found.",
    )


@router.get(
    "/recommendations",
    summary="Get personalized scheme recommendations",
)
async def get_recommendations(
    user_id: str = Query(..., min_length=1, max_length=128, description="User identifier"),
    query: str = Query(None, max_length=500, description="Search query for scheme matching"),
) -> dict:
    """Get personalized scheme recommendations.

    Uses the RAG vector store for semantic matching against the user's query.
    """
    if query:
        try:
            from services.rag import search_schemes
            results = search_schemes(query, k=3)
            return {"status": "success", "user_id": user_id, "recommendations": results}
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "message": str(exc), "recommendations": []}
    return {"status": "success", "user_id": user_id, "recommendations": []}
