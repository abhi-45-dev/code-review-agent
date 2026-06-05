from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class IssueCategory(str, Enum):
    SECURITY = "Security"
    BUG = "Bug"
    CODE_SMELL = "Code Smell"
    STYLE = "Style"

class SeverityTier(str, Enum):
    CRITICAL = "Critical"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

class LanguageFamily(str, Enum):
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"

class FindingItem(BaseModel):
    rule_id: str = Field(
        description="The exact alphanumeric identifier mapping back to the retrieved reference rule chunk from the language vector database (e.g., 'Rule 1')."
    )
    category: IssueCategory = Field(
        description="The structural or behavioral classification of the identified issue."
    )
    severity: SeverityTier = Field(
        description="The risk priority triage level mapping directly back to deployment pipeline guardrails."
    )
    target_lines: str = Field(
        description="The explicit line numbers, range, or exact code snippet where the finding resides (e.g., 'lines 45-52')."
    )
    details: str = Field(
        description="A clear technical breakdown detailing why the code blocks violate or match the specific reference guideline."
    )
    suggestion: Optional[str] = Field(
        default="",
        description="A valid, refactored code block showing the developer how to implement the exact fix. Must never be blank if severity is Critical, Medium, or Low."
    )

class FileReport(BaseModel):
    file_path: str = Field(
        description="The relative file path of the processed source component (e.g., 'src/auth/session.js')."
    )
    language: LanguageFamily = Field(
        description="The identified syntax family of the source target file."
    )
    findings: Optional[List[FindingItem]] = Field(
        default=[],
        description="An array compiling all localized diagnostic findings. Automatically defaults to an empty list if a file passes all guidelines perfectly."
    )

class RepoSummary(BaseModel):
    total_files_scanned: int = Field(
        description="The total count of supported source files discovered and walked inside the target directory."
    )
    successful_scans: int = Field(
        description="The total count of components parsed and reviewed without pipeline compilation or schema errors."
    )
    failed_scans: int = Field(
        description="The total count of components that permanently failed validation or hit unhandled processing bottlenecks."
    )
    failed_file_paths: Optional[List[str]] = Field(
        default=[],
        description="An array documenting the paths of files that failed scanning due to structural errors, acting as the system's fault-tolerance log."
    )
    repository_health_score: str = Field(
        description="An executive summary quality score calculated across the entire project repository (e.g., '92/100')."
    )
