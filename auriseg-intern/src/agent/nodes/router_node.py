from src.agent.state import AgentState


def route_next_file(state: AgentState):
    files = state.get("files", [])
    current_index = state.get("current_file_index", 0)

    next_index = current_index + 1

    if next_index >= len(files):
        return {
            "current_file_index": next_index
        }

    return {
        "current_file_index": next_index,
        "current_file": files[next_index]
    }


def has_more_files(state: AgentState):
    files = state.get("files", [])
    current_index = state.get("current_file_index", 0)

    if current_index + 1 < len(files):
        return "next"

    return "end"
