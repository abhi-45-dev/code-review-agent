from typing import List, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq  import ChatGroq
load_dotenv()



class BugReport(BaseModel):
    issue: str = Field(
        description="Type of bug detected"
    )

    line_hint: str = Field(
        description="Line number or code snippet where the issue occurs"
    )

    severity: Literal["Low", "Medium", "High", "Critical"] = Field(
        description="Severity level of the issue"
    )

    explanation: str = Field(
        description="Explanation of the bug and suggested fix"
    )


class BugDetectionResult(BaseModel):
    findings: List[BugReport] = Field(
        default_factory=list,
        description="List of detected bugs"
    )


@tool
def bug_detector(code_chunk: str) -> dict:
    """
    Analyze a code chunk and return detected bugs.
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    structured_llm = llm.with_structured_output(
        BugDetectionResult
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert code reviewer.

Analyze the provided code and identify:
- Logic bugs
- Off-by-one errors
- Null/None handling issues
- Unhandled exceptions
- Edge-case failures
- Resource leaks
- Incorrect conditions

Return only structured output.
"""
            ),
            (
                "human",
                "Review this code:\n\n{code}"
            )
        ]
    )

    chain = prompt | structured_llm

    result = chain.invoke(
        {
            "code": code_chunk
        }
    )

    return result.model_dump()
