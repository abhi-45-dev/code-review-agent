from src.agent.state import AgentState
from src.tools.security_checker import security_checker


def security_node(state: AgentState):
    print(f"Security node chunks: {len(state['code_chunks'])}")

    all_findings = []

    for i, chunk in enumerate(state["code_chunks"]):
        print(f"Analyzing security chunk {i + 1}/{len(state['code_chunks'])}")

        result = security_checker.invoke(
            {
                "code_chunk": chunk
            }
        )

        all_findings.extend(
            result.get("findings", [])
        )

    return {
        "security_results": all_findings
    }
