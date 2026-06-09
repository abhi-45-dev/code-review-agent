from typing import List, Literal

from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class ImprovementSuggestion(BaseModel):
    suggestion: str = Field(
        description="Short title of the improvement recommendation"
    )

    current_pattern: str = Field(
        description="Current code pattern or approach detected"
    )

    recommended_pattern: str = Field(
        description="Better alternative pattern or implementation"
    )

    reason: str = Field(
        description="Why the recommended pattern is better"
    )

    impact: Literal[
        "Readability",
        "Performance",
        "Maintainability",
        "Memory Efficiency",
        "Concurrency",
        "Security",
        "Modernization"
    ] = Field(
        description="Primary area improved by this suggestion"
    )


class ImprovementSuggestionResult(BaseModel):
    findings: List[ImprovementSuggestion] = Field(
        default_factory=list,
        description="List of improvement recommendations"
    )


@tool
def improvement_suggester(code_chunk: str) -> dict:
    """
    Analyze code and suggest improvements, optimizations,
    and modern coding practices.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    structured_llm = llm.with_structured_output(
        ImprovementSuggestionResult
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert software architect and senior code reviewer.

Analyze the provided code and suggest improvements related to:

1. Readability
2. Performance
3. Maintainability
4. Memory efficiency
5. Concurrency opportunities
6. Security best practices
7. Modern language features and idioms
8. Design pattern improvements
9. Refactoring opportunities

For each suggestion provide:

- suggestion
- current_pattern
- recommended_pattern
- reason
- impact

Impact must be one of:
- Readability
- Performance
- Maintainability
- Memory Efficiency
- Concurrency
- Security
- Modernization

Focus on practical and actionable improvements.

Return only structured output.
"""
            ),
            (
                "human",
                "Review this code and suggest improvements:\n\n{code}"
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
