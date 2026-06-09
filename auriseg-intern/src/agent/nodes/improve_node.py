from src.agent.state import AgentState
from src.tools.improvement_suggester import improvement_suggester


def improve_node(state: AgentState):
    result = improvement_suggester.invoke(
        {
            "code_chunk": state["code_chunk"]
        }
    )

    return {
        "improvement_results": result.get("findings", [])
    }
