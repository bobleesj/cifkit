import os
import shutil
import pytest
import logging
from cifkit import Cif
from cifkit.utils.error_messages import CifParserError
from cifkit.utils.log_messages import CifLog
from cifkit.utils import folder


@pytest.mark.fast
def test_cif_static_properties(cif_URhIn):
    assert cif_URhIn.file_path == "tests/data/cif/URhIn.cif"
    assert cif_URhIn.file_name == "URhIn.cif"
    assert cif_URhIn.file_name_without_ext == "URhIn"
    assert cif_URhIn.unique_elements == {"In", "Rh", "U"}
    assert cif_URhIn.composition_type == 3
    assert cif_URhIn.formula == "URhIn"
    assert cif_URhIn.structure == "ZrNiAl"
    assert cif_URhIn.weight == 455.8
    assert cif_URhIn.site_labels == ["In1", "U1", "Rh1", "Rh2"]
    assert cif_URhIn.space_group_name == "P-62m"
    assert cif_URhIn.space_group_number == 189

    assert cif_URhIn.tag == "rt"

    assert cif_URhIn.bond_pairs == {
        ("U", "U"),
        ("Rh", "Rh"),
        ("In", "In"),
        ("In", "Rh"),
        ("In", "U"),
        ("Rh", "U"),
    }

    assert cif_URhIn.bond_pairs_sorted_by_mendeleev == {
        ("Rh", "Rh"),
        ("U", "Rh"),
        ("U", "U"),
        ("In", "In"),
        ("Rh", "In"),
        ("U", "In"),
    }

    assert cif_URhIn.site_label_pairs == {
        ("In1", "Rh2"),
        ("Rh1", "Rh2"),
        ("Rh2", "Rh2"),
        ("In1", "Rh1"),
        ("Rh1", "U1"),
        ("In1", "U1"),
        ("Rh2", "U1"),
        ("In1", "In1"),
        ("Rh1", "Rh1"),
        ("U1", "U1"),
    }
    assert cif_URhIn.site_label_pairs_sorted_by_mendeleev == {
        ("Rh2", "Rh2"),
        ("Rh1", "Rh2"),
        ("U1", "Rh2"),
        ("Rh2", "In1"),
        ("In1", "In1"),
        ("Rh1", "Rh1"),
        ("U1", "Rh1"),
        ("U1", "U1"),
        ("Rh1", "In1"),
        ("U1", "In1"),
    }

    assert cif_URhIn.atom_site_info == {
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

    assert cif_URhIn.site_mixing_type == "full_occupancy"
    assert cif_URhIn.mixing_info_per_label_pair == {
        ("Rh2", "U1"): "full_occupancy",
        ("In1", "In1"): "full_occupancy",
        ("U1", "U1"): "full_occupancy",
        ("In1", "Rh2"): "full_occupancy",
        ("Rh1", "Rh1"): "full_occupancy",
        ("Rh2", "Rh2"): "full_occupancy",
        ("Rh1", "U1"): "full_occupancy",
        ("Rh1", "Rh2"): "full_occupancy",
        ("In1", "U1"): "full_occupancy",
        ("In1", "Rh1"): "full_occupancy",
    }
    assert cif_URhIn.mixing_info_per_label_pair_sorted_by_mendeleev == {
        ("U1", "Rh1"): "full_occupancy",
        ("In1", "In1"): "full_occupancy",
        ("Rh2", "In1"): "full_occupancy",
        ("U1", "U1"): "full_occupancy",
        ("U1", "In1"): "full_occupancy",
        ("Rh1", "Rh1"): "full_occupancy",
        ("U1", "Rh2"): "full_occupancy",
        ("Rh2", "Rh2"): "full_occupancy",
        ("Rh1", "Rh2"): "full_occupancy",
        ("Rh1", "In1"): "full_occupancy",
    }


@pytest.mark.fast
def test_lazy_loading(cif_URhIn):
    assert cif_URhIn.connections is None
    cif_URhIn.compute_connections()
    assert cif_URhIn.connections is not None


"""
Test log
"""


@pytest.mark.fast
def test_init_log(caplog):
    file_path = "tests/data/cif/URhIn.cif"
    cif = Cif(file_path, logging_enabled=True)

    with caplog.at_level(logging.INFO):
        assert (
            CifLog.PREPROCESSING.value.format(file_path=file_path)
            in caplog.text
        )

        assert CifLog.LOADING_DATA.value in caplog.text

    cif.compute_connections()
    with caplog.at_level(logging.INFO):
        assert CifLog.COMPUTE_CONNECTIONS.value in caplog.text


@pytest.mark.fast
def test_init_no_log(caplog):
    file_path = "tests/data/cif/URhIn.cif"
    Cif(file_path)

    with caplog.at_level(logging.INFO):
        assert caplog.text == ""


@pytest.mark.fast
def test_shortest_distance(cif_URhIn):
    assert cif_URhIn.shortest_distance == 2.697


@pytest.mark.fast
def test_shortest_distance_computation():
    cif_URhIn = Cif("tests/data/cif/URhIn.cif")
    assert cif_URhIn.connections is None
    distance = cif_URhIn.shortest_distance
    assert cif_URhIn.connections is not None
    assert distance == 2.697


@pytest.mark.fast
def test_connections_flattened(cif_URhIn):
    assert cif_URhIn.connections_flattened[0] == (("In", "Rh"), 2.697)
    assert len(cif_URhIn.connections_flattened) == 621


@pytest.mark.fast
def test_shortest_bond_pair_distance(cif_URhIn):
    assert cif_URhIn.shortest_bond_pair_distance == {
        ("In", "In"): 3.244,
        ("In", "Rh"): 2.697,
        ("In", "U"): 3.21,
        ("Rh", "Rh"): 3.881,
        ("Rh", "U"): 2.983,
        ("U", "U"): 3.881,
    }


@pytest.mark.fast
def test_shortest_distance_per_site(cif_URhIn):
    expected = {
        "In1": ("Rh2", 2.697),
        "Rh1": ("In1", 2.852),
        "Rh2": ("In1", 2.697),
        "U1": ("Rh1", 2.984),
    }
    result = cif_URhIn.shortest_site_pair_distance

    assert all(
        result[label][0] == expected[label][0]
        and pytest.approx(result[label][1], 0.001) == expected[label][1]
        for label in result
    )


# Radius
@pytest.mark.fast
def test_radius_values(cif_URhIn):
    assert cif_URhIn.radius_values == {
        "In": {
            "CIF_radius": 1.624,
            "CIF_radius_refined": 1.3283481582381291,
            "Pauling_radius_CN12": 1.66,
        },
        "Rh": {
            "CIF_radius": 1.345,
            "CIF_radius_refined": 1.368651841761871,
            "Pauling_radius_CN12": 1.342,
        },
        "U": {
            "CIF_radius": 1.377,
            "CIF_radius_refined": 1.6143481582381292,
            "Pauling_radius_CN12": 1.51,
        },
    }


@pytest.mark.fast
def test_radius_sum_data(cif_URhIn, radius_sum_data_URhIn):
    result = cif_URhIn.radius_sum
    assert result == radius_sum_data_URhIn


@pytest.mark.fast
def test_CN_max_gap_per_site(cif_URhIn, max_gaps_per_label_URhIn):
    result = cif_URhIn.CN_max_gap_per_site
    assert result == max_gaps_per_label_URhIn


@pytest.mark.fast
def test_CN_best_methods(cif_URhIn):
    result = cif_URhIn.CN_best_methods
    assert result["In1"]["number_of_vertices"] == 14
    assert result["U1"]["number_of_vertices"] == 17
    assert result["Rh1"]["number_of_vertices"] == 9
    assert result["Rh2"]["number_of_vertices"] == 9


@pytest.mark.fast
def test_CN_connetions_by_best_method(cif_URhIn):
    result = cif_URhIn.CN_connections_by_best_methods
    assert len(result["In1"]) == 14
    assert len(result["U1"]) == 17
    assert len(result["Rh1"]) == 9
    assert len(result["Rh2"]) == 9


@pytest.mark.fast
def test_CN_connetions_by_dist_min_method(cif_URhIn):
    result = cif_URhIn.CN_connections_by_min_dist_method
    assert len(result["In1"]) == 14
    assert len(result["U1"]) == 11
    assert len(result["Rh1"]) == 9
    assert len(result["Rh2"]) == 9


"""
Test bond fractions, counts, avg, min, max, unique CN
by (1) min_dist method and (2) best method
"""

"""Test bond counts"""


@pytest.mark.now
def test_CN_bond_counts_by_min_dist_method(cif_URhIn):
    result = cif_URhIn.CN_bond_count_by_min_dist_method

    assert result == {
        "In1": {("In", "In"): 4, ("In", "Rh"): 4, ("In", "U"): 6},
        "Rh1": {("In", "Rh"): 3, ("Rh", "U"): 6},
        "Rh2": {("In", "Rh"): 6, ("Rh", "U"): 3},
        "U1": {("In", "U"): 6, ("Rh", "U"): 5},
    }


@pytest.mark.now
def test_CN_bond_counts_by_best_methods(cif_URhIn):
    result = cif_URhIn.CN_bond_count_by_best_methods
    assert result == {
        "In1": {("In", "In"): 4, ("In", "Rh"): 4, ("In", "U"): 6},
        "Rh1": {("In", "Rh"): 3, ("Rh", "U"): 6},
        "Rh2": {("In", "Rh"): 6, ("Rh", "U"): 3},
        "U1": {
            ("In", "U"): 6,
            ("Rh", "U"): 5,
            ("U", "U"): 6,
        },
    }


@pytest.mark.now
def test_CN_bond_counts_by_min_dist_method_sorted_by_mendeleev(cif_URhIn):
    result = cif_URhIn.CN_bond_count_by_min_dist_method_sorted_by_mendeleev
    assert result == {
        "In1": {("Rh", "In"): 4, ("U", "In"): 6, ("In", "In"): 4},
        "U1": {("U", "Rh"): 5, ("U", "In"): 6},
        "Rh1": {("Rh", "In"): 3, ("U", "Rh"): 6},
        "Rh2": {("Rh", "In"): 6, ("U", "Rh"): 3},
    }


@pytest.mark.now
def test_CN_bond_counts_by_best_methods_sorted_by_mendeleev(cif_URhIn):
    result = cif_URhIn.CN_bond_count_by_best_methods_sorted_by_mendeleev
    print(result)
    assert result == {
        "In1": {("Rh", "In"): 4, ("U", "In"): 6, ("In", "In"): 4},
        "U1": {("U", "Rh"): 5, ("U", "In"): 6, ("U", "U"): 6},
        "Rh1": {("Rh", "In"): 3, ("U", "Rh"): 6},
        "Rh2": {("Rh", "In"): 6, ("U", "Rh"): 3},
    }


"""Test bond fractions"""


@pytest.mark.fast
def test_CN_bond_fractions_by_min_dist_method(cif_URhIn):
    result = cif_URhIn.CN_bond_fractions_by_min_dist_method

    # Define the expected values directly as fractions where possible
    expected_fractions = {
        ("In", "In"): 4 / 43,
        ("In", "Rh"): 13 / 43,
        ("In", "U"): 12 / 43,
        ("Rh", "U"): 14 / 43,
    }

    for key, expected_value in expected_fractions.items():
        assert result[key] == pytest.approx(expected_value, abs=1e-3)


@pytest.mark.fast
def test_CN_bond_fractions_by_best_methods(cif_URhIn):
    result = cif_URhIn.CN_bond_fractions_by_best_methods

    # Define the expected values directly as fractions where possible
    expected_fractions = {
        ("In", "In"): 4 / 49,
        ("In", "Rh"): 13 / 49,
        ("In", "U"): 12 / 49,
        ("Rh", "U"): 14 / 49,
        ("U", "U"): 6 / 49,
    }

    for key, expected_value in expected_fractions.items():
        assert result[key] == pytest.approx(expected_value, abs=1e-3)


@pytest.mark.now
def test_CN_bond_fractions_by_min_dist_method_sorted_by_mendeleev(cif_URhIn):
    result = cif_URhIn.CN_bond_fractions_by_min_dist_method_sorted_by_mendeleev

    # Define the expected values directly as fractions where possible
    expected_fractions = {
        ("In", "In"): 4 / 43,
        ("Rh", "In"): 13 / 43,
        ("U", "In"): 12 / 43,
        ("U", "Rh"): 14 / 43,
    }

    # URhIn
    for key, expected_value in expected_fractions.items():
        assert result[key] == pytest.approx(expected_value, abs=1e-3)


@pytest.mark.now
def test_CN_bond_fractions_by_best_methods_sorted_by_mendeleeve(cif_URhIn):
    result = cif_URhIn.CN_bond_fractions_by_best_methods_sorted_by_mendeleev

    # Define the expected values directly as fractions where possible
    expected_fractions = {
        ("In", "In"): 4 / 49,
        ("Rh", "In"): 13 / 49,
        ("U", "In"): 12 / 49,
        ("U", "Rh"): 14 / 49,
        ("U", "U"): 6 / 49,
    }

    for key, expected_value in expected_fractions.items():
        assert result[key] == pytest.approx(expected_value, abs=1e-3)


@pytest.mark.fast
def test_CN_unique_values_by_min_dist_method(cif_URhIn):
    expected = {14, 9, 11}
    result = cif_URhIn.CN_unique_values_by_min_dist_method
    assert result == expected


@pytest.mark.fast
def test_CN_unique_values_by_best_methods(cif_URhIn):
    expected = {14, 9, 17}
    result = cif_URhIn.CN_unique_values_by_best_methods
    assert result == expected


@pytest.mark.fast
def test_CN_avg_by_min_dist_method(cif_URhIn):
    result = cif_URhIn.CN_avg_by_min_dist_method
    assert result == 10.75


@pytest.mark.fast
def test_CN_avg_by_best_methods(cif_URhIn):
    result = cif_URhIn.CN_avg_by_best_methods
    assert result == 12.25


@pytest.mark.fast
def test_CN_max_by_dist_method(cif_URhIn):
    assert cif_URhIn.CN_max_by_min_dist_method == 14


@pytest.mark.fast
def test_CN_max_by_best_methods(cif_URhIn):
    assert cif_URhIn.CN_max_by_best_methods == 17


@pytest.mark.fast
def test_CN_min_by_dist_method(cif_URhIn):
    assert cif_URhIn.CN_min_by_min_dist_method == 9


@pytest.mark.fast
def test_CN_min_by_best_methods(cif_URhIn):
    assert cif_URhIn.CN_min_by_best_methods == 9


@pytest.mark.fast
def test_get_polyhedron_labels_by_CN_min_dist_method(cif_URhIn):
    (
        polyhedron_points,
        labels,
    ) = cif_URhIn.get_polyhedron_labels_by_CN_min_dist_method("U1")
    assert len(polyhedron_points) == 12  # including the central atom
    assert len(labels) == 12  # including the central atom


@pytest.mark.fast
def test_get_polyhedron_labels_by_CN_best_methods(cif_URhIn):
    (
        polyhedron_points,
        labels,
    ) = cif_URhIn.get_polyhedron_labels_by_CN_best_methods("U1")
    assert len(polyhedron_points) == 18  # including the central atom
    assert len(labels) == 18  # including the central atom


"""
Test
polyhedron
"""


def test_plot_polyhedron_default_output_folder(cif_URhIn):
    # Define the directory to store the output
    expected_output_dir = "tests/data/cif/polyhedrons"
    output_file_path = os.path.join(expected_output_dir, "URhIn_In1.png")

    # Define the output file path
    cif_URhIn.plot_polyhedron("In1")

    assert os.path.exists(output_file_path)
    assert os.path.getsize(output_file_path) > 1024
    shutil.rmtree(expected_output_dir)


def test_plot_polyhedron_with_output_folder_given(cif_URhIn):
    # Define the directory to store the output
    expected_output_dir = "tests/data/cif/polyhedrons_user"
    output_file_path = os.path.join(expected_output_dir, "URhIn_In1.png")

    # Define the output file path
    cif_URhIn.plot_polyhedron(
        "In1", is_displayed=False, output_dir="tests/data/cif/polyhedrons_user"
    )

    assert os.path.exists(output_file_path)
    assert os.path.getsize(output_file_path) > 1024

    shutil.rmtree(expected_output_dir)


def test_plot_polyhedrons(cif_ensemble_test):
    # Define the directory to store the output
    expected_output_dir = "tests/data/cif/ensemble_test/polyhedrons"
    # Ensure the directory exists

    cifs = cif_ensemble_test.cifs
    for cif in cifs:
        labels = cif.site_labels
        for label in labels:
            cif.plot_polyhedron(label, show_labels=True)

    # Check the number of files
    image_file_count = folder.get_file_count(expected_output_dir, ".png")
    assert image_file_count == 12

    shutil.rmtree(expected_output_dir)


"""
Test error during init
"""


def test_init_error_duplicate_label():
    file_path = "tests/data/cif/error/duplicate_labels/457848.cif"
    with pytest.raises(ValueError) as e:
        Cif(file_path)

    expected_error_message = CifParserError.DUPLICATE_LABELS.value
    assert expected_error_message == str(e.value)


def test_init_error_coord_missing():
    file_path = "tests/data/cif/error/missing_loop/452743.cif"
    with pytest.raises(ValueError) as e:
        Cif(file_path)
    expected_error_message = CifParserError.WRONG_LOOP_VALUE_COUNT.value
    assert expected_error_message == str(e.value)


"""
Test files without radius values
"""


@pytest.mark.fast
def test_init_without_radius_data():
    file_path = "tests/data/cif/no_radius_data/EuO.cif"
    cif = Cif(file_path)
    assert cif.is_radius_data_available == False
    assert cif.radius_sum == None
    assert cif.radius_values == None
    assert cif.CN_bond_count_by_best_methods == {
        "Eu": {("Eu", "O"): 6},
        "O": {("Eu", "O"): 6},
    }