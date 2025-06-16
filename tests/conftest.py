import pytest

from cifkit import Cif, CifEnsemble
from cifkit.coordination import composition, filter
from cifkit.preprocessors import environment, environment_util, supercell
from cifkit.utils import cif_parser, folder


@pytest.fixture
def cif_CUMNON_sb() -> Cif:
    return Cif("tests/data/cifs/CUMNON01_sb_only.cif")


@pytest.fixture
def Dy2Co17_cif() -> Cif:
    cif = Cif("tests/data/cif/radius/binary/Dy2Co17.cif")
    return cif


@pytest.fixture
def Tb4RhInGe4_cif() -> Cif:
    cif = Cif("tests/data/cif/radius/quaternary/Tb4RhInGe4.cif", supercell_size=2)
    return cif


"""
CifEnsemble - histogram test
"""


@pytest.fixture(scope="module")
def cif_ensemble_histogram_test() -> CifEnsemble:
    return CifEnsemble("tests/data/cif/histogram", supercell_size=2)


"""
CifEnsemble - test folder
"""


@pytest.fixture(scope="module")
def cif_ensemble_test() -> CifEnsemble:
    return CifEnsemble("tests/data/cif/ensemble_test", supercell_size=2)


# Folder
@pytest.fixture(scope="module")
def cif_folder_path_test():
    return "tests/data/cif/folder"


# Multiple files
@pytest.fixture(scope="module")
def parsed_formula_weight_structure_s_group_data(
    cif_folder_path_test,
):
    results = cif_parser.get_unique_formulas_structures_weights_s_groups(
        cif_folder_path_test
    )
    return results


@pytest.fixture(scope="module")
def file_paths_test(cif_folder_path_test):
    return folder.get_file_paths(cif_folder_path_test)


"""
Cif - ICSD demo file
"""


@pytest.fixture(scope="module")
def file_path_ICSD_formatted():
    return "tests/data/cif/sources/ICSD/EntryWithCollCode43054_formatted.cif"


"""
Cif - URhIn
"""


@pytest.fixture(scope="module")
def file_path_URhIn():
    return "tests/data/cif/URhIn.cif"


@pytest.fixture(scope="module")
def formula_URhIn():
    return "URhIn"


@pytest.fixture(scope="module")
def cif_block_URhIn(file_path_URhIn):
    return cif_parser.get_cif_block(file_path_URhIn)


@pytest.fixture(scope="module")
def unique_site_labels_URhIn(loop_values_URhIn):
    return cif_parser.get_unique_site_labels(loop_values_URhIn)


@pytest.fixture(scope="module")
def loop_values_URhIn(cif_block_URhIn):
    return cif_parser.get_loop_values(cif_block_URhIn)


@pytest.fixture(scope="module")
def unitcell_coords_URhIn(cif_block_URhIn):
    return supercell.get_unitcell_coords_for_all_labels(cif_block_URhIn)


@pytest.fixture(scope="module")
def unitcell_points_URhIn(cif_block_URhIn):
    return supercell.get_supercell_points(cif_block_URhIn, 1)


@pytest.fixture(scope="module")
def supercell_points_URhIn(cif_block_URhIn):
    return supercell.get_supercell_points(cif_block_URhIn, 2)


@pytest.fixture(scope="module")
def lenghts_URhIn(cif_block_URhIn) -> list[float]:
    lengths = cif_parser.get_unitcell_lengths(cif_block_URhIn)
    return lengths


@pytest.fixture(scope="module")
def angles_rad_URhIn(cif_block_URhIn) -> list[float]:
    angles_rad = cif_parser.get_unitcell_angles_rad(cif_block_URhIn)
    return angles_rad


@pytest.fixture(scope="module")
def site_labels_URhIn(loop_values_URhIn):
    return cif_parser.get_unique_site_labels(loop_values_URhIn)


@pytest.fixture(scope="module")
def parsed_cif_data_URhIn(
    unique_site_labels_URhIn, lenghts_URhIn, angles_rad_URhIn
) -> tuple[list[str], list[float], list[float]]:
    return (unique_site_labels_URhIn, lenghts_URhIn, angles_rad_URhIn)


@pytest.fixture(scope="module")
def radius_data_URhIn() -> dict:
    return {
        "In": {
            "CIF_radius": 1.624,
            "CIF_radius_refined": 1.3283,
            "Pauling_radius_CN12": 1.66,
        },
        "Rh": {
            "CIF_radius": 1.345,
            "CIF_radius_refined": 1.3687,
            "Pauling_radius_CN12": 1.342,
        },
        "U": {
            "CIF_radius": 1.377,
            "CIF_radius_refined": 1.6143,
            "Pauling_radius_CN12": 1.516,
        },
    }


@pytest.fixture(scope="module")
def radius_sum_data_URhIn() -> dict:
    return {
        "CIF_radius_sum": {
            "In-In": 3.248,
            "In-Rh": 2.969,
            "In-U": 3.001,
            "Rh-Rh": 2.69,
            "Rh-U": 2.722,
            "U-U": 2.754,
        },
        "CIF_radius_refined_sum": {
            "In-In": 2.657,
            "In-Rh": 2.697,
            "In-U": 2.943,
            "Rh-Rh": 2.737,
            "Rh-U": 2.983,
            "U-U": 3.229,
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


@pytest.fixture(scope="module")
def cif_URhIn(file_path_URhIn):
    return Cif(file_path_URhIn, supercell_size=2)


@pytest.fixture(scope="module")
def connections_URhIn(
    parsed_cif_data_URhIn,
    unitcell_points_URhIn,
    supercell_points_URhIn,
):
    return environment.get_site_connections(
        parsed_cif_data_URhIn,
        unitcell_points_URhIn,
        supercell_points_URhIn,
        cutoff_radius=10.0,
    )


@pytest.fixture(scope="module")
def flattened_connections_URhIn(connections_URhIn):
    return environment_util.flat_site_connections(connections_URhIn)


@pytest.fixture(scope="module")
def bond_counts_CN(cif_URhIn, CN_connections_by_min_dist_URhIn):
    return composition.get_bond_counts(
        cif_URhIn.unique_elements, CN_connections_by_min_dist_URhIn
    )


@pytest.fixture(scope="module")
def max_gaps_per_label_URhIn():
    return {
        "In1": {
            "dist_by_shortest_dist": {"max_gap": 0.306, "CN": 14},
            "dist_by_CIF_radius_sum": {"max_gap": 0.39, "CN": 14},
            "dist_by_CIF_radius_refined_sum": {
                "max_gap": 0.341,
                "CN": 12,
            },
            "dist_by_Pauling_radius_sum": {
                "max_gap": 0.398,
                "CN": 14,
            },
        },
        "U1": {
            "dist_by_shortest_dist": {"max_gap": 0.197, "CN": 11},
            "dist_by_CIF_radius_sum": {"max_gap": 0.312, "CN": 11},
            "dist_by_CIF_radius_refined_sum": {
                "max_gap": 0.27,
                "CN": 17,
            },
            "dist_by_Pauling_radius_sum": {
                "max_gap": 0.256,
                "CN": 17,
            },
        },
        "Rh1": {
            "dist_by_shortest_dist": {"max_gap": 0.315, "CN": 9},
            "dist_by_CIF_radius_sum": {"max_gap": 0.347, "CN": 9},
            "dist_by_CIF_radius_refined_sum": {
                "max_gap": 0.418,
                "CN": 9,
            },
            "dist_by_Pauling_radius_sum": {"max_gap": 0.402, "CN": 9},
        },
        "Rh2": {
            "dist_by_shortest_dist": {"max_gap": 0.31, "CN": 9},
            "dist_by_CIF_radius_sum": {"max_gap": 0.324, "CN": 9},
            "dist_by_CIF_radius_refined_sum": {
                "max_gap": 0.397,
                "CN": 9,
            },
            "dist_by_Pauling_radius_sum": {"max_gap": 0.380, "CN": 9},
        },
    }


@pytest.fixture(scope="module")
def CN_connections_by_min_dist_URhIn(max_gaps_per_label_URhIn, connections_URhIn):
    return filter.get_CN_connections_by_min_dist_method(
        max_gaps_per_label_URhIn, connections_URhIn
    )


@pytest.fixture(scope="module")
def CN_bond_count_by_min_dist_method():
    return {
        "In1": {("In", "In"): 4, ("In", "Rh"): 4, ("In", "U"): 6},
        "Rh1": {("In", "Rh"): 3, ("Rh", "U"): 6},
        "Rh2": {("In", "Rh"): 6, ("Rh", "U"): 3},
        "U1": {("In", "U"): 6, ("Rh", "U"): 5},
    }


@pytest.fixture(scope="module")
def CN_bond_count_by_best_methods():
    return {
        "In1": {("In", "In"): 4, ("In", "Rh"): 4, ("In", "U"): 6},
        "Rh1": {("In", "Rh"): 3, ("Rh", "U"): 6},
        "Rh2": {("In", "Rh"): 6, ("Rh", "U"): 3},
        "U1": {
            ("In", "U"): 6,
            ("Rh", "U"): 5,
            ("U", "U"): 6,
        },
    }
