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
    if len(code_chunk) > 4000:
        code_chunk = code_chunk[:4000]
	
    print(f"Original size: {len(code_chunk)}")

    return {
        "code_chunk": code_chunk
    }
