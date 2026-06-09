from src.agent.graph import graph

initial_state = {
    "input_path": "sample_buggy.py",
    "files": [],
    "current_file": "sample_buggy.py",
    "code_chunk": "",
    "bug_results": [],
    "quality_results": [],
    "security_results": [],
    "improvement_results": [],
    "reports": {}
}

result = graph.invoke(initial_state)

print("\n" + "=" * 60)
print("GRAPH EXECUTION SUCCESS")
print("=" * 60)

print("\nFiles Processed:")
print(result.get("reports", {}).keys())

print("\nReport:")
print(result.get("reports", {}))
