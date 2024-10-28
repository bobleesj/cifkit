from functools import partial

import numpy as np
from scipy.optimize import minimize

from cifkit.data.radius import get_radius_data


def generate_adjacent_pairs(
    elements: list[str],
) -> list[tuple[str, str]]:
    """Generate a list of tuples, where each tuple is a pair of adjacent atom
    labels."""

    # Binary -> [('In', 'Rh')]
    # Ternary -> [('In', 'Rh'), ('Rh', 'U')]
    label_to_pair = [
        (elements[i], elements[i + 1]) for i in range(len(elements) - 1)
    ]
    return label_to_pair


def objective(params, original_radii: list[float]) -> list[float]:
    """Calculate the objective function value,which is the sum of squared percent
    differences between original and refined radii."""

    return np.sum(((original_radii - params) / original_radii) ** 2)


def constraint(params, index_pair: tuple[int, int], shortest_distance: dict):
    """Enforce that the sum of the radii of the pair does not exceed the shortest
    allowed distance between them."""
    i, j = index_pair
    return shortest_distance - (params[i] + params[j])


def get_refined_CIF_radius(
    elements: list[str], shortest_distances: dict
) -> dict[str, float]:
    """Optimize CIF radii given atom labels and their shortest pair distance
    constraints."""
    sorted_elements = sorted(elements)
    radii_data = get_radius_data()
    original_radii = np.array(
        [radii_data[label]["CIF_radius"] for label in sorted_elements]
    )

    label_to_pair = generate_adjacent_pairs(sorted_elements)

    # Constraints setup
    constraints = []
    for pair in label_to_pair:
        dist = shortest_distances[pair]
        # print(
        #     f"Setting constraint for {pair[0]}-{pair[1]} with distance {dist}"
        # )
        i, j = sorted_elements.index(pair[0]), sorted_elements.index(pair[1])
        constraints.append(
            {
                "type": "eq",
                "fun": partial(
                    constraint,
                    index_pair=(i, j),
                    shortest_distance=dist,
                ),
            }
        )

    result = minimize(
        objective,
        original_radii,
        args=(original_radii,),
        constraints=constraints,
        options={"disp": False},
    )

    # if result.success:
    #     print("Optimization succeeded.")
    # else:
    #     print("Optimization failed:", result.message)

    return dict(zip(sorted_elements, result.x))
