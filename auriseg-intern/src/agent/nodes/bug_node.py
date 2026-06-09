from src.agent.state import AgentState
from src.tools.bug_detector import bug_detector


def bug_node(state: AgentState):
    result = bug_detector.invoke(
        {
            "code_chunk": state["code_chunk"]
        }
    )

    return {
        "bug_results": result.get("findings", [])
    }

