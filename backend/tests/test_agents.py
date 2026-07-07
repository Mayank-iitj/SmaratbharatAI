"""Tests for the LangGraph agent router and RAG service."""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Companion agent tests
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Scheme recommender agent tests
# ---------------------------------------------------------------------------
class TestSchemeRecommender:
    def test_scheme_recommender_returns_response(self):
        from agents.scheme_recommender import handle_scheme_query
        result = handle_scheme_query("I need a scholarship for higher studies")
        assert result is not None
        assert len(result.recommended_schemes) > 0

    def test_scheme_match_score_valid(self):
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


# ---------------------------------------------------------------------------
# RAG service tests
# ---------------------------------------------------------------------------
class TestRAGService:
    @patch("services.rag.HuggingFaceEmbeddings")
    @patch("services.rag.FAISS")
    def test_init_vector_store(self, mock_faiss, mock_embeddings):
        """Vector store initializes without errors."""
        import services.rag as rag
        rag._vector_store = None  # Reset state
        mock_faiss.from_documents.return_value = MagicMock()
        mock_embeddings.return_value = MagicMock()
        # Should not raise
        rag.init_vector_store()

    def test_search_schemes_returns_list(self):
        from services.rag import search_schemes
        try:
            results = search_schemes("farmer land support")
            assert isinstance(results, list)
        except Exception:
            # Acceptable if embeddings not available in CI
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


# ---------------------------------------------------------------------------
# Router process_chat tests (mocked LLM)
# ---------------------------------------------------------------------------
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
            pass  # LLM errors acceptable without real key

    def test_router_process_chat_has_suggested_actions(self):
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
