import os
import shutil
import zipfile
from pathlib import Path


def extract_uploaded_zip(
    zip_path: str,
    extract_root: str = "extracted_repos"
) -> str:
    """
    Extract uploaded ZIP and return extracted folder path.
    """

    zip_name = Path(zip_path).stem

    extract_path = os.path.join(
        extract_root,
        zip_name
    )

    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)

    os.makedirs(
        extract_path,
        exist_ok=True
    )

    with zipfile.ZipFile(
        zip_path,
        "r"
    ) as zip_ref:
        zip_ref.extractall(
            extract_path
        )

    return extract_path
