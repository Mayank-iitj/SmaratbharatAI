from pydantic import BaseModel

# In a real setup, we would query the pgvector database in Supabase
# for schemes matching the user's criteria.

class SchemeMatch(BaseModel):
    name: str
    description: str
    match_score: float

class SchemeResponse(BaseModel):
    response: str
    recommended_schemes: list[SchemeMatch]

def handle_scheme_query(query: str, user_profile: dict = None) -> SchemeResponse:
    """Mock handler for the Scheme Recommendation Agent."""
    
    # Mock some data
    schemes = [
        SchemeMatch(
            name="PM Kisan Samman Nidhi", 
            description="Income support of Rs. 6000/- per year to all landholding farmer families.",
            match_score=0.92
        ),
        SchemeMatch(
            name="Stand-Up India Scheme",
            description="Facilitates bank loans between 10 lakh and 1 Crore to at least one SC/ST borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.",
            match_score=0.85
        )
    ]
    
    return SchemeResponse(
        response=f"Based on your query '{query}', here are some recommended government schemes:",
        recommended_schemes=schemes
    )
