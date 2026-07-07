"""Shared pytest fixtures for SmartBharat AI test suite."""
import os
import sys
import pytest

# Ensure GROQ_API_KEY is set for tests (mock value)
os.environ.setdefault("GROQ_API_KEY", "test-key-for-ci")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret")

# Add backend root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Shared FastAPI test client for the session."""
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="session")
def auth_token(client: TestClient) -> str:
    """Get a valid JWT token for authenticated tests."""
    response = client.post("/api/auth/login", json={
        "username": "user",
        "password": "password"
    })
    if response.status_code == 200:
        return response.json()["access_token"]
    return "test-token"


@pytest.fixture(scope="session")
def auth_headers(auth_token: str) -> dict:
    """Return authorization headers for authenticated requests."""
    return {"Authorization": f"Bearer {auth_token}"}
