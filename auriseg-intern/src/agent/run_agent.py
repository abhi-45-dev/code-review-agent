from src.agent.graph import graph


def run_agent(input_path: str):
    initial_state = {
        "input_path": input_path,
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
    path = input("Enter file or folder path: ").strip()

    reports = run_agent(path)
    

    print("\n" + "=" * 60)
    print("CODE REVIEW REPORT")
    print("=" * 60)

    for filename, report in reports.items():
        print(f"\nFILE: {filename}")

        json_report = report.get("json_report", {})
        summary = json_report.get("summary", {})

        print("\nSUMMARY")
        print("-" * 30)
        print(f"Total Issues : {summary.get('total_issues', 0)}")
        print(f"Critical     : {summary.get('critical_count', 0)}")
        print(f"High         : {summary.get('high_count', 0)}")
        print(f"Medium       : {summary.get('medium_count', 0)}")
        print(f"Low          : {summary.get('low_count', 0)}")
        print(f"Info         : {summary.get('info_count', 0)}")

        print("\nMARKDOWN REPORT PREVIEW")
        print("-" * 30)

        markdown_report = report.get(
            "markdown_report",
            "No markdown report generated."
        )

        print(markdown_report[:1000])

        if len(markdown_report) > 1000:
            print("\n... truncated ...")
