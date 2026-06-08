from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List, Dict, Any

LANGCHAIN_SPLITTER_MAPPING = {
    "python": Language.PYTHON,
    "javascript": Language.JS,
    "typescript": Language.TS,
    "java": Language.JAVA,
    "cpp": Language.CPP,
    "c": Language.C,
    "go": Language.GO,
    "php": Language.PHP,
    "html": Language.HTML,
    "ruby": Language.RUBY,
    "rust": Language.RUST,
}

def chunk_file_data(file_payload: Dict[str, Any], chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Document]:
    language_str = file_payload.get("language", "unknown")
    content = file_payload.get("full_content", "")
    filename = file_payload.get("filename", "unknown")
    file_path = file_payload.get("path", "unknown")
    
    if language_str in LANGCHAIN_SPLITTER_MAPPING:
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=LANGCHAIN_SPLITTER_MAPPING[language_str],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    else:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
    raw_chunks = splitter.split_text(content)
    documents = []
    
    for index, chunk_text in enumerate(raw_chunks):
        doc = Document(
            page_content=chunk_text,
            metadata={
                "filename": filename,
                "chunk_index": index,
                "language": language_str,
                "path": file_path
            }
        )
        documents.append(doc)
        
    return documents

def embed_and_store_in_chroma(documents: List[Document], persist_directory: str = "chroma_db") -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="compliance_guidelines"
    )
    
    return vector_store
