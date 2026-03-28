"""
Main execution script for the Autonomous Research Agent.
Combines the ReAct search agent and the Report Generator into a single pipeline.
"""

import argparse
from src.agent import run_agent
from src.report_generator import generate_report

def main():
    parser = argparse.ArgumentParser(description="Autonomous AI Research Agent")
    parser.add_argument(
        "topic", 
        type=str, 
        help="The topic for the AI to research"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        help="Path to save the generated markdown report", 
        default="research_report.md"
    )
    
    args = parser.parse_args()
    
    print(f"\n🚀 Starting Autonomous Research on: '{args.topic}'\n{'-'*60}")
    
    # Step 1: ReAct Agent gathers facts
    agent_result = run_agent(args.topic)
    raw_notes = agent_result["output"]
    
    # Step 2: Report Generator synthesizes the final markdown
    final_report = generate_report(args.topic, raw_notes)
    
    # Save the report to disk
    with open(args.output, "w", encoding="utf-8") as file:
        file.write(final_report)
        
    print(f"\n✅ Success! Final structured report written to: {args.output}\n")

if __name__ == "__main__":
    main()
