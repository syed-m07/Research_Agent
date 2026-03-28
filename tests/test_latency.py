"""
Phase 4 Tests: Latency validation.
Ensures that the entire autonomous research and reporting pipeline
completes within the strict 60-second requirement.
"""

import time
import pytest
from src.agent import run_agent
from src.report_generator import generate_report

class TestEndToEndLatency:
    """Performance tests for the whole pipeline."""

    def test_pipeline_completes_under_60_seconds(self):
        """
        The agent must gather research and generate the final report
        in under 60 seconds total to meet the SLA requirement.
        """
        topic = "Recent advancements in Solid State Batteries"
        
        start_time = time.time()
        
        # 1. Run the agent to gather facts
        print(f"\\n⏱️ Starting latency test for topic: {topic}")
        agent_result = run_agent(topic)
        raw_notes = agent_result["output"]
        
        # 2. Generate the formatted report
        final_report = generate_report(topic, raw_notes)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\\n⏱️ Pipeline completed in: {duration:.2f} seconds")
        
        # Verify the latency requirement
        assert duration < 60.0, f"Latency Test Failed! Pipeline took {duration:.2f}s (Limit: 60s)"
        
        # Sanity check that it actually produced a report
        assert "Key Findings" in final_report

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
