import glob
import os
import shutil

from cifkit.utils.error_messages import FileError


def get_file_path(dir_path: str, file_name: str) -> str:
    """Construct and return the full path for a file within a specified
    directory."""
    return os.path.join(dir_path, file_name)


def get_file_count(dir_path: str, ext=".cif") -> int:
    """Count files with a given extension in a directory."""
    return len(glob.glob(os.path.join(dir_path, f"*{ext}")))


def get_file_paths(dir_path: str, ext=".cif", add_nested_files=False) -> list[str]:
    """Return a list of file paths with a given extension from a
    directory."""
    if add_nested_files:
        # Traverse through directory and subdirectories
        files_list = []
        for root, dirs, files in os.walk(dir_path):
            files_list.extend(
                [os.path.join(root, file) for file in files if file.endswith(ext)]
            )
        return files_list
    else:
        # Find files in the specified directory only
        return glob.glob(os.path.join(dir_path, f"*{ext}"))


def make_output_folder(dir_path: str, new_folder_name: str) -> str:
    """Create an output folder."""
    full_path = os.path.join(dir_path, new_folder_name)

    # Check if the directory already exists
    if not os.path.exists(full_path):
        # Create the directory
        os.makedirs(full_path)
        print(f"Folder '{new_folder_name}' created at '{dir_path}'.")
    else:
        print(f"Folder '{new_folder_name}' already exists at '{dir_path}'.")
    return full_path


def check_file_exists(file_path: str) -> bool:
    """Check if the specified file exists."""
    if not os.path.exists(file_path):
        # Using enum value and formatting it with file_path
        raise FileNotFoundError(
            FileError.FILE_NOT_FOUND.value.format(file_path=file_path)
        )
    return True


def check_file_not_empty(file_path: str) -> bool:
    """Check if the specified file is not empty."""
    if os.path.getsize(file_path) == 0:
        # Using enum value and formatting it with file_path
        raise ValueError(FileError.FILE_IS_EMPTY.value.format(file_path=file_path))
    return True


def move_files(to_directory: str, file_path_list: list[str]) -> None:
    """Move files to another folder, creating the folder if it doesn't
    exist."""
    # Ensure the destination directory exists
    os.makedirs(to_directory, exist_ok=True)

    # Move each file in the list
    for file_path in file_path_list:
        dest_file_path = os.path.join(to_directory, os.path.basename(file_path))
        # Move file to new directory
        shutil.move(file_path, dest_file_path)


def copy_files(to_directory: str, file_path_list: list[str]) -> None:
    """Copy files to another folder, creating the folder if it doesn't
    exist."""
    # Ensure the destination directory exists
    os.makedirs(to_directory, exist_ok=True)

    # Copy each file in the list
    for file_path in file_path_list:
        # Construct full destination path
        dest_file_path = os.path.join(to_directory, os.path.basename(file_path))
        # Copy file to new directory
        shutil.copy(file_path, dest_file_path)
