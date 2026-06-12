from src.agent.graph import graph


def test_pipeline_runs_end_to_end():
    initial_state = {
        "input_path": "sample_buggy.py",
        "files": [],
        "current_file": "",
        "code_chunk": "",
        "code_chunks": [],
        "bug_results": [],
        "quality_results": [],
        "security_results": [],
        "improvement_results": [],
        "reports": {}
    }

    result = graph.invoke(initial_state)

    assert "reports" in result
    assert len(result["reports"]) > 0
