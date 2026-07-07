from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(credentials: dict):
    """
    Mock login endpoint. 
    In production, integrate with Google OAuth or Supabase Auth.
    """
    if credentials.get("username") == "user" and credentials.get("password") == "pass":
        return {"access_token": "mock_jwt_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/me")
async def get_current_user():
    """Mock get current user."""
    return {"user_id": "user_123", "name": "Rahul Sharma", "role": "citizen"}
