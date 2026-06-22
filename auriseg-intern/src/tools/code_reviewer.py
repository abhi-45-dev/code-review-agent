from typing import List, Literal
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from src.llm.factory import get_llm

load_dotenv()


PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "code_review_prompt_v1.txt"
)
SYSTEM_PROMPT = PROMPT_PATH.read_text(
    encoding="utf-8"
)


class BugReport(BaseModel):
    issue: str
    line_hint: str
    severity: Literal["Low", "Medium", "High", "Critical"]
    explanation: str
    evidence: str


class QualityReport(BaseModel):
    issue: str
    line_hint: str
    severity: Literal["Low", "Medium", "High", "Critical"]
    explanation: str
    evidence: str


class SecurityReport(BaseModel):
    issue: str
    line_hint: str

    severity: Literal[
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    confidence: Literal[
        "Low",
        "Medium",
        "High"
    ]

    cwe_id: str

    owasp_category: str

    explanation: str

    evidence: str

    remediation: str


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

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ReviewResult
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT
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
