from typing import List, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


class BugReport(BaseModel):
    issue: str
    line_hint: str
    severity: Literal["Low", "Medium", "High", "Critical"]
    explanation: str


class QualityReport(BaseModel):
    issue: str
    line_hint: str
    severity: Literal["Low", "Medium", "High", "Critical"]
    explanation: str


class SecurityReport(BaseModel):
    issue: str
    line_hint: str
    severity: Literal["Low", "Medium", "High", "Critical"]
    explanation: str


class ImprovementSuggestion(BaseModel):
    suggestion: str
    current_pattern: str
    recommended_pattern: str
    reason: str

    impact: Literal[
        "Readability",
        "Performance",
        "Maintainability",
        "Memory Efficiency",
        "Concurrency",
        "Security",
        "Modernization",
        "Reliability"
    ]


class ReviewResult(BaseModel):
    bugs: List[BugReport] = Field(default_factory=list)
    quality: List[QualityReport] = Field(default_factory=list)
    security: List[SecurityReport] = Field(default_factory=list)
    improvements: List[ImprovementSuggestion] = Field(default_factory=list)


@tool
def code_reviewer(code_chunk: str) -> dict:
    """
    Analyze code for bugs, quality issues,
    security vulnerabilities, and
    improvement opportunities.
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    structured_llm = llm.with_structured_output(
        ReviewResult
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert software architect,
security auditor,
and senior code reviewer.

Analyze the code and return:

1. bugs
2. quality issues
3. security vulnerabilities
4. improvement suggestions

For improvement impact use ONLY one of:

- Readability
- Performance
- Maintainability
- Memory Efficiency
- Concurrency
- Security
- Modernization
- Reliability

Return ONLY structured output.
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
