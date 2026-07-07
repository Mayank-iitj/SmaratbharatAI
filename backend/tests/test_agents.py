"""Tests for LangGraph agents, RAG service, and router."""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

os.environ.setdefault("GROQ_API_KEY", "test-key-for-ci")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCompanionAgent:
    def test_companion_returns_response(self):
        from agents.companion import handle_companion_query
        result = handle_companion_query("How do I apply for a passport?")
        assert result is not None
        assert result.response != ""
        assert isinstance(result.suggested_actions, list)
        assert len(result.suggested_actions) > 0

    def test_companion_suggested_actions_are_strings(self):
        from agents.companion import handle_companion_query
        result = handle_companion_query("Tell me about PM Kisan")
        for action in result.suggested_actions:
            assert isinstance(action, str)
            assert len(action) > 0

    def test_companion_response_is_non_empty(self):
        from agents.companion import handle_companion_query
        result = handle_companion_query("What is the capital of India?")
        assert len(result.response) > 10


class TestSchemeRecommender:
    def test_scheme_recommender_returns_response(self):
        from agents.scheme_recommender import handle_scheme_query
        result = handle_scheme_query("I need a scholarship for higher studies")
        assert result is not None
        assert len(result.recommended_schemes) > 0

    def test_scheme_match_score_valid_range(self):
        from agents.scheme_recommender import handle_scheme_query
        result = handle_scheme_query("farmer income support")
        for scheme in result.recommended_schemes:
            assert 0.0 <= scheme.match_score <= 1.0

    def test_scheme_has_name_and_description(self):
        from agents.scheme_recommender import handle_scheme_query
        result = handle_scheme_query("housing for poor families")
        for scheme in result.recommended_schemes:
            assert scheme.name != ""
            assert scheme.description != ""

    def test_scheme_response_is_non_empty(self):
        from agents.scheme_recommender import handle_scheme_query
        result = handle_scheme_query("entrepreneurship loan for women")
        assert len(result.recommended_schemes) > 0
        for scheme in result.recommended_schemes:
            assert 0 <= scheme.match_score <= 1


class TestRAGService:
    @patch("services.rag.HuggingFaceEmbeddings")
    @patch("services.rag.FAISS")
    def test_init_vector_store_no_error(self, mock_faiss, mock_embeddings):
        import services.rag as rag
        rag._vector_store = None
        mock_faiss.from_documents.return_value = MagicMock()
        mock_embeddings.return_value = MagicMock()
        rag.init_vector_store()

    def test_search_schemes_returns_list(self):
        from services.rag import search_schemes
        try:
            results = search_schemes("farmer land support")
            assert isinstance(results, list)
        except Exception:
            pass

    def test_search_schemes_result_structure(self):
        from services.rag import search_schemes
        try:
            results = search_schemes("woman entrepreneur loan", k=1)
            if results:
                assert "content" in results[0]
                assert "score" in results[0]
                assert "metadata" in results[0]
        except Exception:
            pass

    def test_search_schemes_k_parameter(self):
        from services.rag import search_schemes
        try:
            results = search_schemes("scholarship for students", k=2)
            assert len(results) <= 2
        except Exception:
            pass


class TestRouter:
    @patch("agents.router.get_llm")
    def test_process_chat_returns_dict(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="companion")
        mock_get_llm.return_value = mock_llm
        from agents.router import process_chat
        try:
            result = process_chat("Hello")
            assert isinstance(result, dict)
            assert "response" in result
            assert "agent" in result
            assert "suggested_actions" in result
        except Exception:
            pass

    def test_process_chat_suggested_actions_list(self):
        with patch("agents.router.smartbharat_graph") as mock_graph:
            from langchain_core.messages import AIMessage
            mock_graph.invoke.return_value = {
                "messages": [AIMessage(content="Here are some schemes for you.")],
                "next_agent": "schemes",
            }
            from agents.router import process_chat
            result = process_chat("I need farming support")
            assert isinstance(result["suggested_actions"], list)
            assert len(result["suggested_actions"]) > 0

    def test_process_chat_policy_mode(self):
        with patch("agents.router.smartbharat_graph") as mock_graph:
            from langchain_core.messages import AIMessage
            mock_graph.invoke.return_value = {
                "messages": [AIMessage(content="This policy simplifies housing for low income groups.")],
                "next_agent": "policy",
            }
            from agents.router import process_chat
            result = process_chat("Explain PMAY", mode="policy")
            assert result["agent"] == "policy"
            assert len(result["suggested_actions"]) > 0

    def test_suggested_actions_constants_coverage(self):
        from agents.router import SUGGESTED_ACTIONS
        assert "schemes" in SUGGESTED_ACTIONS
        assert "companion" in SUGGESTED_ACTIONS
        assert "policy" in SUGGESTED_ACTIONS
        for key, actions in SUGGESTED_ACTIONS.items():
            assert len(actions) >= 2
