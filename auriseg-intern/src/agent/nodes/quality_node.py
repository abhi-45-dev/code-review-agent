from src.agent.state import AgentState
from src.tools.quality_checker import quality_checker


def quality_node(state: AgentState):
    result = quality_checker.invoke(
        {
            "code_chunk": state["code_chunk"]
        }
    )

    return {
        "quality_results": result.get("findings", [])
    }
