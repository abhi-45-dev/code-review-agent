from src.agent.state import AgentState
from src.tools.quality_checker import quality_checker


def quality_node(state: AgentState):
    print(f"Quality node chunks: {len(state['code_chunks'])}")

    all_findings = []

    for i, chunk in enumerate(state["code_chunks"]):
        print(f"Analyzing quality chunk {i + 1}/{len(state['code_chunks'])}")

        result = quality_checker.invoke(
            {
                "code_chunk": chunk
            }
        )

        all_findings.extend(
            result.get("findings", [])
        )

    return {
        "quality_results": all_findings
    }
