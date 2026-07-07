"""Application configuration management."""
import os
from functools import lru_cache
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Central application settings loaded from environment variables."""

    # AI
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama3-70b-8192")
    groq_vision_model: str = Field(default="llama-3.2-11b-vision-preview")

    # Auth
    jwt_secret: str = Field(default="smartbharat-dev-secret-change-in-production", alias="JWT_SECRET")

    # CORS
    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")

    # Database
    database_url: str = Field(default="", alias="DATABASE_URL")

    # Embeddings
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")

    # Rate limits
    global_rate_limit: str = Field(default="60/minute")
    chat_rate_limit: str = Field(default="30/minute")

    # App
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = {"populate_by_name": True}

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
            JWT_SECRET=os.getenv("JWT_SECRET", "smartbharat-dev-secret-change-in-production"),
            FRONTEND_URL=os.getenv("FRONTEND_URL", "http://localhost:3000"),
            DATABASE_URL=os.getenv("DATABASE_URL", ""),
            APP_ENV=os.getenv("APP_ENV", "development"),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings.from_env()
