from src.agent.state import AgentState


def report_node(state: AgentState):
    current_file = state["current_file"]

    file_report = {
        "bug_results": state.get("bug_results", []),
        "quality_results": state.get("quality_results", []),
        "security_results": state.get("security_results", []),
        "improvement_results": state.get("improvement_results", [])
    }

    reports = dict(state.get("reports", {}))
    reports[current_file] = file_report

    return {
        "reports": reports
    }
