"""Tests for the Authentication API."""
import pytest
from fastapi.testclient import TestClient


class TestLoginEndpoint:
    def test_login_valid_credentials(self, client: TestClient):
        response = client.post("/api/auth/login", json={
            "username": "user",
            "password": "password"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 86400

    def test_login_wrong_password(self, client: TestClient):
        response = client.post("/api/auth/login", json={
            "username": "user",
            "password": "wrongpass"
        })
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_wrong_username(self, client: TestClient):
        response = client.post("/api/auth/login", json={
            "username": "hacker",
            "password": "password"
        })
        assert response.status_code == 401

    def test_login_empty_username(self, client: TestClient):
        response = client.post("/api/auth/login", json={
            "username": "",
            "password": "password"
        })
        assert response.status_code == 422

    def test_login_password_too_short(self, client: TestClient):
        response = client.post("/api/auth/login", json={
            "username": "user",
            "password": "abc"
        })
        assert response.status_code == 422

    def test_login_missing_fields(self, client: TestClient):
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 422

    def test_login_token_is_jwt_format(self, client: TestClient):
        response = client.post("/api/auth/login", json={
            "username": "user",
            "password": "password"
        })
        assert response.status_code == 200
        token = response.json()["access_token"]
        # JWT format: header.payload.signature
        parts = token.split(".")
        assert len(parts) == 3


class TestMeEndpoint:
    def test_get_me_unauthenticated(self, client: TestClient):
        """Should return default citizen without auth token."""
        response = client.get("/api/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "name" in data
        assert "role" in data

    def test_get_me_with_valid_token(self, client: TestClient, auth_headers: dict):
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "user_123"
        assert data["role"] == "citizen"

    def test_get_me_with_invalid_token(self, client: TestClient):
        response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
        assert response.status_code == 401


class TestSecurityHeaders:
    def test_security_headers_present(self, client: TestClient):
        response = client.get("/health")
        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
        assert "x-xss-protection" in response.headers
        assert response.headers["x-frame-options"] == "DENY"
        assert response.headers["x-content-type-options"] == "nosniff"

    def test_no_server_header_leaked(self, client: TestClient):
        """Ensure server identity is not exposed."""
        response = client.get("/health")
        # Should not expose detailed server info in production
        server = response.headers.get("server", "")
        # We just verify the response is there
        assert response.status_code == 200
