import filecmp
import os
import shutil
import tempfile

import pytest

from cifkit.utils.cif_editor import remove_author_loop


@pytest.fixture
def setup_and_teardown_file():
    temp_dir = tempfile.mkdtemp()
    original_file_path = "tests/data/cif/format_author/author.cif"
    temp_file_path = os.path.join(temp_dir, "author.cif")
    reference_file_path = "tests/data/cif/format_author/author_removed.cif"

    shutil.copyfile(original_file_path, temp_file_path)
    yield temp_file_path, reference_file_path
    shutil.rmtree(temp_dir)


def test_remove_author_loop(setup_and_teardown_file):
    temp_file_path, reference_file_path = setup_and_teardown_file

    remove_author_loop(temp_file_path)

    assert filecmp.cmp(
        temp_file_path, reference_file_path, shallow=False
    ), "The modified file does not match the reference file."


# def test_formatting_ICSD_file():
#     # Parse the structure, density, formula, another formula
#     file_path = "tests/data/ICSD/icsd_001385.cif"
#     top_header_data = extract_top_header_info(new_file_path)

#     # Remove all of the headers until the first "loop_"
#     truncate_content_after_loop(file_path, new_file_path)

#     # Insert header data into the truncated file
#     insert_ICSD_top_header(
#         new_file_path,
#         top_header_data,
#         formatted_file_path,
#     )
