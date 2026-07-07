import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from agents.router import process_chat

def test_routing():
    print("Testing LangGraph Agent with general query...")
    try:
        res = process_chat("Hello, what services can you help me with?")
        print("Response received successfully!")
        print(f"Agent matched: {res['agent']}")
        print(f"Response: {res['response']}")
        print(f"Suggested Actions: {res['suggested_actions']}")
    except Exception as e:
        print(f"Error occurred: {e}")

    print("\nTesting LangGraph Agent with schemes query...")
    try:
        res = process_chat("I need a loan to set up a new greenfield enterprise.")
        print("Response received successfully!")
        print(f"Agent matched: {res['agent']}")
        print(f"Response: {res['response']}")
        print(f"Suggested Actions: {res['suggested_actions']}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY is not set in env. Please set it to run the verification.")
    test_routing()
