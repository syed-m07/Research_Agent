"""
Phase 3 Tests: Validate that the Report Generator correctly
synthesizes raw notes into the required 7-part Markdown structure.
"""

import os
import pytest
from src.report_generator import generate_report

# Mock raw notes to avoid calling the full ReAct agent during the report test
RAW_NOTES_MOCK = """
Summary: Quantum computing utilizes quantum mechanics to solve complex problems faster than classical computers.
Key Facts:
- It relies on qubits, superposition, and entanglement.
- Current machines are in the NISQ (Noisy Intermediate-Scale Quantum) era.
- Major challenges include decoherence and error correction.
- Potential applications include cryptography, drug discovery, and optimization.

Source 1: IBM Quantum
URL: https://www.ibm.com/quantum
IBM is building superconducting quantum processors.

Source 2: Quantum Computing - Wikipedia
URL: https://en.wikipedia.org/wiki/Quantum_computing
Quantum computing is a rapidly-emerging technology.
"""

class TestReportGenerator:
    """Tests for the final report generation module."""

    def test_report_contains_all_sections(self):
        """The generated report MUST contain the 7 mandatory sections."""
        report = generate_report("Quantum Computing Overview", RAW_NOTES_MOCK)
        
        # Check that it's a non-empty string
        assert report is not None
        assert len(report) > 500, "Report is too short"
        
        # Verify all 7 required sections are present in the output
        required_sections = [
            "Cover Page",
            "Title",
            "Introduction",
            "Key Findings",
            "Challenges",
            "Future Scope",
            "References"
        ]
        
        report_lower = report.lower()
        for section in required_sections:
            assert section.lower() in report_lower, f"Missing required section: {section}"
            
        print(f"\\n--- Generated Report length: {len(report)} chars ---")
        print("All required sections found! ✅")
        

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
