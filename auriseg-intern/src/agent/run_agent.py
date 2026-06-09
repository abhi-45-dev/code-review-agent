from src.agent.graph import graph


def run_agent(input_path: str):
    initial_state = {
        "input_path": input_path,
        "files": [],
        "current_file": "",
        "code_chunk": "",
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

        print(f"  Bugs: {len(report.get('bug_results', []))}")
        print(f"  Quality: {len(report.get('quality_results', []))}")
        print(f"  Security: {len(report.get('security_results', []))}")
        print(f"  Improvements: {len(report.get('improvement_results', []))}")
