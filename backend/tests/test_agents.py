import pytest
from agents.companion import handle_companion_query
from agents.scheme_recommender import handle_scheme_query

def test_companion_agent():
    query = "How do I apply for a passport?"
    response = handle_companion_query(query)
    
    assert response is not None
    assert response.response != ""
    assert isinstance(response.suggested_actions, list)
    assert len(response.suggested_actions) > 0

def test_scheme_recommender_agent():
    query = "I need a scholarship for higher studies"
    response = handle_scheme_query(query)
    
    assert response is not None
    assert "scholarship" in query
    assert len(response.recommended_schemes) > 0
    assert response.recommended_schemes[0].match_score > 0
