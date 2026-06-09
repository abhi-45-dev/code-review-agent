from src.agent.state import AgentState
from src.tools.security_checker import security_checker


def security_node(state: AgentState):
    result = security_checker.invoke(
        {
            "code_chunk": state["code_chunk"]
        }
    )

    return {
        "security_results": result.get("findings", [])
    }
