"""
Phase 2 Tests: Validate that the ReAct agent initializes correctly,
runs on a topic, and produces output within latency limits.
"""

import time
import pytest
from src.agent import create_research_agent, run_agent


class TestAgentInitialization:
    """Tests for agent creation and configuration."""

    def test_agent_creates_successfully(self):
        """The agent should initialize without errors."""
        agent = create_research_agent()
        assert agent is not None


class TestAgentExecution:
    """Tests for running the agent end-to-end."""

    def test_agent_runs_and_returns_output(self):
        """The agent should return a result with 'output' key."""
        result = run_agent("Impact of AI in Healthcare")
        assert "output" in result, f"Missing 'output' key. Keys: {result.keys()}"
        assert len(result["output"]) > 100, (
            f"Output too short ({len(result['output'])} chars), agent may not have researched properly"
        )
        print(f"\n--- Agent Output ({len(result['output'])} chars) ---")
        print(result["output"][:800])

    def test_agent_completes_within_time_limit(self):
        """The agent should complete within 60 seconds."""
        start = time.time()
        result = run_agent("Renewable energy trends")
        duration = time.time() - start
        assert duration < 60, f"Agent took {duration:.1f}s — exceeds 60s limit"
        print(f"\n⏱️  Agent completed in {duration:.1f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
