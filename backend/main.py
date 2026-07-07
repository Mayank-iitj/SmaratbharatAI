"""SmartBharat AI FastAPI Backend.

India's First AI-Powered Civic Operating System backend service.
Provides scheme discovery, civic complaints, document OCR, and AI chat.
"""
import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

load_dotenv()

from api.auth import router as auth_router
from api.complaints import router as complaints_router
from api.documents import router as documents_router
from api.schemes import router as schemes_router
from middleware.security import SecurityHeadersMiddleware

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan — pre-warm services on startup."""
    logger.info("SmartBharat AI starting up…")
    try:
        from services.rag import init_vector_store
        init_vector_store()
        logger.info("Vector store pre-warmed successfully.")
    except Exception as exc:
        logger.warning("Could not pre-warm vector store: %s", exc)
    yield
    logger.info("SmartBharat AI shutting down.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SmartBharat AI API",
    version="1.0.0",
    description=(
        "India's AI-Powered Civic Operating System — "
        "scheme discovery, civic complaints, document OCR, and policy simplification."
    ),
    contact={"name": "SmartBharat AI Team"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SecurityHeadersMiddleware)

ALLOWED_ORIGINS: list[str] = list(filter(None, [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.getenv("FRONTEND_URL", ""),
]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(schemes_router, prefix="/api")
app.include_router(complaints_router, prefix="/api")
app.include_router(documents_router, prefix="/api")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    """Chat request schema."""

    message: str = Field(..., min_length=1, max_length=2000, description="User message text")
    user_id: str = Field(..., min_length=1, max_length=128, description="Unique user identifier")
    mode: str = Field(default="general", description="Chat mode: general | schemes | policy")

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be blank.")
        return v

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        if v not in ("general", "schemes", "policy"):
            raise ValueError("mode must be one of: general, schemes, policy")
        return v


class ChatResponse(BaseModel):
    """Chat response schema."""

    response: str
    agent: str
    suggested_actions: list[str]
    mode: str = "general"


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"], summary="Root")
def read_root() -> dict[str, str]:
    """Return API welcome message."""
    return {"message": "Welcome to SmartBharat AI API", "version": "1.0.0"}


@app.get("/health", tags=["Health"], summary="Health check")
def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok", "service": "smartbharat-ai"}


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------
@app.post(
    "/api/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="AI civic chat with intelligent routing",
    description=(
        "Routes user messages through a LangGraph agent workflow. "
        "Supports general civic queries, scheme recommendations (RAG), "
        "and policy simplification modes."
    ),
)
@limiter.limit("30/minute")
async def chat_endpoint(request: Request, req: ChatRequest) -> ChatResponse:
    """Process a user chat message via the LangGraph agent workflow.

    The router agent selects the appropriate sub-agent:
    - **companion**: General civic Q&A and navigation
    - **schemes**: RAG-powered scheme recommendations
    - **policy**: Policy document simplification
    """
    logger.info("Chat request | user=%s | mode=%s | message_len=%d",
                req.user_id, req.mode, len(req.message))
    try:
        from agents.router import process_chat
        res = process_chat(req.message, mode=req.mode)
        return ChatResponse(
            response=res["response"],
            agent=res["agent"],
            suggested_actions=res["suggested_actions"],
            mode=req.mode,
        )
    except Exception as exc:
        logger.error("Chat endpoint error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service temporarily unavailable. Please try again.",
        ) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
