import logging
import os
import shutil

import pytest
from deepdiff import DeepDiff

from cifkit import Cif
from cifkit.utils.error_messages import CifParserError


@pytest.mark.fast
def test_cif_static_properties(cif_URhIn):
    assert cif_URhIn.file_path == "tests/data/cif/URhIn.cif"
    assert cif_URhIn.file_name == "URhIn.cif"
    assert cif_URhIn.file_name_without_ext == "URhIn"
    assert cif_URhIn.unique_elements == {"In", "Rh", "U"}
    assert cif_URhIn.composition_type == 3
    assert cif_URhIn.formula == "URhIn"
    assert cif_URhIn.structure == "ZrNiAl"
    assert cif_URhIn.db_source == "PCD"
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
def test_init_no_log(caplog):
    file_path = "tests/data/cif/URhIn.cif"
    Cif(file_path)

    with caplog.at_level(logging.INFO):
        assert caplog.text == ""


@pytest.mark.fast
def test_init_with_log(caplog):
    file_path = "tests/data/cif/URhIn.cif"

    with caplog.at_level(logging.INFO):
        cif = Cif(file_path, logging_enabled=True)
        assert "Preprocessing tests/data/cif/URhIn.cif" in caplog.text
        assert "Parsing .cif and generating supercell for URhIn.cif" in caplog.text

        cif.compute_connections()
        assert "Computing pair distances for URhIn.cif" in caplog.text


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


@pytest.mark.fast
def test_radius_values(cif_URhIn):
    actual_values = cif_URhIn.radius_values
    expected_values = {
        "In": {
            "CIF_radius": 1.487,
            "CIF_radius_refined": 1.328,
            "Pauling_radius_CN12": 1.66,
        },
        "Rh": {
            "CIF_radius": 1.345,
            "CIF_radius_refined": 1.369,
            "Pauling_radius_CN12": 1.342,
        },
        "U": {
            "CIF_radius": 1.377,
            "CIF_radius_refined": 1.614,
            "Pauling_radius_CN12": 1.516,
        },
    }

    for element, radii in actual_values.items():
        for radius_type, actual in radii.items():
            expected = expected_values[element][radius_type]
            assert actual == pytest.approx(expected, abs=0.001)


@pytest.mark.fast
def test_radius_sum_data(cif_URhIn):
    # Tested Jun 11, 2025
    actual_sum = cif_URhIn.radius_sum
    expected_sum = {
        "CIF_radius_sum": {
            "In-In": 3.248,
            "In-Rh": 2.969,
            "In-U": 3.001,
            "Rh-Rh": 2.69,
            "Rh-U": 2.722,
            "U-U": 2.754,
        },
        "CIF_radius_refined_sum": {
            "In-In": 2.656,
            "In-Rh": 2.697,
            "In-U": 2.942,
            "Rh-Rh": 2.738,
            "Rh-U": 2.983,
            "U-U": 3.228,
        },
        "Pauling_radius_sum": {
            "In-In": 3.32,
            "In-Rh": 3.002,
            "In-U": 3.176,
            "Rh-Rh": 2.684,
            "Rh-U": 2.858,
            "U-U": 3.032,
        },
    }
    print("Actual sum:", actual_sum)
    diff = DeepDiff(actual_sum, expected_sum, significant_digits=3)
    assert diff == {}


@pytest.mark.fast
def test_CN_max_gap_per_site(cif_URhIn, max_gaps_per_label_URhIn):
    cif_URhIn.compute_CN()
    result = cif_URhIn.CN_max_gap_per_site
    for label, dist_types in max_gaps_per_label_URhIn.items():
        for dist_type, values in dist_types.items():
            assert result[label][dist_type]["CN"] == values["CN"]
            assert result[label][dist_type]["max_gap"] == pytest.approx(
                values["max_gap"], abs=0.00101
            )


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


@pytest.mark.slow
def test_CN_bond_counts_by_min_dist_method(cif_URhIn):
    result = cif_URhIn.CN_bond_count_by_min_dist_method

    assert result == {
        "In1": {("In", "In"): 4, ("In", "Rh"): 4, ("In", "U"): 6},
        "Rh1": {("In", "Rh"): 3, ("Rh", "U"): 6},
        "Rh2": {("In", "Rh"): 6, ("Rh", "U"): 3},
        "U1": {("In", "U"): 6, ("Rh", "U"): 5},
    }


@pytest.mark.slow
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


@pytest.mark.slow
def test_CN_bond_counts_by_min_dist_method_sorted_by_mendeleev(cif_URhIn):
    result = cif_URhIn.CN_bond_count_by_min_dist_method_sorted_by_mendeleev
    assert result == {
        "In1": {("Rh", "In"): 4, ("U", "In"): 6, ("In", "In"): 4},
        "U1": {("U", "Rh"): 5, ("U", "In"): 6},
        "Rh1": {("Rh", "In"): 3, ("U", "Rh"): 6},
        "Rh2": {("Rh", "In"): 6, ("U", "Rh"): 3},
    }


@pytest.mark.slow
def test_CN_bond_counts_by_best_methods_sorted_by_mendeleev(cif_URhIn):
    result = cif_URhIn.CN_bond_count_by_best_methods_sorted_by_mendeleev
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


@pytest.mark.slow
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


@pytest.mark.slow
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
Test polyhedron
"""


@pytest.mark.pyvista
def test_plot_polyhedron_default_output_folder(cif_URhIn):
    # Define the directory to store the output
    expected_output_dir = "tests/data/cif/polyhedrons"
    output_file_path = os.path.join(expected_output_dir, "URhIn_In1.png")

    # Define the output file path
    cif_URhIn.plot_polyhedron("In1")

    assert os.path.exists(output_file_path)
    assert os.path.getsize(output_file_path) > 1024
    shutil.rmtree(expected_output_dir)


@pytest.mark.pyvista
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


"""
Test init
"""


def test_init_cif_with_CN_computed():
    file_path = "tests/data/cif/URhIn.cif"
    cif = Cif(file_path, compute_CN=True, supercell_size=2)
    assert cif.CN_bond_count_by_best_methods == {
        "In1": {("In", "Rh"): 4, ("In", "U"): 6, ("In", "In"): 4},
        "U1": {("Rh", "U"): 5, ("In", "U"): 6, ("U", "U"): 6},
        "Rh1": {("In", "Rh"): 3, ("Rh", "U"): 6},
        "Rh2": {("In", "Rh"): 6, ("Rh", "U"): 3},
    }


"""
Test init error
"""


@pytest.mark.fast
def test_init_error_duplicate_label():
    file_path = "tests/data/cif/error/duplicate_labels/457848.cif"
    with pytest.raises(ValueError) as e:
        Cif(file_path)

    expected_error_message = CifParserError.DUPLICATE_LABELS.value
    assert expected_error_message == str(e.value)


@pytest.mark.fast
def test_init_error_coord_missing():
    file_path = "tests/data/cif/error/missing_loop/452743.cif"
    with pytest.raises(ValueError) as e:
        Cif(file_path)

    assert "contains no atomic label and type." in str(e.value)


"""
Test files that is not full occupancy
"""


def test_init_atomic_mixing_deficiency_without_atomic_mixing():
    file_path = "tests/data/cif/cif_CN_init/1956508.cif"
    cif = Cif(file_path)
    cif.compute_CN()
    assert cif.CN_unique_values_by_best_methods == {11, 14, 15}


"""
Test files with error in geometry
"""


def print_connected_points(all_labels_connections):
    """Utility function for printing connections per site label."""
    for label, connections in all_labels_connections.items():
        print(f"\nAtom site {label}:")
        for (
            label,
            dist,
            coords_1,
            coords_2,
        ) in connections:
            print(f"{label} {dist} {coords_1}, {coords_2}")


@pytest.mark.pyvista
def test_init_atomic_mixing():
    file_path = "tests/data/cif/atomic_mixing/261241.cif"
    cif = Cif(file_path)
    cif.compute_CN()
    polyhedron_points, vertex_labels = cif.get_polyhedron_labels_by_CN_best_methods(
        "CoM1"
    )
    assert len(polyhedron_points) == 13
    assert len(vertex_labels) == 13


"""
Test file without mendeeleve number
"""


@pytest.mark.fast
def test_init_without_mendeeleve_number():
    file_path = "tests/data/cif/cif_no_mendeleev/454169.cif"
    cif = Cif(file_path)
    assert cif.unique_elements == {"Pu", "Ga"}
    assert cif.bond_pairs == {("Pu", "Pu"), ("Ga", "Pu"), ("Ga", "Ga")}
    assert cif.bond_pairs_sorted_by_mendeleev == {
        ("Pu", "Pu"),
        ("Pu", "Ga"),
        ("Ga", "Ga"),
    }


"""
Test CIF various db sources
"""


@pytest.mark.parametrize(
    "file_path, expected_db_source, expected_elements, expected_atom_count",
    [
        (
            "tests/data/cif/sources/ICSD/EntryWithCollCode43054.cif",
            "ICSD",
            {"Fe", "Ge"},
            216,
        ),
        ("tests/data/cif/sources/MS/U13Rh4.cif", "MS", {"U", "Fe"}, 2988),
        ("tests/data/cif/sources/MS/U13Rh4.cif", "MS", {"U", "Fe"}, 2988),
        ("tests/data/cif/sources/COD/1010581.cif", "COD", {"Cu", "Se"}, 1383),
        (
            "tests/data/cif/sources/CCDC/2294753.cif",
            "CCDC",
            {"Er", "In", "Co"},
            3844,
        ),
        (
            "tests/data/cif/sources/MP/LiFeP2O7.cif",
            "MP",
            {"Fe", "Li", "O", "P"},
            594,
        ),
    ],
)
@pytest.mark.now
def test_init_cif_file(
    tmpdir,
    file_path,
    expected_db_source,
    expected_elements,
    expected_atom_count,
):
    copied_file_path = os.path.join(tmpdir, os.path.basename(file_path))
    shutil.copyfile(file_path, copied_file_path)
    cif = Cif(copied_file_path, supercell_size=2)

    # Perform assertions
    assert cif.db_source == expected_db_source
    assert cif.unique_elements == expected_elements
    assert cif.supercell_atom_count == expected_atom_count
