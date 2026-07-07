"""LangGraph agent router for SmartBharat AI.

Routes user messages to the appropriate sub-agent:
- companion: General civic Q&A
- schemes: RAG-powered scheme discovery
- policy: Policy document simplification
"""
import logging
import os
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Suggested actions by agent type
SUGGESTED_ACTIONS: dict[str, list[str]] = {
    "schemes": [
        "Check my eligibility",
        "How to apply for PM Kisan",
        "Find housing schemes",
        "Student scholarship options",
    ],
    "companion": [
        "Find schemes for farmers",
        "Report a pothole",
        "Explain PMAY scheme",
        "Help with Aadhaar",
    ],
    "policy": [
        "Explain in Hindi",
        "What documents do I need?",
        "Who is eligible?",
        "Key benefits summary",
    ],
}


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
class AgentState(TypedDict):
    """LangGraph state for the SmartBharat AI workflow."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_agent: str


# ---------------------------------------------------------------------------
# LLM factory
# ---------------------------------------------------------------------------
def get_llm(model: str = GROQ_MODEL) -> ChatGroq:
    """Return a ChatGroq LLM instance.

    Args:
        model: Groq model identifier to use.

    Returns:
        Configured ChatGroq instance.

    Raises:
        ValueError: If GROQ_API_KEY is not set.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    return ChatGroq(model=model, groq_api_key=api_key, temperature=0.3, max_tokens=512)


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------
def router_node(state: AgentState) -> dict:
    """Route user message to the appropriate sub-agent.

    Determines intent from the last user message and sets ``next_agent``
    to one of: ``companion``, ``schemes``, or ``policy``.
    """
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""

    prompt = (
        "You are a routing agent for SmartBharat AI, India's civic AI system.\n"
        "Classify the user's intent:\n"
        "- 'schemes' → asking about government schemes, subsidies, loans, or financial aid\n"
        "- 'policy' → asking to explain, summarize, or simplify a government policy/circular\n"
        "- 'companion' → everything else (complaints, navigation, general Q&A)\n\n"
        f"User message: {last_message}\n\n"
        "Respond with EXACTLY one word: schemes, policy, or companion."
    )

    try:
        llm = get_llm()
        response = llm.invoke([HumanMessage(content=prompt)])
        decision = response.content.strip().lower()
        if "schemes" in decision:
            return {"next_agent": "schemes"}
        elif "policy" in decision:
            return {"next_agent": "policy"}
        else:
            return {"next_agent": "companion"}
    except Exception as exc:
        logger.warning("Router node failed, defaulting to companion: %s", exc)
        return {"next_agent": "companion"}


def companion_node(state: AgentState) -> dict:
    """Handle general civic Q&A via the Civic Companion.

    Answers questions about Indian government services, complaints,
    document requirements, and general civic navigation.
    """
    messages = state["messages"]
    system = SystemMessage(
        content=(
            "You are the SmartBharat AI Civic Companion — India's first AI civic assistant. "
            "You help Indian citizens navigate government services, understand their rights, "
            "file complaints, and access public services. "
            "Be empathetic, clear, and accurate. Use Markdown formatting. "
            "Always cite relevant government portals (e.g., india.gov.in) when applicable. "
            "Keep responses under 180 words."
        )
    )
    try:
        llm = get_llm()
        response = llm.invoke([system] + list(messages[-6:]))
        return {"messages": [response]}
    except Exception as exc:
        logger.error("Companion node error: %s", exc)
        return {"messages": [AIMessage(content="Sorry, I'm having trouble connecting. Please try again.")]}


def scheme_node(state: AgentState) -> dict:
    """Recommend government schemes using RAG retrieval.

    Retrieves semantically similar scheme documents from the vector store
    and uses the LLM to generate personalized recommendations.
    """
    from services.rag import search_schemes

    messages = state["messages"]
    last_message = messages[-1].content

    try:
        results = search_schemes(last_message, k=4)
        context = "\n".join([
            f"- **{r['metadata'].get('id', 'Scheme')}**: {r['content']}"
            for r in results
        ])
    except Exception as exc:
        logger.warning("RAG search failed: %s", exc)
        context = ""

    system = SystemMessage(
        content=(
            "You are the SmartBharat AI Scheme Recommender. "
            "Based on retrieved scheme documents, recommend the most relevant government schemes. "
            "Explain eligibility criteria, key benefits, and how to apply. "
            "Include official links where possible. Keep responses under 220 words.\n\n"
            f"Retrieved Schemes:\n{context or 'No specific schemes found — suggest general categories.'}"
        )
    )
    try:
        llm = get_llm()
        response = llm.invoke([system, HumanMessage(content=last_message)])
        return {"messages": [response]}
    except Exception as exc:
        logger.error("Scheme node error: %s", exc)
        return {"messages": [AIMessage(content="Sorry, I couldn't retrieve schemes right now.")]}


def policy_node(state: AgentState) -> dict:
    """Simplify complex government policies and circulars.

    Takes complex policy language and translates it into plain English
    that any citizen can understand.
    """
    messages = state["messages"]
    system = SystemMessage(
        content=(
            "You are the SmartBharat Policy Simplifier. "
            "Your job is to take complex government policies, circulars, and legal documents "
            "and explain them in simple, plain English that any Indian citizen can understand. "
            "Break down jargon, highlight key points, explain who it affects and how. "
            "Structure your response with: Summary, Key Points, Who is Affected, Action Required. "
            "Keep responses under 250 words."
        )
    )
    try:
        llm = get_llm()
        response = llm.invoke([system] + list(messages[-4:]))
        return {"messages": [response]}
    except Exception as exc:
        logger.error("Policy node error: %s", exc)
        return {"messages": [AIMessage(content="Sorry, I couldn't simplify this policy right now.")]}


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------
def _route_decision(state: AgentState) -> str:
    """Extract routing decision from state."""
    return state.get("next_agent", "companion")


builder = StateGraph(AgentState)
builder.add_node("router", router_node)
builder.add_node("companion", companion_node)
builder.add_node("schemes", scheme_node)
builder.add_node("policy", policy_node)

builder.add_edge(START, "router")
builder.add_conditional_edges("router", _route_decision, {
    "companion": "companion",
    "schemes": "schemes",
    "policy": "policy",
})
builder.add_edge("companion", END)
builder.add_edge("schemes", END)
builder.add_edge("policy", END)

smartbharat_graph = builder.compile()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def process_chat(user_message: str, mode: str = "general") -> dict:
    """Process a user chat message through the LangGraph agent workflow.

    Args:
        user_message: The user's message text.
        mode: Optional mode override — 'general', 'schemes', or 'policy'.

    Returns:
        Dict with keys: response (str), agent (str), suggested_actions (list[str]).
    """
    initial_state: AgentState = {
        "messages": [HumanMessage(content=user_message)],
        "next_agent": mode if mode in ("schemes", "policy") else "companion",
    }

    try:
        final_state = smartbharat_graph.invoke(initial_state)
        agent = final_state.get("next_agent", "companion")
        last_message = final_state["messages"][-1].content
    except Exception as exc:
        logger.error("Graph invocation failed: %s", exc, exc_info=True)
        agent = "companion"
        last_message = "I'm having trouble connecting to the AI service. Please try again."

    return {
        "response": last_message,
        "agent": agent,
        "suggested_actions": SUGGESTED_ACTIONS.get(agent, SUGGESTED_ACTIONS["companion"]),
    }
