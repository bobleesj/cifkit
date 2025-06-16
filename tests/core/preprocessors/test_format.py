import os
import shutil
import tempfile

import pytest

from cifkit.preprocessors.format import preprocess_label_element_loop_values
from cifkit.utils import cif_parser, folder, string_parser


def run_preprocess_test_on_cif_files(cif_dir):
    # Create a temporary directory to store the copied folder
    temp_dir = tempfile.mkdtemp()
    temp_cif_dir = os.path.join(temp_dir, os.path.basename(cif_dir))
    shutil.copytree(cif_dir, temp_cif_dir)
    cif_file_path_list = folder.get_file_paths(temp_cif_dir)

    for temp_cif_file_path in cif_file_path_list:
        preprocess_label_element_loop_values(temp_cif_file_path)
        # Perform tests on the modified temporary file
        block = cif_parser.get_cif_block(temp_cif_file_path)
        loop_values = cif_parser.get_loop_values(block)
        num_element_labels = len(loop_values[0])

        for i in range(num_element_labels):
            atom_type_label = loop_values[0][i]
            atom_type_symbol = loop_values[1][i]
            parsed_atom_type_symbol = string_parser.get_atom_type_from_label(
                atom_type_label
            )
            assert atom_type_symbol == parsed_atom_type_symbol

    # Clean up the temporary directory after tests
    shutil.rmtree(temp_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_1():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_1"
    run_preprocess_test_on_cif_files(cif_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_2():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_2"
    run_preprocess_test_on_cif_files(cif_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_3():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_3"
    run_preprocess_test_on_cif_files(cif_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_4():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_4"
    run_preprocess_test_on_cif_files(cif_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_5():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_5"
    run_preprocess_test_on_cif_files(cif_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_6():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_6"
    run_preprocess_test_on_cif_files(cif_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_7():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_7"
    run_preprocess_test_on_cif_files(cif_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_8():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_8"
    run_preprocess_test_on_cif_files(cif_dir)


@pytest.mark.fast
def test_preprocess_cif_file_on_label_element_type_mixed():
    cif_dir = "tests/data/cif/format_label/symbolic_atom_label_type_mixed"

    temp_dir = tempfile.mkdtemp()
    temp_cif_dir = os.path.join(temp_dir, os.path.basename(cif_dir))
    shutil.copytree(cif_dir, temp_cif_dir)

    cif_file_path_list = folder.get_file_paths(temp_cif_dir)

    for temp_cif_file_path in cif_file_path_list:
        preprocess_label_element_loop_values(temp_cif_file_path)
        lines = cif_parser.get_line_content_from_tag(
            temp_cif_file_path, "_atom_site_occupancy"
        )

        filename = os.path.basename(temp_cif_file_path)

        # Type 1
        if filename == "457848.cif":
            assert len(lines) == 6
            assert lines[4].strip() == "NiM1 Ni 3 b 0 0 0.5 0.5"
            assert lines[5].strip() == "TaM2 Ta 3 b 0 0 0.5 0.5"

        if filename == "250805.cif":
            assert len(lines) == 3
            assert lines[1].strip() == "PrM1 Pr 8 b 0.375 0.375 0.375 0.75"
            assert lines[2].strip() == "PtM2 Pt 8 b 0.375 0.375 0.375 0.25"
        if filename == "1020250.cif":
            assert len(lines) == 3
            assert lines[1].strip() == "Co Co 8 c 0.25 0.25 0.25 1"

        if filename == "312084.cif":
            assert len(lines) == 3
            assert lines[0].strip() == "Ge1A Ge 8 h 0 0.06 0.163 0.500"
            assert lines[1].strip() == "Pd1B Pd 8 h 0 0.06 0.163 0.500"

        if filename == "1020251.cif":
            assert len(lines) == 3
            assert lines[1].strip() == "Rh Rh 8 c 0.25 0.25 0.25 1"

        if filename == "1633288.cif":
            assert len(lines) == 7
            assert lines[2].strip() == "Dy Dy 4 i 0 0.5 0.1935 1"

        if filename == "1049941.cif":
            assert len(lines) == 11
            assert lines[0].strip() == "Pr1 Pr 4 j 0.02076 0.5 0.30929 1"
            assert lines[-1].strip() == "In4 In 2 a 0 0 0 1"

        if filename == "381111.cif":
            assert len(lines) == 6
            assert lines[0].strip() == "Ni1A Ni 4 j 0 0.172 0.5 0.88(1)"
            assert lines[1].strip() == "Ga1B Ga 4 j 0 0.172 0.5 0.12(1)"

        # Type 7
        if filename == "1817279.cif":
            assert len(lines) == 3
            assert lines[0].strip() == "Fe1 Fe 1 d 0.5 0.5 0.5 0.99(4)"
            assert lines[1].strip() == "Pt2 Pt 1 d 0.5 0.5 0.5 0.01(4)"

        # Type 7
        if filename == "1817275.cif":
            assert len(lines) == 4
            assert lines[0].strip() == "Fe1 Fe 1 d 0.5 0.5 0.5 0.97(4)"
            assert lines[1].strip() == "Pt2 Pt 1 d 0.5 0.5 0.5 0.03(4)"
            assert lines[2].strip() == "Pt1 Pt 1 a 0 0 0 0.98(4)"
            assert lines[3].strip() == "Fe2 Fe 1 a 0 0 0 0.02(4)"

        # Type 8
        if filename == "1814810.cif":
            assert len(lines) == 13
            assert lines[0].strip() == "Er7 Er 16 h 0.06284 0.06662 0.39495 1"
            assert lines[9].strip() == "Er13A Er 4 c 0.75 0.25 0.14542 0.83(2)"
            assert lines[10].strip() == "In13B In 4 c 0.75 0.25 0.14542 0.17(2)"
            assert lines[11].strip() == "In13A In 4 c 0.75 0.25 0.59339 0.93(3)"
            assert lines[12].strip() == "Co13B Co 4 c 0.75 0.25 0.59339 0.07(3)"

        # Type 9
        if filename == "1200981.cif":
            assert len(lines) == 4
            assert lines[1].strip() == "SnB Sn 4 c 0.0595 0.25 0.0952 1"
            assert lines[2].strip() == "SnA Sn 4 c 0.0983 0.25 0.6419 1"

    shutil.rmtree(temp_dir)
