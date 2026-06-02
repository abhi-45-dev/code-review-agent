import os
import sys
import logging
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Configure logging to suppress noisy warnings and outputs
logging.basicConfig(level=logging.ERROR)

# --- CONFIGURATION LAYER ---
MODEL_NAME = "llama-3.3-70b-versatile"
TARGET_FILE = "src/prompt_experiments.py"
DB_PATH = "faiss_index"

def run_rag_pipeline():
    print(f"📂 [Step 1] Loading target source file natively: {TARGET_FILE}...")
    if not os.path.exists(TARGET_FILE):
        print(f"❌ Error: Target file {TARGET_FILE} not found.")
        return

    try:
        # Read the file using native Python I/O for virtual environment stability
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            file_content = f.read()
        raw_documents = [Document(page_content=file_content, metadata={"source": TARGET_FILE})]
        print("✅ Successfully loaded file context natively.")
    except Exception as e:
        print(f"❌ Failed to read file natively: {str(e)}")
        return

    # 2. Optimized Text Splitting Layer
    print("\n🗜️ [Step 2] Splitting raw code layout into logical semantic chunks...")
    # Increased chunk size to 1000 to ensure imports and full blocks don't get sharded awkwardly
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", "def ", "class ", " ", ""]
    )
    chunks = splitter.split_documents(raw_documents)
    print(f"✅ Generated {len(chunks)} comprehensive text chunks.")

    # 3. Embedding Model Initialization
    print("\n🧠 [Step 3] Loading local HuggingFace embedding engine (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 4. Compute Coordinates & Build FAISS Store
    print("💾 [Step 4] Computing vector coordinates and writing to local FAISS index...")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DB_PATH)
    print(f"✅ FAISS index successfully built and saved to folder: '{DB_PATH}'")

    # 5. Initialize LLM Synthesis Generation Layer
    try:
        model = ChatGroq(model=MODEL_NAME, temperature=0)
    except Exception as e:
        print(f"❌ Failed to initialize Groq model: {str(e)}")
        return

    # 6. Establish the Contextual Q&A Prompt Template Matrix
    qa_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert software engineering assistant specializing in codebase analysis.\n"
            "Answer the user's question about the source code using ONLY the retrieved context snippets provided below.\n"
            "If the answer cannot be derived from the context, state clearly that the code snippet wasn't found.\n\n"
            "=== RETRIEVED REPOSITORY CONTEXT ===\n{retrieved_context}"
        ),
        ("human", "{user_question}")
    ])

    print("\n🚀 Codebase RAG Pipeline Online! Type 'exit' to quit.\n")

    # 7. Interactive Q&A Retrieval Loop
    while True:
        try:
            user_query = input("Ask about your codebase: ")
            if user_query.lower() == 'exit':
                print("Ending RAG session.")
                break
                
            if not user_query.strip():
                continue

            # 🔍 Step A: Execute similarity search with expanded window (k=4)
            print("📡 [Retrieval] Searching FAISS vector coordinates...")
            matched_docs = db.similarity_search(user_query, k=4)
            
            # Format the matches into a single clean context block
            compiled_context = ""
            for i, doc in enumerate(matched_docs):
                compiled_context += f"\n--- Snippet {i+1} ---\n{doc.page_content}\n"

            # 🧠 Step B: Pipe the context and question straight into the LLM chain
            print("🧠 [LLM Generation] Synthesizing response from repository context...")
            rag_chain = qa_prompt | model
            response = rag_chain.invoke({
                "retrieved_context": compiled_context,
                "user_question": user_query
            })

            print(f"\nAI:\n{response.content}\n")
            print("-" * 60)

        except KeyboardInterrupt:
            print("\nSession interrupted cleanly.")
            continue
        except Exception as e:
            print(f"\n❌ Error encountered during query pipeline: {str(e)}\n")
            continue

if __name__ == "__main__":
    run_rag_pipeline()
