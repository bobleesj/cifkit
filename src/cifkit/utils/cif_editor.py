import os

from cifkit.preprocessors.format import preprocess_label_element_loop_values
from cifkit.utils import cif_parser

# Parser .cif file
from cifkit.utils.cif_parser import check_unique_atom_site_labels
from cifkit.utils.cif_sourcer import get_cif_db_source


def remove_author_loop(file_path: str) -> None:
    """Remove the author section from a .cif file to prevent parsing
    problems caused by a wrongly formatted author block.

    This is a common issue in PCD files.
    """
    (
        start_index,
        end_index,
    ) = cif_parser.get_start_end_line_indexes(file_path, "_publ_author_address")

    with open(file_path, "r") as f:
        original_lines = f.readlines()

        # Replace the specific section in original_lines with modified_lines
        original_lines[start_index:end_index] = ["''\n", ";\n", ";\n"]

    with open(file_path, "w") as f:
        f.writelines(original_lines)


def add_hashtag_in_first_line(file_path: str):
    """ICSD files start with (C) which causes parsing issues with gemmi.

    If that is the case, add a # before (C) to fix the parsing issue.
    """
    # First, check if the file exists and is a CIF file
    if not os.path.exists(file_path) or not file_path.endswith(".cif"):
        raise FileNotFoundError("File does not exist or is not a CIF file")

    # Read the contents of the file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Check if the first line starts with (C)
    if lines and lines[0].startswith("(C)"):
        # Modify the first line by adding a # right after (C)
        lines[0] = lines[0].replace("(C)", "# (C)", 1)

        # Write the modified content back to the file
        with open(file_path, "w") as file:
            file.writelines(lines)


def edit_cif_file_based_on_db(file_path: str):
    """Edit a CIF file based on the database it is from.

    PCD: Remove author loop and preprocess label element loop values
    ICSD: Add a hashtag in the first line
    """
    db_source = get_cif_db_source(file_path)
    if db_source == "ICSD":
        add_hashtag_in_first_line(file_path)
    elif db_source == "PCD":
        remove_author_loop(file_path)
        # Preprocessing the label is only tested on PCD files
        preprocess_label_element_loop_values(file_path)

    check_unique_atom_site_labels(file_path)
