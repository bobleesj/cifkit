import os
from cifkit.utils import folder
import glob
from cifkit.models.cif import Cif
from cifkit.utils.error_messages import CifParserError
from pathlib import Path


def make_directory_and_move(file_path, dir_path, new_file_path):
    """
    Create directory if it doesn't exist and move the file.
    """
    os.makedirs(dir_path, exist_ok=True)
    new_file_path = os.path.join(dir_path, new_file_path)
    os.rename(file_path, new_file_path)


def move_files_based_on_errors(dir_path):
    print(f"\nCIF Preprocessing in {dir_path} begun...\n")

    # Ensure dir_path is a Path object
    dir_path = Path(dir_path)

    # Dictionary to hold directory paths for each error type
    error_directories = {
        "error_operations": dir_path / "error_operations",
        "error_duplicate_labels": dir_path / "error_duplicate_labels",
        "error_wrong_loop_value": dir_path / "error_wrong_loop_value",
        "error_coords": dir_path / "error_coords",
        "error_invalid_label": dir_path / "error_invalid_label",
        "error_others": dir_path / "error_others",
    }

    # Ensure all direct
    file_paths = list(dir_path.glob("*.cif"))
    num_files_moved = {key: 0 for key in error_directories.keys()}
    file_paths = folder.get_file_paths(str(dir_path))

    for i, file_path in enumerate(file_paths, start=1):
        filename = os.path.basename(file_path)
        print(f"Preprocessing {file_path} ({i}/{len(file_paths)})")
        try:
            Cif(file_path)
        except Exception as e:
            error_message = str(e)
            # Example of handling specific errors, adjust as needed
            if "symmetry operation" in error_message:
                error_type = "error_operations"
            elif "contains duplicate atom site labels" in error_message:
                error_type = "error_duplicate_labels"
            elif "Wrong number of values in loop" in error_message:
                error_type = "error_wrong_loop_value"
            elif "missing atomic coordinates" in error_message:
                error_type = "error_coords"
            elif "incorrectly parsed element" in error_message:
                error_type = "error_invalid_label"
            else:
                error_type = "error_others"

            make_directory_and_move(
                file_path, error_directories[error_type], filename
            )
            num_files_moved[error_type] += 1
            print(
                f"File {filename} moved to '{error_type}' due to: {error_message}"
            )

    # Display the number of files moved to each folder
    print("\nSUMMARY")
    for error_type, count in num_files_moved.items():
        print(f"# of files moved to '{error_type}' folder: {count}")