from src.agent.state import AgentState
from src.tools.code_reviewer import code_reviewer


def review_node(state: AgentState):
    print(f"Review node chunks: {len(state['code_chunks'])}")

    bug_results = []
    quality_results = []
    security_results = []
    improvement_results = []

    for i, chunk in enumerate(state["code_chunks"]):
        print(f"Reviewing chunk {i + 1}/{len(state['code_chunks'])}")

        result = code_reviewer.invoke(
            {
                "code_chunk": chunk
            }
        )

        bug_results.extend(
            result.get("bugs", [])
        )

        quality_results.extend(
            result.get("quality", [])
        )

        security_results.extend(
            result.get("security", [])
        )

        improvement_results.extend(
            result.get("improvements", [])
        )

    return {
        "bug_results": bug_results,
        "quality_results": quality_results,
        "security_results": security_results,
        "improvement_results": improvement_results
    }
