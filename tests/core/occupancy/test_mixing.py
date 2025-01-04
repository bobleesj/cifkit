import pytest

from cifkit import Cif
from cifkit.occupancy.mixing import (
    compute_coord_occupancy_sum,
    frac_coordinates,
    get_mixing_type_per_pair_dict,
    get_site_mixing_type,
)


@pytest.mark.fast
def test_full_occupancy(cif_URhIn):
    file_mixing_type = get_site_mixing_type(
        cif_URhIn.site_labels, cif_URhIn.atom_site_info
    )
    assert file_mixing_type == "full_occupancy"


@pytest.mark.fast
def test_deficiency_without_atomic_mixing():
    cif = Cif("tests/data/cif/occupancy/527000.cif")
    file_mixing_type = get_site_mixing_type(cif.site_labels, cif.atom_site_info)
    assert file_mixing_type == "deficiency_without_atomic_mixing"


@pytest.mark.fast
def test_full_occupancy_atomic_mixing():
    cif = Cif("tests/data/cif/occupancy/529848.cif")
    file_mixing_type = get_site_mixing_type(cif.site_labels, cif.atom_site_info)
    assert file_mixing_type == "full_occupancy_atomic_mixing"


@pytest.mark.fast
def test_deficiency_and_atomic_mixing():
    cif = Cif("tests/data/cif/occupancy/554324.cif")
    file_mixing_type = get_site_mixing_type(cif.site_labels, cif.atom_site_info)
    assert file_mixing_type == "deficiency_atomic_mixing"


@pytest.mark.fast
def test_frac_coordinates(cif_URhIn):
    result = frac_coordinates(cif_URhIn.atom_site_info, "In1")
    assert result == (0.2505, 0.0, 0.5)

    result = frac_coordinates(cif_URhIn.atom_site_info, "U1")
    assert result == (0.5925, 0, 0)


@pytest.mark.fast
def test_compute_coord_occupancy_sum_deficiency_without_atomic_mixing():
    cif = Cif("tests/data/cif/occupancy/527000.cif")
    result = compute_coord_occupancy_sum(cif.site_labels, cif.atom_site_info)
    assert result == {
        (0.333333, 0.666667, 0.75): 0.38,
        (0.333333, 0.666667, 0.25): 1.0,
        (0.0, 0.0, 0.0): 1.0,
    }


@pytest.mark.fast
def test_compute_coord_occupancy_sum_full_occupancy_atomic_mixing():
    cif = Cif("tests/data/cif/occupancy/529848.cif")
    result = compute_coord_occupancy_sum(cif.site_labels, cif.atom_site_info)
    assert result == {(0.0, 0.0, 0.0): 1.0}


@pytest.mark.fast
def test_compute_coord_occupancy_sum_deficiency_and_atomic_mixing():
    cif = Cif("tests/data/cif/occupancy/554324.cif")
    result = compute_coord_occupancy_sum(cif.site_labels, cif.atom_site_info)
    assert result == {
        (0.333333, 0.666667, 0.75): 0.6,
        (0.333333, 0.666667, 0.25): 1.0,
        (0.0, 0.0, 0.0): 1.0,
    }


"""
Test atomic mixing between labels
"""


@pytest.mark.fast
def test_get_atom_site_mixing_dict_1():
    cif = Cif("tests/data/cif/occupancy/300160.cif")

    atom_site_pair_dict = get_mixing_type_per_pair_dict(
        cif.site_labels, cif.site_label_pairs, cif.atom_site_info
    )

    assert atom_site_pair_dict == {
        ("Rh1", "Rh1"): "full_occupancy",
        ("Ge1", "Ge1"): "full_occupancy",
        ("Ge1", "Sm1"): "full_occupancy",
        ("Rh1", "Sm1"): "full_occupancy",
        ("Sm1", "Sm1"): "full_occupancy",
        ("Ge1", "Rh1"): "full_occupancy",
    }


@pytest.mark.fast
def test_get_atom_site_mixing_dict_1_sorted_by_mendeleev():
    cif = Cif("tests/data/cif/occupancy/300160.cif")

    atom_site_pair_dict = get_mixing_type_per_pair_dict(
        cif.site_labels,
        cif.site_label_pairs_sorted_by_mendeleev,
        cif.atom_site_info,
    )

    # Mendeleev # - Ge 79, Rh 59, Sm 23
    assert atom_site_pair_dict == {
        ("Rh1", "Rh1"): "full_occupancy",
        ("Ge1", "Ge1"): "full_occupancy",
        ("Sm1", "Ge1"): "full_occupancy",
        ("Sm1", "Rh1"): "full_occupancy",
        ("Sm1", "Sm1"): "full_occupancy",
        ("Rh1", "Ge1"): "full_occupancy",
    }


@pytest.mark.fast
def test_get_atom_site_mixing_dict_2_sorted_by_mendeleev():
    """
    Pair: Rh2-Si 2.28 Å - deficiency_no_atomic_mixing
    Pair: Rh1-Rh1 2.524 Å - full_occupancy
    """

    cif = Cif("tests/data/cif/occupancy/527000.cif")

    data = get_mixing_type_per_pair_dict(
        cif.site_labels,
        cif.site_label_pairs_sorted_by_mendeleev,
        cif.atom_site_info,
    )
    # Mendeleev # - Rh 59, Si 78
    assert len(data) == 6
    assert data[("Rh1", "Si")] == "full_occupancy"
    assert data[("Rh1", "Rh1")] == "full_occupancy"
    assert data[("Rh1", "Rh2")] == "deficiency_without_atomic_mixing"
    assert data[("Rh2", "Rh2")] == "deficiency_without_atomic_mixing"
    assert data[("Si", "Si")] == "full_occupancy"
    assert data[("Rh2", "Si")] == "deficiency_without_atomic_mixing"


@pytest.mark.fast
def test_get_atom_site_mixing_dict_3_sorted_by_mendeleev():
    """
    Mendeleev # - Fe 55, Ge 79
    1831432.cif
    Fe Fe 8 b 0.375 0.375 0.375 0.01
    Ge1 Ge 8 a 0.125 0.125 0.125 0.944
    Fe2 Fe 8 a 0.125 0.125 0.125 0.056

    Result:
    Fe-Fe 2.448 deficiency,
    Fe-Ge 2.448 mixing-deficiency,
    Fe-Fe 2.448 mixing-deficiency
    """
    cif = Cif("tests/data/cif/occupancy/1831432.cif")

    data = get_mixing_type_per_pair_dict(
        cif.site_labels,
        cif.site_label_pairs_sorted_by_mendeleev,
        cif.atom_site_info,
    )
    assert len(data) == 6
    assert data[("Fe", "Fe")] == "deficiency_without_atomic_mixing"
    assert data[("Fe", "Fe2")] == "deficiency_with_atomic_mixing"

    assert data[("Fe", "Ge1")] == "deficiency_with_atomic_mixing"
    assert data[("Fe2", "Ge1")] == "full_occupancy_atomic_mixing"
    assert data[("Fe2", "Fe2")] == "full_occupancy_atomic_mixing"
    assert data[("Ge1", "Ge1")] == "full_occupancy_atomic_mixing"


@pytest.mark.fast
def test_get_atom_site_mixing_dict_4():
    """
    Mendeleev # - Ni 61, Sb 85
    529848.cif
    Ni1 Ni 4 a 0 0 0 0.92
    Sb2 Sb 4 a 0 0 0 0.08

    Result:
    529848: Ni-Sb 2.531 mixing
    """
    cif = Cif("tests/data/cif/occupancy/529848.cif")

    data = get_mixing_type_per_pair_dict(
        cif.site_labels,
        cif.site_label_pairs_sorted_by_mendeleev,
        cif.atom_site_info,
    )

    assert len(data) == 3
    assert data[("Ni1", "Ni1")] == "full_occupancy_atomic_mixing"
    assert data[("Sb2", "Sb2")] == "full_occupancy_atomic_mixing"
    assert data[("Ni1", "Sb2")] == "full_occupancy_atomic_mixing"


@pytest.mark.fast
def test_get_atom_site_mixing_dict_5():
    cif = Cif("tests/data/cif/occupancy/1617211.cif")

    data = get_mixing_type_per_pair_dict(
        cif.site_labels,
        cif.site_label_pairs_sorted_by_mendeleev,
        cif.atom_site_info,
    )

    assert len(data) == 6
    assert data[("Si1", "Si1")] == "full_occupancy"
    assert data[("Si1B", "Si1B")] == "deficiency_with_atomic_mixing"
    assert data[("Fe1A", "Fe1A")] == "deficiency_with_atomic_mixing"
    assert data[("Fe1A", "Si1")] == "deficiency_with_atomic_mixing"
    assert data[("Si1", "Si1B")] == "deficiency_with_atomic_mixing"
    assert data[("Fe1A", "Si1B")] == "deficiency_with_atomic_mixing"
