from typing import List, Literal

from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class SecurityReport(BaseModel):
    issue: str = Field(
        description="Security issue detected"
    )

    line_hint: str = Field(
        description="Line number or code snippet where the issue occurs"
    )

    severity: Literal["Low", "Medium", "High", "Critical"] = Field(
        description="Severity level of the issue"
    )

    explanation: str = Field(
        description="Explanation of the vulnerability and suggested remediation"
    )


class SecurityCheckResult(BaseModel):
    findings: List[SecurityReport] = Field(
        default_factory=list,
        description="List of security findings"
    )


@tool
def security_checker(code_chunk: str) -> dict:
    """
    Analyze code for security vulnerabilities.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    structured_llm = llm.with_structured_output(
        SecurityCheckResult
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert application security reviewer.

Analyze the provided code and identify:

1. Hardcoded API keys, passwords, tokens, secrets
2. SQL injection vulnerabilities
3. Shell/command injection vulnerabilities
4. Dangerous eval() or exec() usage
5. Unsafe deserialization (pickle, yaml.load, etc.)
6. Sensitive data exposed in logs
7. Weak cryptography or insecure hashing
8. Insecure authentication practices
9. Insecure file handling
10. Any OWASP-style security risks

Severity guidance:
- Critical: exploitable secrets, injection, RCE, auth bypass
- High: serious security weaknesses
- Medium: risky patterns
- Low: security hygiene issues

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
