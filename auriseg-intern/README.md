# Multi-Agent Code Review System

A production-grade, asynchronous code review agent built with LangGraph and LangChain. The system parses repository source files, evaluates code structures against customized guidelines using a vector database knowledge layer, and runs unified LLM evaluations to output standardized quality assessments.

## Core Architecture
- **Orchestration:** LangGraph (Asynchronous Map-Reduce Flow)
- **Framework:** LangChain
- **Vector Storage:** Chroma DB
- **Core Model:** Google Gemini Ecosystem

## Getting Started
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your keys in a local `.env` file
