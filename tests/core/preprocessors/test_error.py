import os
import shutil

import pytest

from cifkit.preprocessors.error import move_files_based_on_errors
from cifkit.utils.folder import get_file_count, get_file_paths


@pytest.mark.fast
def test_move_files_based_on_errors(tmpdir):
    # Setup source directory and temporary directory for testing
    source_dir = "tests/data/cif/error/combined"
    file_paths = get_file_paths(source_dir)
    new_paths = []
    for file_path in file_paths:
        new_file_path = os.path.join(tmpdir, os.path.basename(file_path))
        shutil.copy(file_path, new_file_path)
        new_paths.append(new_file_path)

    # Define expected directories
    expected_dirs = {
        "error_duplicate_labels": tmpdir / "error_duplicate_labels",
        "error_wrong_loop_value": tmpdir / "error_wrong_loop_value",
        "error_invalid_label": tmpdir / "error_invalid_label",
        "error_others": tmpdir / "error_others",
    }

    # Run the function with the paths in the temporary directory
    move_files_based_on_errors(str(tmpdir), new_paths)

    # Assert the number of files in eoach directory
    assert get_file_count(expected_dirs["error_duplicate_labels"]) == 1
    assert get_file_count(expected_dirs["error_invalid_label"]) == 1
