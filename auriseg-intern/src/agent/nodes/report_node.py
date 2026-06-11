from src.agent.state import AgentState

from src.output.report_generator import (
    generate_json_report,
    generate_markdown_report
)


def report_node(state: AgentState):
    current_file = state["current_file"]

    file_report = {
        "bug_results": state.get("bug_results", []),
        "quality_results": state.get("quality_results", []),
        "security_results": state.get("security_results", []),
        "improvement_results": state.get("improvement_results", [])
    }

    json_report = generate_json_report(
        current_file,
        file_report
    )

    markdown_report = generate_markdown_report(
        current_file,
        file_report
    )

    reports = dict(
        state.get("reports", {})
    )

    reports[current_file] = {
        "json_report": json_report,
        "markdown_report": markdown_report
    }

    return {
        "reports": reports
    }
