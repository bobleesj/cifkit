import filecmp
import os
import shutil
import tempfile

import gemmi
import pytest

from cifkit.utils.cif_editor import add_hashtag_in_first_line, remove_author_loop
from cifkit.utils.cif_parser import get_unitcell_lengths


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


@pytest.mark.fast
def test_hashtag_in_first_line(tmpdir):
    temp_file_path = os.path.join(tmpdir, "test.cif")
    origin_file_path = "tests/data/cif/sources/ICSD/EntryWithCollCode43054.cif"
    shutil.copyfile(origin_file_path, temp_file_path)

    add_hashtag_in_first_line(temp_file_path)

    doc = gemmi.cif.read_file(temp_file_path)
    block = doc.sole_block()
    assert get_unitcell_lengths(block) == [4.7, 4.7, 4.7]
