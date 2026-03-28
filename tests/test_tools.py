"""
Phase 1 Tests: Validate that Tavily and Wikipedia tools
return expected data and the raw output format is acceptable.
"""

import pytest
from src.tools import web_search, wikipedia


class TestTavilySearchTool:
    """Tests for the Tavily web search tool."""

    def test_tavily_returns_results(self):
        """Tavily should return a non-empty string with search results."""
        result = web_search.invoke("Impact of AI in Healthcare")
        assert result is not None
        assert len(result) > 50, f"Result too short: {len(result)} chars"
        assert len(result) <= 2000, f"Result exceeds 2000 char limit: {len(result)} chars"
        print(f"\n--- Web Search Output ({len(result)} chars) ---")
        print(result)

    def test_tavily_result_has_content(self):
        """Tavily result should contain source references."""
        result = web_search.invoke("Renewable energy trends 2025")
        assert "Source" in result, f"No 'Source' markers in result"
        print(f"\n--- Web Search Output ({len(result)} chars) ---")
        print(result[:500])


class TestWikipediaTool:
    """Tests for the Wikipedia lookup tool."""

    def test_wikipedia_returns_content(self):
        """Wikipedia should return a non-empty string for a valid query."""
        result = wikipedia.invoke("Artificial Intelligence")
        assert result is not None
        assert len(result) > 0
        print(f"\n--- Wikipedia Raw Output ({len(result)} chars) ---")
        print(result[:500])

    def test_wikipedia_respects_char_limit(self):
        """Wikipedia output should be truncated to 2000 chars."""
        result = wikipedia.invoke("Machine Learning")
        assert len(result) <= 2000, f"Output too long: {len(result)} chars"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
