import os
from pathlib import Path
from typing import List, Dict, Any

LANGUAGE_MAPPING = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
    ".rb": "ruby",
    ".rs": "rust",
    ".cs": "csharp",
    ".php": "php",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".sh": "shell"
}

def load_file_data(file_path: Path) -> Dict[str, Any]:
    """
    Safely reads a single file, handles encoding fallback, and extracts metadata.
    """
    ext = file_path.suffix.lower()
    language = LANGUAGE_MAPPING.get(ext, "unknown")
    
    # Handle unknown/unsupported formats safely
    if language == "unknown":
        raise ValueError(f"Unsupported file format: {ext}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fallback for encoding issues so the application doesn't crash
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        
    line_count = len(content.splitlines())
    
    return {
        "filename": file_path.name,
        "language": language,
        "full_content": content,
        "line_count": line_count,
        "path": str(file_path)
    }

def process_input(target_path: str) -> List[Dict[str, Any]]:
    """
    Core controller that accepts a single file or directory path,
    manages folder walking, and handles missing files.
    """
    path_obj = Path(target_path)
    
    # Handle File Not Found
    if not path_obj.exists():
        raise FileNotFoundError(f"The path '{target_path}' does not exist.")
        
    loaded_files = []
    
    # If single file path
    if path_obj.is_file():
        try:
            loaded_files.append(load_file_data(path_obj))
        except ValueError:
            # Skip or ignore unsupported formats when single file targeted if desired,
            # or pass it along depending on strictness. Here we skip cleanly.
            pass
        return loaded_files

    # If folder path, walk recursively
    for current_path in path_obj.rglob("*"):
        if current_path.is_file():
            # Skip build directories, virtual environments, and hidden folders
            if any(part.startswith('.') or part in ("node_modules", "venv", "__pycache__") for part in current_path.parts):
                continue
                
            ext = current_path.suffix.lower()
            if ext in LANGUAGE_MAPPING:
                try:
                    loaded_files.append(load_file_data(current_path))
                except Exception:
                    # Skip files that encounter unresolvable load issues to prevent crashing the directory walk
                    continue
                    
    return loaded_files

