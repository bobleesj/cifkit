import pytest

from cifkit.utils import folder
from cifkit.utils.cif_parser import (
    check_unique_atom_site_labels,
    get_cif_block,
    get_formula_structure_weight_s_group,
    get_label_occupancy_coordinates,
    get_line_content_from_tag,
    get_loop_tags,
    get_loop_value_dict,
    get_loop_values,
    get_start_end_line_indexes,
    get_tag_from_third_line,
    get_unique_elements_from_loop,
    get_unique_formulas_structures_weights_s_groups,
    get_unique_label_count,
    get_unique_site_labels,
    get_unitcell_angles_rad,
    get_unitcell_lengths,
    parse_atom_site_occupancy_info,
)
from cifkit.utils.error_messages import CifParserError


def test_get_cif_block(cif_block_URhIn):
    assert cif_block_URhIn is not None


def test_get_unit_cell_lengths_angles(cif_block_URhIn):
    lengths = get_unitcell_lengths(cif_block_URhIn)
    angles = get_unitcell_angles_rad(cif_block_URhIn)

    assert lengths == [7.476, 7.476, 3.881]
    assert angles == [1.5708, 1.5708, 2.0944]


def test_get_loop_tags():
    expected_tags = [
        "_atom_site_label",
        "_atom_site_type_symbol",
        "_atom_site_symmetry_multiplicity",
        "_atom_site_Wyckoff_symbol",
        "_atom_site_fract_x",
        "_atom_site_fract_y",
        "_atom_site_fract_z",
        "_atom_site_occupancy",
    ]

    assert get_loop_tags() == expected_tags, CifParserError.INVALID_LOOP_TAGS.value


def test_get_loop_values(cif_block_URhIn):
    loop_values = get_loop_values(cif_block_URhIn)

    assert loop_values[0][0] == "In1"
    assert loop_values[0][1] == "U1"
    assert loop_values[0][2] == "Rh1"
    assert loop_values[0][3] == "Rh2"
    assert loop_values[1][0] == "In"
    assert loop_values[1][1] == "U"
    assert loop_values[1][2] == "Rh"
    assert loop_values[1][3] == "Rh"


@pytest.mark.fast
def test_get_loop_value_ICSD(file_path_ICSD_formatted):
    block = get_cif_block(file_path_ICSD_formatted)
    loop_values = get_loop_values(block)
    assert loop_values[0][0] == "Fe1"
    assert loop_values[0][1] == "Ge1"
    assert loop_values[1][0] == "Fe0+"
    assert loop_values[1][1] == "Ge0+"
    assert loop_values[2][0] == "4"
    assert loop_values[2][1] == "4"
    assert loop_values[3][0] == "a"
    assert loop_values[3][1] == "a"
    assert loop_values[4][0] == "0.1352(4)"
    assert loop_values[4][1] == "0.8414(3)"
    assert loop_values[5][0] == "0.1352"
    assert loop_values[5][1] == "0.8414"
    assert loop_values[6][0] == "0.1352"
    assert loop_values[6][1] == "0.8414"
    assert loop_values[7][0] == "1."
    assert loop_values[7][1] == "1."


def test_get_num_of_atom_unique_labels(loop_values_URhIn):
    assert get_unique_label_count(loop_values_URhIn) == 4


def test_get_unique_elements(loop_values_URhIn):
    assert get_unique_elements_from_loop(loop_values_URhIn) == {
        "In",
        "Rh",
        "U",
    }


def test_get_atom_labels(loop_values_URhIn):
    assert get_unique_site_labels(loop_values_URhIn) == [
        "In1",
        "U1",
        "Rh1",
        "Rh2",
    ]


def test_get_label_occupancy_coordinates(loop_values_URhIn):
    label, occupacny, coordinates = get_label_occupancy_coordinates(loop_values_URhIn, 0)
    assert label == "In1"
    assert occupacny == 1.0
    assert coordinates == (0.2505, 0.0, 0.5)

    label, occupacny, coordinates = get_label_occupancy_coordinates(loop_values_URhIn, 1)
    assert label == "U1"
    assert occupacny == 1.0
    assert coordinates == (0.5925, 0.0, 0.0)


def test_get_loop_value_dict(loop_values_URhIn):
    expected_dict = {
        "In1": {"coords": (0.2505, 0.0, 0.5), "occupancy": 1.0},
        "Rh1": {
            "coords": (0.333333, 0.666667, 0.5),
            "occupancy": 1.0,
        },
        "Rh2": {"coords": (0.0, 0.0, 0.0), "occupancy": 1.0},
        "U1": {"coords": (0.5925, 0.0, 0.0), "occupancy": 1.0},
    }

    assert get_loop_value_dict(loop_values_URhIn) == expected_dict


def test_get_start_end_line_indexes():
    file_path = "tests/data/cif/format_author/author.cif"
    keyword = "_publ_author_address"
    # Line 54-103 before space a provided
    assert get_start_end_line_indexes(file_path, keyword) == (
        54,
        103,
    )


def test_get_line_content_from_tag(file_path_URhIn):
    content_lines = get_line_content_from_tag(file_path_URhIn, "_atom_site_occupancy")

    assert len(content_lines) == 4
    assert content_lines[0].strip() == "In1 In 3 g 0.2505 0 0.5 1"
    assert content_lines[1].strip() == "U1 U 3 f 0.5925 0 0 1"
    assert content_lines[2].strip() == "Rh1 Rh 2 d 0.333333 0.666667 0.5 1"
    assert content_lines[3].strip() == "Rh2 Rh 1 a 0 0 0 1"


def test_get_formula_structure_weight_sgroup(cif_block_URhIn):
    parsed_result = get_formula_structure_weight_s_group(cif_block_URhIn)
    (
        formula,
        structure,
        weight,
        s_group_num,
        s_group_name,
    ) = parsed_result
    assert formula == "URhIn"
    assert structure == "ZrNiAl"
    assert weight == 455.8
    assert s_group_num == 189
    assert s_group_name == "P-62m"


def test_get_unique_formulas_structure_weight(cif_folder_path_test):
    file_path_list = folder.get_file_paths(cif_folder_path_test)
    (
        formulas,
        structures,
        weights,
        s_group_nums,
        s_group_names,
    ) = get_unique_formulas_structures_weights_s_groups(file_path_list)
    assert formulas == {"LaRu2Ge2", "CeRu2Ge2", "EuIr2Ge2"}
    assert structures == {"CeAl2Ga2"}
    assert weights == {486.2, 487.4, 681.6}
    assert s_group_nums == {139}
    assert s_group_names == {"I4/mmm"}


def test_get_tag_from_third_line():
    file_path = "tests/data/cif/tag/1817275_rt.cif"
    assert get_tag_from_third_line(file_path) == "rt"

    file_path = "tests/data/cif/tag/1817275_rt_hex.cif"
    assert get_tag_from_third_line(file_path) == "rt_hex"


@pytest.mark.fast
def test_get_parsed_atom_site_occupancy_info(file_path_URhIn):
    atom_site_info = parse_atom_site_occupancy_info(file_path_URhIn)

    expected = {
        "In1": {
            "element": "In",
            "site_occupancy": 1.0,
            "x_frac_coord": 0.2505,
            "y_frac_coord": 0.0,
            "z_frac_coord": 0.5,
            "symmetry_multiplicity": 3,
            "wyckoff_symbol": "g",
        },
        "U1": {
            "element": "U",
            "site_occupancy": 1.0,
            "x_frac_coord": 0.5925,
            "y_frac_coord": 0.0,
            "z_frac_coord": 0.0,
            "symmetry_multiplicity": 3,
            "wyckoff_symbol": "f",
        },
        "Rh1": {
            "element": "Rh",
            "site_occupancy": 1.0,
            "x_frac_coord": 0.333333,
            "y_frac_coord": 0.666667,
            "z_frac_coord": 0.5,
            "symmetry_multiplicity": 2,
            "wyckoff_symbol": "d",
        },
        "Rh2": {
            "element": "Rh",
            "site_occupancy": 1.0,
            "x_frac_coord": 0.0,
            "y_frac_coord": 0.0,
            "z_frac_coord": 0.0,
            "symmetry_multiplicity": 1,
            "wyckoff_symbol": "a",
        },
    }

    assert atom_site_info == expected


@pytest.mark.fast
def test_get_parsed_atom_site_occupancy_info_ICSD(file_path_ICSD_formatted):
    atom_site_info = parse_atom_site_occupancy_info(file_path_ICSD_formatted)

    expected = {
        "Fe1": {
            "element": "Fe",
            "site_occupancy": 1.0,
            "symmetry_multiplicity": 4,
            "wyckoff_symbol": "a",
            "x_frac_coord": 0.1352,
            "y_frac_coord": 0.1352,
            "z_frac_coord": 0.1352,
        },
        "Ge1": {
            "element": "Ge",
            "site_occupancy": 1.0,
            "symmetry_multiplicity": 4,
            "wyckoff_symbol": "a",
            "x_frac_coord": 0.8414,
            "y_frac_coord": 0.8414,
            "z_frac_coord": 0.8414,
        },
    }
    assert atom_site_info == expected


def test_get_parsed_atom_site_occupancy_info_with_braket():
    """Er7 Er 16 h 0.06284 0.06662 0.39495 1 Co13B Co 4 c 0.75 0.25 0.59339
    0.07(3) `"""
    file_path = "tests/data/cif/cif_parser/1814810.cif"
    atom_site_info = parse_atom_site_occupancy_info(file_path)

    assert atom_site_info == {
        "Er7": {
            "element": "Er",
            "site_occupancy": 1.0,
            "x_frac_coord": 0.06284,
            "y_frac_coord": 0.06662,
            "z_frac_coord": 0.39495,
            "symmetry_multiplicity": 16,
            "wyckoff_symbol": "h",
        },
        "Co13B": {
            "element": "Co",
            "site_occupancy": 0.07,
            "x_frac_coord": 0.75,
            "y_frac_coord": 0.25,
            "z_frac_coord": 0.59339,
            "symmetry_multiplicity": 4,
            "wyckoff_symbol": "c",
        },
    }


@pytest.mark.fast
def test_check_unique_atom_site_labels(file_path_URhIn):
    check_unique_atom_site_labels(file_path_URhIn)

    duplicate_labels_file_path = "tests/data/cif/bad_cif_format/duplicate_labels.cif"
    with pytest.raises(ValueError) as e:
        check_unique_atom_site_labels(duplicate_labels_file_path)
    assert str(e.value) == "The file contains duplicate atom site labels."

    unparsable_file_path = "tests/data/cif/bad_cif_format/label_element_different.cif"
    with pytest.raises(ValueError) as e:
        check_unique_atom_site_labels(unparsable_file_path)
    assert str(e.value) == "The element was not correctly parsed from the site label."
