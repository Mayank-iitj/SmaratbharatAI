"""Comprehensive pytest test suite for SmartBharat AI API endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Health endpoints
# ---------------------------------------------------------------------------
class TestHealthEndpoints:
    def test_root_returns_welcome(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_health_check_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# Schemes endpoints
# ---------------------------------------------------------------------------
class TestSchemesEndpoints:
    def test_list_schemes_returns_list(self):
        response = client.get("/api/schemes/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_scheme_has_required_fields(self):
        response = client.get("/api/schemes/")
        scheme = response.json()[0]
        assert "id" in scheme
        assert "name" in scheme
        assert "description" in scheme
        assert "eligibility_criteria" in scheme
        assert "official_link" in scheme

    def test_get_scheme_by_id(self):
        response = client.get("/api/schemes/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_get_scheme_not_found(self):
        response = client.get("/api/schemes/99999")
        assert response.status_code == 404

    def test_filter_schemes_by_category(self):
        response = client.get("/api/schemes/?category=Agriculture")
        assert response.status_code == 200
        schemes = response.json()
        for scheme in schemes:
            assert scheme["category"].lower() == "agriculture"


# ---------------------------------------------------------------------------
# Complaints endpoints
# ---------------------------------------------------------------------------
class TestComplaintsEndpoints:
    def test_submit_valid_complaint(self):
        response = client.post("/api/complaints/", json={
            "category": "Pothole",
            "description": "Large pothole on the main road causing accidents",
            "location": "MG Road, Bangalore",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "complaint_id" in data

    def test_submit_complaint_invalid_category(self):
        response = client.post("/api/complaints/", json={
            "category": "InvalidCategory",
            "description": "Some description here",
            "location": "Somewhere",
        })
        assert response.status_code == 422

    def test_submit_complaint_description_too_short(self):
        response = client.post("/api/complaints/", json={
            "category": "Pothole",
            "description": "Short",
            "location": "Somewhere",
        })
        assert response.status_code == 422

    def test_track_complaint_valid_id(self):
        response = client.get("/api/complaints/101")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "complaint_id" in data

    def test_track_complaint_invalid_id(self):
        response = client.get("/api/complaints/-1")
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# Chat endpoint
# ---------------------------------------------------------------------------
class TestChatEndpoint:
    @patch("agents.router.process_chat")
    def test_chat_companion_route(self, mock_process):
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

    def test_chat_empty_message_rejected(self):
        response = client.post("/api/chat", json={
            "message": "",
            "user_id": "user_123",
        })
        assert response.status_code == 422

    def test_chat_message_too_long_rejected(self):
        response = client.post("/api/chat", json={
            "message": "x" * 2001,
            "user_id": "user_123",
        })
        assert response.status_code == 422

    def test_chat_missing_user_id_rejected(self):
        response = client.post("/api/chat", json={
            "message": "Hello",
        })
        assert response.status_code == 422
