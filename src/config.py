"""
Configuration loader for the Research Agent.
Loads and validates required API keys from .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_groq_api_key() -> str:
    """Retrieve and validate the Groq API key."""
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found in .env file. Please set it.")
    return key


def get_tavily_api_key() -> str:
    """Retrieve and validate the Tavily API key."""
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        raise ValueError("TAVILY_API_KEY not found in .env file. Please set it.")
    return key


# --- Model Configuration ---
GROQ_MODEL_NAME = "llama-3.1-8b-instant"
AGENT_MAX_ITERATIONS = 3
