"""
Tool definitions for the Research Agent.
Provides truncated Tavily Web Search and Wikipedia lookup tools
to stay within Groq's free-tier TPM limits.
"""

import json
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from src.config import get_tavily_api_key

# Max characters per tool response to keep LLM context manageable
MAX_TOOL_OUTPUT_CHARS = 2000


@tool
def web_search(query: str) -> str:
    """Search the web for current, relevant information on a topic.
    Use this tool when you need recent data, statistics, news, or expert opinions."""
    get_tavily_api_key()

    search = TavilySearch(
        max_results=3,
        search_depth="basic",
        include_answer=True,
    )
    raw_result = search.invoke(query)

    # Extract and format the key parts concisely
    output_parts = []

    if isinstance(raw_result, dict):
        # Add the pre-built answer
        if raw_result.get("answer"):
            output_parts.append(f"Summary: {raw_result['answer']}")

        # Add individual results (title + truncated content)
        results = raw_result.get("results", [])
        for i, r in enumerate(results[:3], 1):
            title = r.get("title", "N/A")
            content = r.get("content", "")[:400]
            url = r.get("url", "")
            output_parts.append(f"\nSource {i}: {title}\nURL: {url}\n{content}")
    else:
        output_parts.append(str(raw_result)[:MAX_TOOL_OUTPUT_CHARS])

    result = "\n".join(output_parts)
    return result[:MAX_TOOL_OUTPUT_CHARS]


@tool
def wikipedia(query: str) -> str:
    """Look up background information, definitions, and historical context from Wikipedia.
    Use this tool when you need foundational knowledge or encyclopedic context on a topic."""
    api_wrapper = WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=1500,
    )
    wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    result = wiki_tool.invoke(query)
    return result[:MAX_TOOL_OUTPUT_CHARS]


def get_all_tools() -> list:
    """Returns a list of all available tools for the agent."""
    return [web_search, wikipedia]
