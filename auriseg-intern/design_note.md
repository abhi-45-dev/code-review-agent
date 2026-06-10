# Design Note: Automated Code Review Agent via RAG & LangGraph

## 1. System Architecture
This system implements an automated code review pipeline combining Retrieval-Augmented Generation (RAG) with stateful workflow orchestration. 

* **Ingestion & Representation**: Code components are read into memory using file loaders. Reference engineering guidelines are chunked using structural paragraph separators (`\n\n`) to preserve rule integrity.
* **Retrieval Mechanism**: Semantic search is performed completely offline using a local HuggingFace embedding engine (`all-MiniLM-L6-v2`) paired with an in-memory FAISS vector index. Relevant coding constraints are extracted dynamically based on query contexts.
* **State Management**: LangGraph manages data transitions through a predictable `AgentState` schema, tracking source arrays, retrieved context strings, and the resulting validation structures.
* **Deterministic Parsing**: The underlying LLM is integrated with structured output compilation bounded by Pydantic validation frameworks. Strongly typed Enums restrict arbitrary diagnostic categorizations.

## 2. Key Learnings & Takeaways
* **Context Anchoring prevents Hallucinations**: Forcing the model to grade scripts exclusively against specific retrieved vector contexts eliminates generalized feedback and ensures strict compliance tracking.
* **State Isolation**: Using LangGraph isolates discrete operational elements. Moving from unstructured textual evaluation to precise data objects remains modular, allowing for future additions like auto-repair iterations.
* **Schema Enforcement**: Utilizing Pydantic configurations with strict `Enum` and descriptive mappings guarantees dependable data boundaries, shifting LLM output targets from arbitrary strings to highly structured APIs.

returns json output as per the prepared pydantic schema
