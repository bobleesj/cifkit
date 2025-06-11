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

    radius_opt._generate_element_pairs([A, B]) == [
        ("Dy", "Dy"),
        ("Dy", "Co"),
        ("Co", "Co"),
    ]
    # This is confirmed with Oliynyk's video
    shortest_bond_pair_distance = {
        ("Dy", "Dy"): 4.06,
        ("Co", "Co"): 2.363,
        ("Dy", "Co"): 2.782,
    }

    result = radius_opt.get_refined_CIF_radius(
        [A, B], shortest_bond_pair_distance
    )

    assert (
        DeepDiff(
            result,
            {
                "Dy": np.float64(1.6062119417614027),
                "Co": np.float64(1.1757880582385976),
            },
            significant_digits=4,
        )
        == {}
    )

def test_ternary_refined_radius():
    R = "U"
    M = "Rh"
    X = "In"
    assert radius.value("U") == {"CIF": 1.377, "Pauling_CN12": 1.516}
    assert radius.value("Rh") == {"CIF": 1.345, "Pauling_CN12": 1.342}
    assert radius.value("In") == {"CIF": 1.624, "Pauling_CN12": 1.66}

    shortest_bond_pair_distance = {
        ("U", "U"): 3.881,
        ("U", "Rh"): 2.983,
        ("In", "In"): 3.244,
        ("Rh", "In"): 2.697,
        ("U", "In"): 3.21,
        ("Rh", "Rh"): 3.881,
    }
    optimized_radii = radius_opt.get_refined_CIF_radius(
        [R, M, X], shortest_bond_pair_distance
    )
    # Setting constraint for U-Rh with distance 2.983
    # Setting constraint for Rh-In with distance 2.697
    diff = DeepDiff(
        optimized_radii,
        {
            "U": np.float64(1.6143481586494364),
            "Rh": np.float64(1.3686518413505637),
            "In": np.float64(1.3283481586494363),
        },
        significant_digits=4,
    )
    assert diff == {}
