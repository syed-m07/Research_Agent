"""
ReAct Agent for the Research Agent.
Initializes a LangChain agent with Groq LLM, search tools,
and strict guardrails for research quality and latency control.
"""

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from src.config import get_groq_api_key, GROQ_MODEL_NAME, AGENT_MAX_ITERATIONS
from src.tools import get_all_tools
from src.callbacks import ResearchAgentCallbackHandler


# --- System Prompt for the Research Agent ---
SYSTEM_PROMPT = """You are a thorough and efficient research agent. Your job is to research a given topic
and gather comprehensive, factual information from multiple sources.

STRICT RULES:
1. ONLY use information retrieved from the tools. NEVER fabricate or hallucinate facts.
2. Use the web_search tool for current data, statistics, recent developments, and expert opinions.
3. Use the wikipedia tool for foundational background, definitions, and historical context.
4. You MUST use BOTH tools at least once to get a well-rounded perspective.
5. After gathering sufficient information from both sources, STOP searching and synthesize your findings.
6. Be efficient — do not repeat searches for information you already have.

When you have gathered enough information, provide ALL findings organized as raw research notes. Include:
- Key facts and statistics
- Recent developments and trends
- Background context
- Challenges and concerns
- Expert opinions
- Future outlook

Do NOT format as a final report — just provide organized raw notes for the report generator."""


def create_research_agent():
    """
    Creates and returns a fully configured research agent
    with Groq LLM, search tools, and visibility callbacks.
    """
    # Initialize the Groq LLM
    llm = ChatGroq(
        api_key=get_groq_api_key(),
        model_name=GROQ_MODEL_NAME,
        temperature=0.1,  # Low temp for factual research
        max_tokens=1024,  # Reduced from 4096 to prevent hitting Groq TPM limits
    )

    # Get search tools
    tools = get_all_tools()

    # Create the agent using LangChain's new create_agent API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent


def run_agent(topic: str) -> dict:
    """
    Runs the research agent on a given topic.

    Args:
        topic: The research topic to investigate.

    Returns:
        A dict with the agent's final response and message history.
    """
    agent = create_research_agent()
    callbacks = [ResearchAgentCallbackHandler()]

    print(f"\n{'='*60}")
    print(f"  RESEARCHING: {topic}")
    print(f"{'='*60}")

    # Invoke the agent with the topic
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Research the following topic thoroughly: {topic}"}]},
        config={
            "callbacks": callbacks,
            "recursion_limit": AGENT_MAX_ITERATIONS * 2 + 1,  # Each iteration = 2 graph steps + 1
        },
    )

    # Extract the final AI message content
    messages = result.get("messages", [])
    final_output = ""
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_calls"):
            final_output = msg.content
            break

    return {"output": final_output, "messages": messages}
