"""
Phase 1 Tests: Validate that Tavily and Wikipedia tools
return expected data and the raw output format is acceptable.
"""

import pytest
from src.tools import get_search_tool, get_wikipedia_tool


class TestTavilySearchTool:
    """Tests for the Tavily web search tool."""

    def test_tavily_returns_results(self):
        """Tavily should return a dict with 'results' and 'answer' keys."""
        tool = get_search_tool()
        response = tool.invoke("Impact of AI in Healthcare")
        assert response is not None
        assert isinstance(response, dict), f"Expected dict, got {type(response)}"
        assert "results" in response, f"Missing 'results' key. Keys: {response.keys()}"
        assert "answer" in response, f"Missing 'answer' key. Keys: {response.keys()}"
        print(f"\n--- Tavily Answer ---")
        print(response["answer"])
        print(f"\n--- Tavily Results ({len(response['results'])} items) ---")
        for i, result in enumerate(response["results"]):
            print(f"\nResult {i + 1}: {result.get('title', 'N/A')}")
            print(f"  URL: {result.get('url', 'N/A')}")
            print(f"  Content: {str(result.get('content', ''))[:200]}...")

    def test_tavily_result_has_content(self):
        """Each Tavily result item should contain 'content' and 'url' fields."""
        tool = get_search_tool()
        response = tool.invoke("Renewable energy trends 2025")
        assert isinstance(response, dict)
        results = response.get("results", [])
        assert len(results) > 0, "No results returned"
        for result in results:
            assert "content" in result, f"Missing 'content' key in result: {result}"
            assert "url" in result, f"Missing 'url' key in result: {result}"



class TestWikipediaTool:
    """Tests for the Wikipedia lookup tool."""

    def test_wikipedia_returns_content(self):
        """Wikipedia should return a non-empty string for a valid query."""
        tool = get_wikipedia_tool()
        result = tool.invoke("Artificial Intelligence")
        assert result is not None
        assert len(result) > 0
        print(f"\n--- Wikipedia Raw Output ({len(result)} chars) ---")
        print(result[:500])  # Print first 500 chars

    def test_wikipedia_respects_char_limit(self):
        """Wikipedia output should respect the 2000 char limit per article."""
        tool = get_wikipedia_tool()
        result = tool.invoke("Machine Learning")
        # With top_k_results=2and 2000 chars each, max is ~4000 + headers
        assert len(result) < 6000, f"Output too long: {len(result)} chars"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
