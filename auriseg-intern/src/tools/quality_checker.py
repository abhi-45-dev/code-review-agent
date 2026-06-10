from typing import List, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
load_dotenv()


class QualityReport(BaseModel):
    issue: str = Field(
        description="Code quality issue detected"
    )

    line_hint: str = Field(
        description="Line number or code snippet where the issue occurs"
    )

    severity: Literal["Low", "Medium", "High", "Critical"] = Field(
        description="Severity level of the issue"
    )

    explanation: str = Field(
        description="Explanation and suggested improvement"
    )


class QualityCheckResult(BaseModel):
    findings: List[QualityReport] = Field(
        default_factory=list,
        description="List of code quality findings"
    )


@tool
def quality_checker(code_chunk: str) -> dict:
    """
    Analyze code quality and suggest improvements.
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    structured_llm = llm.with_structured_output(
        QualityCheckResult
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert software quality reviewer.

Analyze the provided code and identify:

1. PEP8 naming convention violations
2. Excessively long functions
3. Cyclomatic complexity concerns
4. Missing type hints
5. Missing docstrings
6. Magic numbers
7. Refactoring opportunities
8. Readability and maintainability issues

For each finding provide:
- issue
- line_hint
- severity
- explanation

Return only structured output.
"""
            ),
            (
                "human",
                "Review the following code:\n\n{code}"
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
