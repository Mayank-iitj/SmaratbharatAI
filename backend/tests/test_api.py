"""Comprehensive pytest test suite for SmartBharat AI API endpoints."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Health endpoints
# ---------------------------------------------------------------------------
class TestHealthEndpoints:
    def test_root_returns_welcome(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check_returns_ok(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_health_includes_service_name(self, client: TestClient):
        response = client.get("/health")
        assert "service" in response.json()


# ---------------------------------------------------------------------------
# Schemes endpoints
# ---------------------------------------------------------------------------
class TestSchemesEndpoints:
    def test_list_schemes_returns_list(self, client: TestClient):
        response = client.get("/api/schemes/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_scheme_has_required_fields(self, client: TestClient):
        response = client.get("/api/schemes/")
        scheme = response.json()[0]
        assert "id" in scheme
        assert "name" in scheme
        assert "description" in scheme
        assert "eligibility_criteria" in scheme
        assert "official_link" in scheme
        assert "category" in scheme

    def test_get_scheme_by_id(self, client: TestClient):
        response = client.get("/api/schemes/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_get_scheme_not_found(self, client: TestClient):
        response = client.get("/api/schemes/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_filter_schemes_by_category(self, client: TestClient):
        response = client.get("/api/schemes/?category=Agriculture")
        assert response.status_code == 200
        schemes = response.json()
        for scheme in schemes:
            assert scheme["category"].lower() == "agriculture"

    def test_filter_schemes_empty_category(self, client: TestClient):
        response = client.get("/api/schemes/?category=NonExistentCategory")
        assert response.status_code == 200
        assert response.json() == []

    def test_schemes_official_links_are_urls(self, client: TestClient):
        response = client.get("/api/schemes/")
        for scheme in response.json():
            assert scheme["official_link"].startswith("http")


# ---------------------------------------------------------------------------
# Complaints endpoints
# ---------------------------------------------------------------------------
class TestComplaintsEndpoints:
    def test_submit_valid_complaint(self, client: TestClient):
        response = client.post("/api/complaints/", json={
            "category": "Pothole",
            "description": "Large pothole on the main road causing accidents to vehicles",
            "location": "MG Road, Bangalore, Karnataka",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "complaint_id" in data
        assert "message" in data

    def test_submit_complaint_invalid_category(self, client: TestClient):
        response = client.post("/api/complaints/", json={
            "category": "<script>alert(1)</script>",
            "description": "Injection attempt description",
            "location": "Somewhere",
        })
        assert response.status_code == 422

    def test_submit_complaint_description_too_short(self, client: TestClient):
        response = client.post("/api/complaints/", json={
            "category": "Pothole",
            "description": "Short",
            "location": "Somewhere",
        })
        assert response.status_code == 422

    def test_submit_complaint_description_too_long(self, client: TestClient):
        response = client.post("/api/complaints/", json={
            "category": "Pothole",
            "description": "x" * 1001,
            "location": "Somewhere",
        })
        assert response.status_code == 422

    def test_submit_all_valid_categories(self, client: TestClient):
        categories = ["Pothole", "Garbage", "Streetlight", "Water Leak", "Sewage"]
        for cat in categories:
            response = client.post("/api/complaints/", json={
                "category": cat,
                "description": "This is a detailed description of the civic issue in the area",
                "location": "Test Location, City, State",
            })
            assert response.status_code == 201, f"Category {cat} failed"

    def test_track_complaint_valid_id(self, client: TestClient):
        response = client.get("/api/complaints/101")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "complaint_id" in data
        assert "estimated_resolution" in data

    def test_track_complaint_invalid_id(self, client: TestClient):
        response = client.get("/api/complaints/-1")
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# Chat endpoint
# ---------------------------------------------------------------------------
class TestChatEndpoint:
    @patch("agents.router.process_chat")
    def test_chat_companion_route(self, mock_process, client: TestClient):
        mock_process.return_value = {
            "response": "I can help you with government services.",
            "agent": "companion",
            "suggested_actions": ["Find schemes", "File complaint"],
        }
        response = client.post("/api/chat", json={
            "message": "Hello, how are you?",
            "user_id": "user_123",
        })
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "agent" in data
        assert isinstance(data["suggested_actions"], list)
        assert "mode" in data

    @patch("agents.router.process_chat")
    def test_chat_policy_mode(self, mock_process, client: TestClient):
        mock_process.return_value = {
            "response": "This policy means citizens get housing subsidies.",
            "agent": "policy",
            "suggested_actions": ["Explain in Hindi", "Who is eligible?"],
        }
        response = client.post("/api/chat", json={
            "message": "Explain the PMAY policy",
            "user_id": "user_123",
            "mode": "policy",
        })
        assert response.status_code == 200
        assert response.json()["mode"] == "policy"

    def test_chat_empty_message_rejected(self, client: TestClient):
        response = client.post("/api/chat", json={
            "message": "",
            "user_id": "user_123",
        })
        assert response.status_code == 422

    def test_chat_whitespace_only_rejected(self, client: TestClient):
        response = client.post("/api/chat", json={
            "message": "   ",
            "user_id": "user_123",
        })
        assert response.status_code == 422

    def test_chat_message_too_long_rejected(self, client: TestClient):
        response = client.post("/api/chat", json={
            "message": "x" * 2001,
            "user_id": "user_123",
        })
        assert response.status_code == 422

    def test_chat_missing_user_id_rejected(self, client: TestClient):
        response = client.post("/api/chat", json={
            "message": "Hello",
        })
        assert response.status_code == 422

    def test_chat_invalid_mode_rejected(self, client: TestClient):
        response = client.post("/api/chat", json={
            "message": "Hello",
            "user_id": "user_123",
            "mode": "invalid_mode",
        })
        assert response.status_code == 422
