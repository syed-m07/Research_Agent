"""
Tool definitions for the Research Agent.
Provides Tavily Web Search and Wikipedia lookup tools.
"""

from langchain_tavily import TavilySearch
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from src.config import get_tavily_api_key


def get_search_tool() -> TavilySearch:
    """
    Initializes the Tavily web search tool.
    Returns top 5 results with content snippets.
    """
    # Ensure the API key is set in the environment before initializing
    get_tavily_api_key()

    search_tool = TavilySearch(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        name="web_search",
        description=(
            "Search the web for current, relevant information on a topic. "
            "Use this tool when you need recent data, statistics, news, or expert opinions."
        ),
    )
    return search_tool


def get_wikipedia_tool() -> WikipediaQueryRun:
    """
    Initializes the Wikipedia lookup tool.
    Returns summarized content from Wikipedia articles (max 2000 chars to save tokens).
    """
    api_wrapper = WikipediaAPIWrapper(
        top_k_results=2,
        doc_content_chars_max=2000,
    )
    wiki_tool = WikipediaQueryRun(
        api_wrapper=api_wrapper,
        name="wikipedia",
        description=(
            "Look up background information, definitions, and historical context from Wikipedia. "
            "Use this tool when you need foundational knowledge or encyclopedic context on a topic."
        ),
    )
    return wiki_tool


def get_all_tools() -> list:
    """Returns a list of all available tools for the agent."""
    return [get_search_tool(), get_wikipedia_tool()]
