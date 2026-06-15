import os

from src.agent.state import AgentState


SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".go",
    ".rs",
    ".cs",
    ".php",
    ".rb",
    ".swift",
    ".kt"
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build"
}


def ingest_node(state: AgentState):
    input_path = state["input_path"]
    files = []

    if os.path.isfile(input_path):
        ext = os.path.splitext(input_path)[1]

        if ext in SUPPORTED_EXTENSIONS:
            files.append(input_path)

    elif os.path.isdir(input_path):
        for root, dirs, filenames in os.walk(input_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for filename in filenames:
                ext = os.path.splitext(filename)[1]

                if ext in SUPPORTED_EXTENSIONS:
                    files.append(
                        os.path.relpath(
                            os.path.join(root, filename),
                            input_path
                        )
                    )

    return {
        "files": files,
        "current_file_index": 0,
        "current_file": files[0] if files else ""
    }

