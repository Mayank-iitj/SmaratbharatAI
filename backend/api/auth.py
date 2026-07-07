"""Authentication API router with JWT token support."""
import os
import hashlib
import hmac
import time
import json
import base64
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)

# ---------------------------------------------------------------------------
# Simple HMAC-based JWT (no external deps)
# ---------------------------------------------------------------------------
_SECRET = os.getenv("JWT_SECRET", "smartbharat-dev-secret-change-in-production")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _create_token(user_id: str, name: str, role: str = "citizen") -> str:
    """Create a signed HMAC JWT-like token."""
    header = _b64url(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = _b64url(json.dumps({
        "sub": user_id, "name": name, "role": role,
        "iat": int(time.time()), "exp": int(time.time()) + 86400
    }).encode())
    sig = _b64url(hmac.new(_SECRET.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest())
    return f"{header}.{payload}.{sig}"


def _verify_token(token: str) -> Optional[dict]:
    """Verify a token and return its payload, or None if invalid."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, payload, sig = parts
        expected = _b64url(hmac.new(_SECRET.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected):
            return None
        data = json.loads(base64.urlsafe_b64decode(payload + "=="))
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict:
    """Dependency to extract and validate the current user from bearer token."""
    if not credentials:
        # Allow unauthenticated for demo purposes
        return {"user_id": "user_123", "name": "Rahul Sharma", "role": "citizen"}
    payload = _verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class LoginRequest(BaseModel):
    """Login credentials."""

    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)

    @field_validator("username")
    @classmethod
    def sanitize_username(cls, v: str) -> str:
        return v.strip().lower()


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400


class UserProfile(BaseModel):
    """Authenticated user profile."""

    user_id: str
    name: str
    role: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and get access token",
)
async def login(credentials: LoginRequest) -> TokenResponse:
    """Authenticate a citizen and return a signed JWT token.

    In production, validates against Supabase Auth or Google OAuth.
    Demo credentials: username=user, password=password
    """
    # Demo credential check — replace with real auth in production
    valid = (
        credentials.username == "user" and
        hmac.compare_digest(credentials.password, "password")
    )
    if not valid:
        logger.warning("Failed login attempt for username: %s", credentials.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please check your username and password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = _create_token("user_123", "Rahul Sharma")
    logger.info("Successful login for: %s", credentials.username)
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Get current authenticated user profile",
)
async def get_me(current_user: dict = Depends(get_current_user)) -> UserProfile:
    """Return the profile of the currently authenticated user."""
    return UserProfile(
        user_id=current_user.get("sub", "user_123"),
        name=current_user.get("name", "Citizen"),
        role=current_user.get("role", "citizen"),
    )
