"""SmartBharat AI FastAPI Backend.

India's First AI-Powered Civic Operating System backend service.
"""
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from api.auth import router as auth_router
from api.complaints import router as complaints_router
from api.documents import router as documents_router
from api.schemes import router as schemes_router
from middleware.security import SecurityHeadersMiddleware

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan handler — warm up services on startup."""
    # Pre-warm the vector store so first request is fast
    try:
        from services.rag import init_vector_store
        init_vector_store()
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: Could not pre-warm vector store: {exc}")
    yield


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SmartBharat AI API",
    version="1.0.0",
    description=(
        "India's AI-Powered Civic Operating System — "
        "scheme discovery, civic complaints, and policy simplification."
    ),
    lifespan=lifespan,
)

# Rate-limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# CORS — restrict to known origins in production
ALLOWED_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)

# Routers
app.include_router(auth_router, prefix="/api")
app.include_router(schemes_router, prefix="/api")
app.include_router(complaints_router, prefix="/api")
app.include_router(documents_router, prefix="/api")


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    """Request body for the /api/chat endpoint."""

    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    user_id: str = Field(..., min_length=1, max_length=128, description="Unique user identifier")

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        """Strip leading/trailing whitespace and reject empty strings."""
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be blank.")
        return v


class ChatResponse(BaseModel):
    """Response body for the /api/chat endpoint."""

    response: str
    agent: str
    suggested_actions: list[str]


# ---------------------------------------------------------------------------
# Health & root endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"], summary="Root")
def read_root() -> dict[str, str]:
    """Return a welcome message."""
    return {"message": "Welcome to SmartBharat AI API"}


@app.get("/health", tags=["Health"], summary="Health check")
def health_check() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Chat endpoint
# ---------------------------------------------------------------------------
@app.post(
    "/api/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Civic AI chat",
)
@limiter.limit("30/minute")
async def chat_endpoint(request: Request, req: ChatRequest) -> ChatResponse:
    """Route user message through the LangGraph agent workflow.

    The router agent decides whether to invoke the Civic Companion or the
    Scheme Recommender and returns a structured response with suggested
    follow-up actions.
    """
    try:
        from agents.router import process_chat
        res = process_chat(req.message)
        return ChatResponse(
            response=res["response"],
            agent=res["agent"],
            suggested_actions=res["suggested_actions"],
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service temporarily unavailable: {exc}",
        ) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
