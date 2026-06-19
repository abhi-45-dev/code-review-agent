from src.agent.graph import graph


def run_agent(
    input_path: str,
    review_type: str = "all"
):
    initial_state = {
        "input_path": input_path,
        "review_type": review_type,
        "files": [],
        "current_file": "",
        "current_file_index": 0,
        "code_chunk": "",
        "code_chunks": [],
        "bug_results": [],
        "quality_results": [],
        "security_results": [],
        "improvement_results": [],
        "reports": {}
    }

    result = graph.invoke(initial_state)

    return result.get("reports", {})


if __name__ == "__main__":
    path = input(
        "Enter file or folder path: "
    ).strip()

    review_type = input(
        "Review type (all/bug/quality/security): "
    ).strip().lower()

    if review_type not in [
        "all",
        "bug",
        "quality",
        "security"
    ]:
        print(
            "Invalid review type. "
            "Defaulting to 'all'."
        )
        review_type = "all"

    reports = run_agent(
        path,
        review_type
    )

    print("\n" + "=" * 60)
    print("CODE REVIEW REPORT")
    print("=" * 60)

    for filename, report in reports.items():
        print(f"\nFILE: {filename}")

        json_report = report.get(
            "json_report",
            {}
        )

        summary = json_report.get(
            "summary",
            {}
        )

        print("\nSUMMARY")
        print("-" * 30)
        print(
            f"Total Issues : "
            f"{summary.get('total_issues', 0)}"
        )
        print(
            f"Critical     : "
            f"{summary.get('critical_count', 0)}"
        )
        print(
            f"High         : "
            f"{summary.get('high_count', 0)}"
        )
        print(
            f"Medium       : "
            f"{summary.get('medium_count', 0)}"
        )
        print(
            f"Low          : "
            f"{summary.get('low_count', 0)}"
        )
        print(
            f"Info         : "
            f"{summary.get('info_count', 0)}"
        )

        print("\nMARKDOWN REPORT PREVIEW")
        print("-" * 30)

        markdown_report = report.get(
            "markdown_report",
            "No markdown report generated."
        )

        print(markdown_report[:1000])

        if len(markdown_report) > 1000:
            print("\n... truncated ...")
