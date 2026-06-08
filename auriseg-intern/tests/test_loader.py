import os
import pytest
import tempfile
from pathlib import Path
from ingestion.loader import process_input, load_file_data

def test_process_single_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test_script.py"
        file_path.write_text("print('Hello World')", encoding="utf-8")
        
        results = process_input(str(file_path))
        
        assert len(results) == 1
        assert results[0]["filename"] == "test_script.py"
        assert results[0]["language"] == "python"
        assert results[0]["line_count"] == 1

def test_process_directory_scan():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "main.py").write_text("import os", encoding="utf-8")
        (tmp_path / "index.js").write_text("console.log()", encoding="utf-8")
        (tmp_path / "styles.css").write_text("body {}", encoding="utf-8")
        
        # Create a venv folder to test exclusion logic
        venv_dir = tmp_path / "venv"
        venv_dir.mkdir()
        (venv_dir / "ignored.py").write_text("print()", encoding="utf-8")
        
        results = process_input(str(tmpdir))
        
        # Should catch python, javascript, and css, but skip the venv folder
        assert len(results) == 3
        languages = [item["language"] for item in results]
        assert "python" in languages
        assert "javascript" in languages
        assert "css" in languages

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        process_input("non_existent_file_path_xyz.py")

def test_encoding_fallback():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "corrupt_bytes.py"
        # Write bytes that are invalid in strict UTF-8
        file_path.write_bytes(b"print('hello')\n# \xff\xfe invalid text")
        
        results = process_input(str(file_path))
        assert len(results) == 1
        assert results[0]["language"] == "python"
        assert results[0]["line_count"] == 2
