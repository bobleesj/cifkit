import pytest

from cifkit.data.radius_optimization import get_refined_CIF_radius


def test_optimization(cif_URhIn):
    # Example usage:
    elements_sorted = sorted(cif_URhIn.unique_elements)
    assert elements_sorted == ["In", "Rh", "U"]
    assert cif_URhIn.shortest_bond_pair_distance == {
        ("In", "In"): 3.244,
        ("In", "Rh"): 2.697,  # RM
        ("In", "U"): 3.21,
        ("Rh", "Rh"): 3.881,
        ("Rh", "U"): 2.983,  # MX
        ("U", "U"): 3.881,
    }
    optimized_radii = get_refined_CIF_radius(
        elements_sorted, cif_URhIn.shortest_bond_pair_distance
    )
    expected_radii = {"U": 1.6143, "Rh": 1.3687, "In": 1.3283}
    assert optimized_radii == pytest.approx(expected_radii, abs=1e-3, rel=1e-3)
