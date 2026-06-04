import os
from enum import Enum
from typing import TypedDict, List
from pydantic import BaseModel, Field
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

class ReviewStatus(str, Enum):
    PASSED = "Passed"
    VIOLATED = "Violated"
    WARNING = "Warning"

class SeverityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
    NONE = "None"

class FindingItem(BaseModel):
    rule_id: str = Field(
        description="The identifier of the rule being checked (e.g., 'Rule 1', 'Rule 2')."
    )
    status: ReviewStatus = Field(
        description="The status of the code compliance. Must exactly match one of the allowed Enum options."
    )
    severity: SeverityLevel = Field(
        description="Assigned risk level if a violation or warning is flagged. Use 'None' if the status is 'Passed'."
    )
    target_lines: str = Field(
        description="The exact snippet of code or line numbers where the finding is located (e.g., 'lines 4-8' or 'def PrintMessage(msg):')."
    )
    details: str = Field(
        description="A technical breakdown explaining why the code matches, violates, or triggers a warning against the specific rule."
    )
    suggestion: str = Field(
        description="Provide a concrete, refactored code block showing how to resolve the issue. If status is 'Passed', leave as an empty string."
    )

class StructuredReview(BaseModel):
    findings: List[FindingItem] = Field(
        description="A structured collection of individual rule assessments mapping back to the provided guidelines."
    )
    overall_summary: str = Field(
        description="An executive technical summary evaluating architectural risk, overall code health, and priority actions."
    )

class AgentState(TypedDict):
    code: str
    retrieved_rules: str
    review_findings: dict

def ingest_python_file(file_path: str):
    try:
        loader = TextLoader(file_path)
        documents = loader.load()
        return documents[0].page_content
    except Exception as e:
        print(f"[Error] Loading code file: {e}")
        return None

def setup_rag_retriever(rules_path: str):
    try:
        loader = TextLoader(rules_path)
        rules_doc = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0, separator="\n\n")
        chunks = text_splitter.split_documents(rules_doc)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.from_documents(chunks, embeddings)
        return db.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        print(f"[Error] Setting up RAG: {e}")
        return None

def review_node(state: AgentState):
    print("\n[Node] Entering LangGraph Review Node...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    structured_llm = llm.with_structured_output(StructuredReview)
    
    prompt = f"""
    You are an expert code reviewer. Analyze the following Python code based strictly on the provided rules.
    Evaluate the rules carefully and generate a structured review matching the required JSON schema.
    
    Rules:
    {state['retrieved_rules']}
    
    Code to Review:
    {state['code']}
    """
    
    response = structured_llm.invoke(prompt)
    return {"review_findings": response.model_dump()}

if __name__ == "__main__":
    code_content = ingest_python_file("target_code.py")
    retriever = setup_rag_retriever("coding_rules.txt")
    
    if retriever and code_content:
        docs = retriever.invoke("naming conventions documentation safety layout")
        rules_text = "\n\n".join([doc.page_content for doc in docs])
        
        workflow = StateGraph(AgentState)
        workflow.add_node("review_code", review_node)
        workflow.set_entry_point("review_code")
        workflow.add_edge("review_code", END)
        
        app = workflow.compile()
        
        initial_state = {
            "code": code_content,
            "retrieved_rules": rules_text,
            "review_findings": {}
        }
        
        print("[Graph] Executing workflow with fully descriptive Pydantic Enums...")
        final_output = app.invoke(initial_state)
        
        import json
        print("\n--- Enforced Structured JSON Output ---")
        print(json.dumps(final_output["review_findings"], indent=2))
