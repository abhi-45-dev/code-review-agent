
import pytest
import tempfile
from langchain_core.documents import Document
from src.vector_store.embedder import (
    chunk_file_data,
    embed_and_store_in_chroma
)

def test_chunk_file_data_python_boundaries():
    mock_payload = {
        "filename": "auth.py",
        "language": "python",
        "full_content": "class UserAuth:\n    def login(self):\n        pass\n\n    def logout(self):\n        pass",
        "path": "/src/auth.py"
    }
    
    docs = chunk_file_data(mock_payload, chunk_size=50, chunk_overlap=0)
    
    assert len(docs) > 0
    for doc in docs:
        assert isinstance(doc, Document)
        assert doc.metadata["filename"] == "auth.py"
        assert doc.metadata["language"] == "python"
        assert doc.metadata["path"] == "/src/auth.py"
        assert "chunk_index" in doc.metadata

def test_chunk_file_data_fallback():
    mock_payload = {
        "filename": "config.xyz",
        "language": "unknown",
        "full_content": "setting1=true\nsetting2=false\nsetting3=true",
        "path": "/src/config.xyz"
    }
    
    docs = chunk_file_data(mock_payload, chunk_size=20, chunk_overlap=0)
    
    assert len(docs) > 0
    assert docs[0].metadata["language"] == "unknown"
    assert docs[0].metadata["chunk_index"] == 0

def test_chroma_storage_and_retrieval():
    mock_docs = [
        Document(
            page_content="def process_payment(amount):\n    print('Paying:', amount)",
            metadata={"filename": "billing.py", "chunk_index": 0, "language": "python", "path": "/src/billing.py"}
        ),
        Document(
            page_content="def reset_password(user):\n    print('Resetting password for:', user)",
            metadata={"filename": "auth.py", "chunk_index": 0, "language": "python", "path": "/src/auth.py"}
        )
    ]

    with tempfile.TemporaryDirectory() as tmp_dir:
        db = embed_and_store_in_chroma(mock_docs, persist_directory=tmp_dir)
        results = db.similarity_search("How do I change my password?", k=1)
        
        assert len(results) == 1
        assert "reset_password" in results[0].page_content
        assert results[0].metadata["filename"] == "auth.py"
