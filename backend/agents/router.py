import os
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

# Define the State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_agent: str

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("WARNING: GROQ_API_KEY not set!")
    return ChatGroq(model="llama3-70b-8192", groq_api_key=api_key)

# 1. The Router Node
def router_node(state: AgentState):
    """Decides whether to route to the Companion or the Scheme Recommender."""
    llm = get_llm()
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""
    
    prompt = f"""
    You are a routing agent for SmartBharat AI.
    Determine if the user's message is asking about finding or applying for government schemes, or financial help.
    If yes, respond with EXACTLY the word "schemes".
    Otherwise, respond with EXACTLY the word "companion".
    
    User message: {last_message}
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        decision = response.content.strip().lower()
        if "schemes" in decision:
            return {"next_agent": "schemes"}
        else:
            return {"next_agent": "companion"}
    except Exception as e:
        print(f"Router Error: {e}")
        return {"next_agent": "companion"}

# 2. The Companion Node
def companion_node(state: AgentState):
    """Handles general civic Q&A."""
    llm = get_llm()
    messages = state["messages"]
    
    system_prompt = SystemMessage(content="You are the SmartBharat AI Civic Companion. Answer clearly, concisely, and accurately based on Indian government policies. Use Markdown formatting. Keep responses under 150 words.")
    
    # We pass the history up to 5 messages
    call_messages = [system_prompt] + list(messages[-5:])
    
    try:
        response = llm.invoke(call_messages)
        return {"messages": [response]}
    except Exception as e:
        print(f"Companion Error: {e}")
        return {"messages": [AIMessage(content="Sorry, I am having trouble connecting to the AI service.")]}

# 3. The Scheme Recommender Node
def scheme_node(state: AgentState):
    """Uses RAG to recommend schemes."""
    from services.rag import search_schemes
    
    llm = get_llm()
    messages = state["messages"]
    last_message = messages[-1].content
    
    # 1. Retrieve schemes
    results = search_schemes(last_message)
    context = "\n".join([f"- **{r['metadata'].get('id', 'N/A')}**: {r['content']}" for r in results])
    
    system_prompt = SystemMessage(content="You are the SmartBharat AI Scheme Recommender. Recommend schemes based on the retrieved context below. Explain why they match and the benefits. Keep it under 200 words.\n\nContext:\n" + context)
    
    try:
        response = llm.invoke([system_prompt, HumanMessage(content=last_message)])
        return {"messages": [response]}
    except Exception as e:
        print(f"Scheme Error: {e}")
        return {"messages": [AIMessage(content="Sorry, I couldn't fetch the schemes right now.")]}


# Build the Graph
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("companion", companion_node)
builder.add_node("schemes", scheme_node)

builder.add_edge(START, "router")

def route_decision(state: AgentState):
    return state.get("next_agent", "companion")

builder.add_conditional_edges("router", route_decision, {
    "companion": "companion",
    "schemes": "schemes"
})

builder.add_edge("companion", END)
builder.add_edge("schemes", END)

# Compile the graph
smartbharat_graph = builder.compile()

def process_chat(user_message: str):
    """Entry point to process a chat message."""
    initial_state = {"messages": [HumanMessage(content=user_message)]}
    final_state = smartbharat_graph.invoke(initial_state)
    agent = final_state.get("next_agent", "companion")
    
    if agent == "schemes":
        suggested_actions = ["Check my eligibility", "How to apply", "Find agricultural schemes"]
    else:
        suggested_actions = ["Find schemes", "Report a pothole", "Explain PMAY"]
        
    return {
        "response": final_state["messages"][-1].content,
        "agent": agent,
        "suggested_actions": suggested_actions
    }
