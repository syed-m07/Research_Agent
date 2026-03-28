"""
Report Generator Module.
Takes raw research notes from the agent and uses an LLM
to format them into a highly structured, 7-part Markdown report.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_groq_api_key, GROQ_MODEL_NAME

REPORT_PROMPT = """You are an expert technical writer and research analyst. 
Your task is to take the provided raw research notes and generate a polished, highly structured Markdown report.

Topic: {topic}

The report MUST explicitly include the following 7 sections in exactly this order:
1. Cover Page (Include a nice text-based cover block with topic, generated date, and context)
2. Title
3. Introduction
4. Key Findings
5. Challenges
6. Future Scope
7. References (CRITICAL: You MUST extract the exact Source URLs and Titles from the RAW RESEARCH NOTES. DO NOT hallucinate [Author] or [Year] if they are not explicitly in the notes. Just list the Title and the URL.)

Format the output strictly as Markdown. Do not include conversational filler like "Here is your report".

RAW RESEARCH NOTES:
{raw_notes}

Write the complete Markdown report below:
"""

def generate_report(topic: str, raw_notes: str) -> str:
    """
    Generates a structured markdown report from raw research notes.
    
    Args:
        topic: The original research topic.
        raw_notes: The raw findings returned by the ReAct agent.
        
    Returns:
        The final formatted markdown report string.
    """
    llm = ChatGroq(
        api_key=get_groq_api_key(),
        model_name=GROQ_MODEL_NAME,
        temperature=0.3, # slightly higher temp for writing/formatting a report
        max_tokens=2048, # ensure we don't blow up TPM limits (8b instant has 6k limit)
    )
    
    prompt = ChatPromptTemplate.from_template(REPORT_PROMPT)
    chain = prompt | llm
    
    print("\n📝 writing final structured report...")
    result = chain.invoke({"topic": topic, "raw_notes": raw_notes})
    
    return result.content
