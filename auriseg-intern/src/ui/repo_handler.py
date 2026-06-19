from file_utils import (
    save_uploaded_file
)

from zip_utils import (
    extract_uploaded_zip
)


def prepare_repository(
    uploaded_file
) -> str:

    zip_path = save_uploaded_file(
        uploaded_file
    )

    repo_path = extract_uploaded_zip(
        zip_path
    )

    return repo_path


def prepare_repository(
    uploaded_file
) -> str:
    """
    Save uploaded ZIP and return
    extracted repository path.
    """

    zip_path = save_uploaded_file(
        uploaded_file
    )

    repo_path = extract_uploaded_zip(
        zip_path
    )

    return repo_path
