from typing import Dict, List, TypedDict


class AgentState(TypedDict):
    # User input
    input_path: str

    # Repository ingestion
    files: List[str]
    current_file: str
    current_file_index: int

    code_chunk: str
    code_chunks: List[str]

    # Current file results
    bug_results: List[dict]
    quality_results: List[dict]
    security_results: List[dict]
    improvement_results: List[dict]

    # Repository-wide reports
    reports: Dict[str, dict]
