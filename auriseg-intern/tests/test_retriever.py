import pytest
import os
import shutil
from langchain_core.documents import Document
from src.vector_store.embedder import embed_and_store_in_chroma
from src.agent.retriever import CodeRetriever

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    test_dir = "test_chroma_retriever_db"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        
    mock_docs = [
        Document(page_content="def calculate_total(price): return price * 1.18", metadata={"filename": "tax.py", "language": "python"}),
        Document(page_content="def login_user(username, password): exec(f'SELECT * FROM users WHERE name={username}')", metadata={"filename": "auth.py", "language": "python"}),
        Document(page_content="void process_buffer(char *str) { char buf[10]; strcpy(buf, str); }", metadata={"filename": "buffer.c", "language": "c"}),
        Document(page_content="class MemoryLeakTracker { constructor() { this.data = []; } }", metadata={"filename": "tracker.js", "language": "javascript"})
    ]
    
    embed_and_store_in_chroma(documents=mock_docs, persist_directory=test_dir)
    yield
    
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

def test_retriever_all_query():
    retriever = CodeRetriever(persist_directory="test_chroma_retriever_db")
    docs = retriever.retrieve_code_chunks("calculate tax price function", query_type="all")
    assert len(docs) > 0
    assert any("tax.py" in d.metadata.get("filename", "") for d in docs)

def test_retriever_bug_query():
    retriever = CodeRetriever(persist_directory="test_chroma_retriever_db")
    docs = retriever.retrieve_code_chunks("buffer overflow array index out of bounds", query_type="bug")
    assert len(docs) > 0

def test_retriever_security_query():
    retriever = CodeRetriever(persist_directory="test_chroma_retriever_db")
    docs = retriever.retrieve_code_chunks("SQL injection raw exec login authentication vulnerability", query_type="security")
    assert len(docs) > 0
    assert any("auth.py" in d.metadata.get("filename", "") for d in docs)

def test_retriever_quality_query():
    retriever = CodeRetriever(persist_directory="test_chroma_retriever_db")
    docs = retriever.retrieve_code_chunks("code optimization and memory leak management overhead", query_type="quality")
    assert len(docs) > 0

def test_retriever_fallback_mechanism():
    retriever = CodeRetriever(persist_directory="test_chroma_retriever_db")
    docs = retriever.retrieve_code_chunks("something completely unrelated to coding syntax", score_threshold=1.5)
    assert len(docs) > 0
