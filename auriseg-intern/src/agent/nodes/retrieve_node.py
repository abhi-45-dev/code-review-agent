from src.vector_store.embedder import chunk_file_data
import os

from src.agent.state import AgentState


def retrieve_node(state: AgentState):
    input_path = state["input_path"]
    current_file = state["current_file"]

    if os.path.isdir(input_path):
        file_path = os.path.join(input_path, current_file)
    else:
        file_path = current_file

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code_chunk = file.read()

    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            code_chunk = file.read()

    print(f"Original size: {len(code_chunk)}")

    docs = chunk_file_data(
        {
            "language": "c",
            "full_content": code_chunk,
            "filename": current_file,
            "path": file_path
        },
        chunk_size=3000,
        chunk_overlap=300
    )

    code_chunks = [doc.page_content for doc in docs]

    print(f"Chunk count: {len(code_chunks)}")

    return {
        "code_chunk": code_chunk,
        "code_chunks": code_chunks
    }
