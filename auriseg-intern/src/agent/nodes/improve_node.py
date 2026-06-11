from src.agent.state import AgentState
from src.tools.improvement_suggester import improvement_suggester


def improve_node(state: AgentState):
    print(f"Improve node chunks: {len(state['code_chunks'])}")

    all_findings = []

    for i, chunk in enumerate(state["code_chunks"]):
        print(f"Analyzing improve chunk {i + 1}/{len(state['code_chunks'])}")

        result = improvement_suggester.invoke(
            {
                "code_chunk": chunk
            }
        )

        all_findings.extend(
            result.get("findings", [])
        )

    return {
        "improvement_results": all_findings
    }
