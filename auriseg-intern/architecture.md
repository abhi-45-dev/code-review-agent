# System Requirements & Architecture Specification: Automated Code Review Agent
**Phase 2 — Project Design, Flow Diagram, & Tool Planning**

---

## 1. Scope of Detection & RAG Core Pipeline

### 1.1 Core Detection Categories
The agent enforces a strict, zero-tolerance policy for structural inefficiencies, poor code hygiene, and architectural hazards. It actively flags issues in the following categories, prioritizing performance and system safety even when code executes without explicit syntax errors:

* **Dead & Redundant Code:** Abandoned or unused variables, dead imports (`import`, `require`), and unreachable code blocks following terminating `return` statements.
* **Complex or Bloated Functions:** Code blocks or functions that violate the Single Responsibility Principle by handling multiple logic streams or exceeding optimal structural line-count thresholds.
* **Inefficient/Meaningless Loops:** Empty iteration structures, constant redundant operations within a loop, or high-complexity loops ($O(N^2)$) that can be structurally optimized using modern linear-time lookups (such as HashMaps, Dictionaries, or Sets).
* **Control Flow Optimization:** Deeply nested, cascading `if-else` structural layouts. The agent proactively suggests transitioning these patterns into clean, language-native alternatives.
* **Security, Safety & Basic Style:** Protection against dangerous execution vulnerabilities (e.g., `eval()`), missing entry parameter validation, omitted documentation (docstrings), and basic language-specific naming convention mismatches.

### 1.2 End-to-End Core RAG Pipeline Flow
The system processes and checks source code targets against static rules by implementing a sequential RAG Preparation and Execution flow:

`Ingest ──► Chunk ──► Embed ──► Retrieve ──► Review ──► Report`

* **Data Ingestion:** The pipeline reads reference documentation containing corporate coding standards, optimization rules, and security guidelines for both Python and JavaScript. 
* **Markdown/Structure-Based Chunking:** Documents are split dynamically using structure-based markdown heading boundaries (`MarkdownHeaderTextSplitter` anchored to `## Rule X`). This guarantees that a rule's description, target violations, and refactoring guidelines stay bound together as atomic contextual chunks, eliminating structural noise.
* **Vector Space Embedding & Storage:** Chunks are embedded and stored in **Chroma DB** across completely isolated data collections (`python_rules` vs `javascript_rules`) to prevent cross-language context pollution. When evaluating a source file, the orchestration pipeline dynamically routes semantic queries to the corresponding isolated collection based purely on the target file's extension.

---

## 2. Level of Analysis & Optimization Strategy

### 2.1 Core Analysis Strategy: Whole-Folder Codebase Auditor
The agent operates directly at the directory or repository level rather than examining isolated files. This enables cross-referencing multiple modules, detecting cross-file script relationships, checking import validity, and generating a single, cohesive repository health report.

### 2.2 Speed & Memory Optimization Subsystem
To minimize execution latency and protect system memory when parsing entire multi-file project directories, the architecture integrates three distinct optimizations:
* **Token De-duplication Cache:** Before launching parallel processing tracks, the agent inspects structural layout hashes. If the same type of universal compliance violation is identified across multiple files, the agent utilizes cached rule contexts rather than repeating redundant vector lookups, optimizing total token usage.
* **Asynchronous Sub-Graph Parallelism:** Rather than executing scans sequentially (one file after another), the state graph explodes the discovered file checklist into parallel, concurrent worker threads using native asynchronous runtime environments to fully leverage system hardware capabilities.
* **Lazy File-Stream Loading:** To preserve a flat memory footprint, file contents are not loaded globally into memory at initialization. Contents are dynamically streamed into the execution state only when their corresponding parallel worker node is scheduled and activated.

---

## 3. Execution Flow & Fault Tolerance

### 3.1 Architecture Pattern: Hybrid Map-Reduce Router-State Machine
The workflow uses an advanced state graph combination that joins a simple, developer-readable routing pattern with a robust, self-healing state loop running across concurrent asynchronous worker tracks.

```mermaid
graph TD
    %% Styling
    classDef storage fill:#f9f,stroke:#333,stroke-width:2px;
    classDef process fill:#bbf,stroke:#333,stroke-width:2px;
    classDef flow fill:#dfd,stroke:#333,stroke-width:1px;

    %% 1. Background Knowledge Injection Subsystem (RAG Prep)
    subgraph RAG_Preparation [1. Core Rule RAG Pipeline]
        A[Raw Coding Standards MD] --> B[Markdown Header Splitter]
        B -->|Atomic Rule Contexts| C[Embedding Model Engine]
        C --> D1[(Chroma DB: Python Collection)]:::storage
        C --> D2[(Chroma DB: JS Collection)]:::storage
    end

    %% 2. Execution Pipeline (Map-Reduce System)
    subgraph LangGraph_Engine [2. Parallel Orchestration Engine]
        E[Target Folder Path Input] --> F[Ingestion Node]
        F -->|pathlib.Path.rglob| G{Language Router}
        
        %% Map Phase (Parallel Workers)
        G -->|Filter .py files| H1[Parallel Worker Lane: Python]:::flow
        G -->|Filter .js files| H2[Parallel Worker Lane: JS]:::flow
        
        %% Core Unified Processing Nodes
        H1 --> I1[Unified Review Node: file_x.py]:::process
        H2 --> I2[Unified Review Node: file_y.js]:::process
        
        %% Internal Node Utilities
        D1 -.->|Similarity Context Search| I1
        D2 -.->|Similarity Context Search| I2
        
        %% LLM Interfacing
        I1 --> J1[LLM Pass: .with_structured_output]
        I2 --> J2[LLM Pass: .with_structured_output]
        
        %% Self-Healing Validation Loops
        J1 -->|Fails Pydantic Guard| K1{Validation Retry Gate}
        K1 -->|Retry Max 2| I1
        J2 -->|Fails Pydantic Guard| K2{Validation Retry Gate}
        K2 -->|Retry Max 2| I2
        
        %% Reduce Phase (Automatic Aggregation)
        K1 -->|Valid Pydantic Payload| L[operator.add Automatic Reducer Sink]:::flow
        K2 -->|Valid Pydantic Payload| L
        J1 -->|Valid Pydantic Payload| L
        J2 -->|Valid Pydantic Payload| L
        
        %% Final Synthesis
        L --> M[Reduction & Formatter Node]:::process
        M --> N[Final Structured JSON + MD Output Report]
    end
