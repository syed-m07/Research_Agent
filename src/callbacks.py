"""
Custom LangChain callbacks for agent visibility.
Prints user-friendly status messages as the agent thinks and acts.
"""

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
from typing import Any, Dict, List, Optional


class ResearchAgentCallbackHandler(BaseCallbackHandler):
    """
    Callback handler that prints human-readable status messages
    as the ReAct agent progresses through its reasoning loop.
    """

    def __init__(self):
        self.step_count = 0

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        """Called when a tool starts running."""
        self.step_count += 1
        tool_name = serialized.get("name", "unknown_tool")

        if tool_name == "web_search":
            print(f"\n🔍 [{self.step_count}] crawling relevant websites for information...")
        elif tool_name == "wikipedia":
            print(f"\n📚 [{self.step_count}] extracting background knowledge from wikipedia...")
        else:
            print(f"\n⚙️  [{self.step_count}] using {tool_name}...")

        print(f"   query: {input_str}")

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Called when the agent completes its reasoning."""
        print(f"\n✅ done — agent finished in {self.step_count} step(s).")

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Called when the LLM starts generating."""
        if self.step_count == 0:
            print("\n🧠 thinking about the problem statement...")
        else:
            print(f"\n💭 analyzing findings and deciding next step...")

    def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
        """Called when a tool errors out."""
        print(f"\n❌ tool error: {error}")
