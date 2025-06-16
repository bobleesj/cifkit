import numpy as np
import pytest
from bobleesj.utils.sources import radius
from deepdiff import DeepDiff

from cifkit.data import radius_optimization as radius_opt


def test_binary_refined_radius():
    # All expected values are from Oliynyk's video
    A = "Dy"
    B = "Co"
    assert radius.value("Dy") == {"CIF": 1.752, "Pauling_CN12": 1.77}
    assert radius.value("Co") == {"CIF": 1.25, "Pauling_CN12": 1.252}

    # This is confirmed with Oliynyk's video
    shortest_bond_pair_distance = {
        ("Dy", "Dy"): 4.06,
        ("Co", "Co"): 2.363,
        ("Dy", "Co"): 2.782,
    }
    optimized_radii, obj_value = radius_opt.get_refined_CIF_radius(
        [A, B], shortest_bond_pair_distance, elements_ordered=False
    )
    print(optimized_radii)
    diff = DeepDiff(
        optimized_radii,
        {
            "Dy": np.float64(1.6062119417614027),
            "Co": np.float64(1.1757880582385976),
        },
        significant_digits=3,
    )

    assert diff == {}
    assert obj_value == pytest.approx(0.010449041063004245, abs=1e-2)


@pytest.mark.parametrize(
    "shortest_bond_pair_distance",
    [
        {
            ("U", "U"): 3.881,
            ("U", "Rh"): 2.983,
            ("In", "In"): 3.244,
            ("Rh", "In"): 2.697,
            ("U", "In"): 3.21,
            ("Rh", "Rh"): 3.881,
        },
        {
            ("In", "In"): 3.244,
            ("In", "Rh"): 2.697,
            ("In", "U"): 3.21,
            ("Rh", "Rh"): 3.881,
            ("Rh", "U"): 2.983,
            ("U", "U"): 3.881,
        },
    ],
)
def test_ternary_refined_radius_parametrized(shortest_bond_pair_distance):
    R = "U"
    M = "Rh"
    X = "In"

    assert radius.value("U") == {"CIF": 1.377, "Pauling_CN12": 1.516}
    assert radius.value("Rh") == {"CIF": 1.345, "Pauling_CN12": 1.342}
    assert radius.value("In") == {"CIF": 1.624, "Pauling_CN12": 1.66}

    optimized_radii, obj_value = radius_opt.get_refined_CIF_radius(
        [R, M, X], shortest_bond_pair_distance, elements_ordered=False
    )

    print("Optimized Radii:")
    print(optimized_radii)
    expected_radii = {
        "U": np.float64(1.486946039959839),
        "Rh": np.float64(1.3559562114475352),
        "In": np.float64(1.4870460399593393),
    }

    diff = DeepDiff(optimized_radii, expected_radii, significant_digits=3)
    assert diff == {}
    assert obj_value == pytest.approx(0.013553279301314749, abs=1e-3)


def test_quaternary_refined_radius_parametrized(Tb4RhInGe4_cif):
    assert Tb4RhInGe4_cif.shortest_bond_pair_distance == {
        ("Ge", "Rh"): 2.47,
        ("Ge", "Ge"): 2.596,
        ("Ge", "In"): 2.818,
        ("Ge", "Tb"): 2.917,
        ("Rh", "Tb"): 3.076,
        ("Rh", "Rh"): 3.148,
        ("In", "Tb"): 3.367,
        ("Tb", "Tb"): 3.538,
        ("In", "In"): 4.264,
        ("In", "Rh"): 4.711,
    }

    A = "Tb"
    B = "Rh"
    C = "In"
    D = "Ge"

    assert radius.value("Tb") == {"CIF": 1.764, "Pauling_CN12": 1.773}
    assert radius.value("Rh") == {"CIF": 1.345, "Pauling_CN12": 1.342}
    assert radius.value("In") == {"CIF": 1.624, "Pauling_CN12": 1.66}
    assert radius.value("Ge") == {"CIF": 1.225, "Pauling_CN12": 1.366}

    optimized_radii, obj_value = radius_opt.get_refined_CIF_radius(
        [A, B, C, D],
        Tb4RhInGe4_cif.shortest_bond_pair_distance,
        elements_ordered=False,
    )
    expected_radii = {
        "Tb": np.float64(1.685319483724592),
        "Rh": np.float64(1.4210498719642057),
        "In": np.float64(1.6868162610695323),
        "Ge": np.float64(1.1597125276078235),
    }

    diff = DeepDiff(optimized_radii, expected_radii, significant_digits=4)
    assert diff == {}
    assert obj_value == pytest.approx(0.009523133315868711, abs=1e-6)


@pytest.mark.parametrize(
    "elements, expected_pairs",
    [
        (["Dy", "Co"], [("Dy", "Co")]),
        (["U", "Rh", "In"], [("U", "Rh"), ("Rh", "In")]),
    ],
)
def test_generate_adjacent_pairs(elements, expected_pairs):
    """Test the generation of adjacent element pairs."""
    result = radius_opt._generate_adjacent_pairs(elements)
    assert result == expected_pairs
