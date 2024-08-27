import os
import shutil

import pytest

from cifkit.preprocessors.error import move_files_based_on_errors
from cifkit.utils.folder import get_file_count, get_file_paths


@pytest.mark.fast
def test_move_files_based_on_errors(tmp_path):
    # Setup source directory and temporary directory for testing
    source_dir = "tests/data/cif/error/combined"
    tmp_dir = tmp_path / "ensemble_error"
    tmp_dir.mkdir()

    # Get file paths from the source directory and copy to tmp_path
    file_paths = get_file_paths(source_dir)
    new_paths = []
    for file_path in file_paths:
        new_file_path = tmp_dir / os.path.basename(file_path)
        shutil.copy(file_path, new_file_path)
        new_paths.append(new_file_path)  # Keep track of new file paths

    # Define expected directories
    expected_dirs = {
        "error_duplicate_labels": tmp_dir / "error_duplicate_labels",
        "error_wrong_loop_value": tmp_dir / "error_wrong_loop_value",
        "error_invalid_label": tmp_dir / "error_invalid_label",
        "error_others": tmp_dir / "error_others",
    }

    # Run the function with the paths in the temporary directory
    move_files_based_on_errors(str(tmp_dir), new_paths)

    # Assert the number of files in each directory
    assert get_file_count(expected_dirs["error_wrong_loop_value"]) == 1
    assert get_file_count(expected_dirs["error_duplicate_labels"]) == 1
    assert get_file_count(expected_dirs["error_invalid_label"]) == 1
