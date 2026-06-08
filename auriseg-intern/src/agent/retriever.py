import os
from typing import List, Literal
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

QueryType = Literal["bug", "security", "quality", "all"]

class CodeRetriever:
    def __init__(self, persist_directory: str = "chroma_db", collection_name: str = "compliance_guidelines"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
    def get_vector_store(self) -> Chroma:
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )

    def retrieve_code_chunks(
        self, 
        query: str, 
        query_type: QueryType = "all", 
        score_threshold: float = 0.3, 
        top_k: int = 4
    ) -> List[Document]:
        db = self.get_vector_store()
        
        enriched_query = query
        if query_type != "all":
            enriched_query = f"[{query_type.upper()} CONTEXT] {query}"
            
        results_with_scores = db.similarity_search_with_relevance_scores(
            query=enriched_query,
            k=top_k
        )
        
        filtered_docs = [
            doc for doc, score in results_with_scores 
            if score >= score_threshold
        ]
        
        if not filtered_docs and results_with_scores:
            filtered_docs = [doc for doc, _ in results_with_scores]
            
        return filtered_docs
