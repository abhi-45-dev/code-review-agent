from src.agent.state import AgentState
from src.tools.bug_detector import bug_detector


def bug_node(state: AgentState):
    print(f"Bug node chunks: {len(state['code_chunks'])}")

    all_findings = []

    for i, chunk in enumerate(state["code_chunks"]):
        print(f"Analyzing bug chunk {i + 1}/{len(state['code_chunks'])}")

        result = bug_detector.invoke(
            {
                "code_chunk": chunk
            }
        )

        all_findings.extend(
            result.get("findings", [])
        )

    return {
        "bug_results": all_findings
    }
