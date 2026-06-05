# System Requirements & Architecture Specification: Automated Code Review Agent
**Phase 2 — Project Design & Architecture**

---

## 1. Scope of Detection (Task 1)

### 1.1 Core Detection Categories
The agent enforces a strict, zero-tolerance policy for structural inefficiencies, poor code hygiene, and architectural hazards. It actively flags issues in the following categories, prioritizing performance and system safety even when code executes without explicit syntax errors:

* **Dead & Redundant Code:** Abandoned or unused variables, dead imports (`import`, `require`), and unreachable code blocks following terminating `return` statements.
* **Complex or Bloated Functions:** Code blocks or functions that violate the Single Responsibility Principle by handling multiple logic streams or exceeding optimal structural line-count thresholds.
* **Inefficient/Meaningless Loops:** Empty iteration structures, constant redundant operations within a loop, or high-complexity loops ($O(N^2)$) that can be structurally optimized using modern linear-time lookups (such as HashMaps, Dictionaries, or Sets).
* **Control Flow Optimization:** Deeply nested, cascading `if-else` structural layouts. The agent proactively suggests transitioning these patterns into clean, language-native alternatives.
* **Security, Safety & Basic Style:** Protection against dangerous execution vulnerabilities (e.g., `eval()`), missing entry parameter validation, omitted documentation (docstrings), and basic language-specific naming convention mismatches.

### 1.2 Multi-Language RAG Architecture
To ensure seamless scalability as more languages are added over the course of development, the retrieval layer isolates engineering guidelines completely:
* **Design Choice: Separate Indices per Language (Isolated Indexing).** Instead of utilizing a single, combined database prone to cross-language context pollution, individual vector indices are built natively per language (e.g., a dedicated index for Python PEP 8 / optimization guidelines and a separate, independent index for JavaScript style/safety rules).
* **Impact:** This approach completely eliminates language-rule confusion for the LLM during the retrieval state. When evaluating a source file, the orchestration pipeline dynamically routes semantic queries to the corresponding isolated vector database based purely on the target file's extension.

---

## 2. Level of Analysis & Optimization Strategy (Task 2)

### 2.1 Core Analysis Strategy: Whole-Folder Codebase Auditor
The agent operates directly at the directory or repository level rather than examining isolated files. This enables cross-referencing multiple modules, detecting cross-file script relationships, checking import validity, and generating a single, cohesive repository health report.

### 2.2 Speed & Memory Optimization Subsystem
To minimize execution latency and protect system memory when parsing entire multi-file project directories, the architecture integrates three distinct optimizations:
* **Token De-duplication Cache:** Before launching parallel processing tracks, the agent inspects structural layout hashes. If the same type of universal compliance violation is identified across multiple files, the agent utilizes cached rule contexts rather than repeating redundant vector lookups, optimizing total token usage.
* **Asynchronous Sub-Graph Parallelism:** Rather than executing scans sequentially (one file after another), the state graph explodes the discovered file checklist into parallel, concurrent worker threads using native asynchronous runtime environments to fully leverage system hardware capabilities.
* **Lazy File-Stream Loading:** To preserve a flat memory footprint, file contents are not logged globally into memory at initialization. Contents are dynamically streamed into the execution state only when their corresponding parallel worker node is scheduled and activated.

---

## 3. Execution Flow & Fault Tolerance (Task 3)

### 3.1 Architecture Pattern: Hybrid Router-State Machine
The workflow uses an advanced state graph combination that joins a simple, developer-readable routing pattern with a robust, self-healing state loop.

1. **The Ingestion & Routing Phase:** The entry node walks the folder structure and inspects extensions. Files ending in `.py` route directly to the Python track, and files ending in `.js` route to the JavaScript track. Unsupported assets (e.g., Markdown, images, binary caches) are intercepted and dropped immediately to conserve token and execution energy.
2. **The Controlled State Machine (Self-Healing Loop):** When an individual worker node finishes checking a file, its output payload passes through a strict structural Pydantic validation gate. If the LLM returns an incomplete or malformed JSON payload (e.g., missing a required parameter), a conditional edge catches the validation exception and loops the payload back to the LLM alongside the explicit stack trace. To control processing and token overhead, this self-healing loop is capped at a maximum of **2 retry attempts**.

### 3.2 Fault Tolerance: Isolated Graceful Degradation
The final consolidation stage protects pipeline integrity through total task isolation:
* **Behavior:** If a directory containing 9 files is scanned, and 8 files execute cleanly while 1 file repeatedly fails validation or hits an unhandled script error, **the program must not crash**.
* **Outcome:** The graph gracefully isolates the error, logs a clean diagnostic warning containing the specific path of the failed file inside the final aggregator state, and ensures that the compilation of the other 8 successful file reports continues without disruption.

---

## 4. Output Definition & Pydantic Schema Format (Task 4)

### 4.1 Severity Levels Triage System
Findings are categorized under four explicit priority categories to ensure developers know exactly what issues require mandatory attention versus optional adjustments:

* **Critical:** Assigned to any vulnerability, bug, or pattern that risks causing data loss, leakage, corruption, or unauthorized access to a **database**, as well as system-breaking blocks like active infinite loops or hardcoded production API credentials. **Rule:** If a bug compromises data safety, it is automatically escalated to Critical, no matter how minor or simple the code fix is.
* **Medium:** Assigned to heavy structural design code smells that directly degrade runtime efficiency and violate clean code principles (e.g., redundant loops, bloated functions handling multiple architectural responsibilities, or bare exception handling blocks).
* **Low:** Assigned to **mandatory clean-up actions and technical debt** that developers must resolve before moving to production, even though the current code executes safely without throwing errors (e.g., dead variables, leftover unused library imports, or redundant variable assignments right before a return).
* **Info:** Strictly limited to minor code improvement suggestions and developer guidance where compliance is **completely optional and up to the choice of the developer or client** (e.g., syntax shortcuts like suggesting a list comprehension, modern arrow functions, or structural type-hinting guidelines).

### 4.2 Pydantic Field Specification Schema

```python
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
