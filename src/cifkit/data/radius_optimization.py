from functools import partial

import numpy as np
from bobleesj.utils.sources import radius
from scipy.optimize import minimize


def _generate_adjacent_pairs(
    elements: list[str],
) -> list[tuple[str, str]]:
    """Generate a list of tuples, where each tuple is a pair of adjacent atom
    labels.

    Examples
    --------
    >>> _generate_adjacent_pairs(["Dy", "Co"])
    [("Dy", "Co")]
    >>> )_generate_adjacent_pairs(["U", "Rh", "In"])
    [("U", "Rh"), ("Rh", "In")]
    """
    element_pairs = [
        (elements[i], elements[i + 1]) for i in range(len(elements) - 1)
    ]
    return element_pairs


def _objective(params, original_radii: list[float]) -> list[float]:
    """Calculate the objective function value, which is the sum of squared
    percent differences between original and refined radii."""
    return np.sum(((original_radii - params) / original_radii) ** 2)


def _constraint(params, index_pair: tuple[int, int], shortest_distance: dict):
    """Enforce that the sum of the radii of the pair does not exceed the
    shortest allowed distance between them."""
    i, j = index_pair
    return shortest_distance - (params[i] + params[j])


def get_refined_CIF_radius(
    elements: list[str], shortest_distances: dict
) -> dict[str, float]:
    """Optimize CIF radii given elements and their shortest pair distance
    constraints."""
    radii_data = radius.data()
    original_radii = np.array(
        [radii_data[element]["CIF"] for element in elements]
    )
    element_pairs = _generate_adjacent_pairs(elements)
    # Constraints setup
    constraints = []
    for pair in element_pairs:
        print("Setting constraint for", pair)
        # Get the shortest distance for the pair, considering both orders
        dist = shortest_distances.get(pair) or shortest_distances.get(
            (pair[1], pair[0])
        )
        print(
            f"Setting constraint for {pair[0]}-{pair[1]} with distance {dist}"
        )
        i, j = elements.index(pair[0]), elements.index(pair[1])
        constraints.append(
            {
                "type": "eq",
                "fun": partial(
                    _constraint,
                    index_pair=(i, j),
                    shortest_distance=dist,
                ),
            }
        )
    result = minimize(
        _objective,
        original_radii,
        args=(original_radii,),
        constraints=constraints,
        options={"disp": False},
    )
    if result.success:
        print("CIF radius optimization succeeded.")
    else:
        print("CIF radius optimization failed:", result.message)
    return dict(zip(elements, result.x)), result.fun
