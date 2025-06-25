from functools import partial

import numpy as np
from bobleesj.utils.sources import radius
from scipy.optimize import minimize


def _generate_adjacent_pairs(
    elements: list[str],
) -> list[tuple[str, str]]:
    """Generate a list of tuples, where each tuple is a pair of adjacent
    atom labels.

    Examples
    --------
    >>> _generate_adjacent_pairs(["Dy", "Co"])
    [("Dy", "Co")]
    >>> )_generate_adjacent_pairs(["U", "Rh", "In"])
    [("U", "Rh"), ("Rh", "In")]
    """
    element_pairs = [(elements[i], elements[i + 1]) for i in range(len(elements) - 1)]
    return element_pairs


def _objective(params, original_radii: list[float]) -> list[float]:
    """Calculate the objective function value, which is the sum of
    squared percent differences between original and refined radii."""
    return np.sum(((original_radii - params) / original_radii) ** 2)


def _constraint(params, index_pair: tuple[int, int], shortest_distance: dict):
    """Enforce that the sum of the radii of the pair does not exceed the
    shortest allowed distance between them."""
    i, j = index_pair
    return shortest_distance - (params[i] + params[j])


def get_refined_CIF_radius(
    elements: list[str],
    shortest_distances: dict[tuple[str, str], float],
    elements_ordered=True,
    use_size_constraint=True,
) -> dict[str, float]:
    """Optimize CIF radii for a set of elements given (1) their adjacent
    pairwise distance constraints (2) size order of the original CIF
    radii.

    Parameters
    ----------
    elements : list[str]
        List of chemical element symbols to optimize radii for.
    shortest_distances : dict[tuple[str, str], float]
        Dictionary of shortest pairwise distances between element pairs.
        Keys should be tuples of two element symbols (e.g., ('Fe', 'Ge')).
    elements_ordered : bool, default True
        The elements will be sorted before processing.
        This affects how adjacency interatomic bond pairs is defined
        when generating element pairs.
    use_size_constraint : bool, default True
        Use the radius size order constraint. If True, the optimization
        will ensure that the refined radii maintain the original size order
        of the CIF radii. If False, this constraint is not applied.

    Returns
    -------
    dict[str, float]
        Dictionary mapping each element to its optimized CIF radius.
    float
        Value of the objective function (sum of squared deviations from original radii).
    """
    if elements_ordered:
        elements = sorted(elements)
    radius_data = radius.data()
    original_radii = np.array([radius_data[element]["CIF"] for element in elements])
    original_radii_dict = {elem: radius_data[elem]["CIF"] for elem in elements}
    index_map = {element: idx for idx, element in enumerate(elements)}
    element_pairs = _generate_adjacent_pairs(elements)
    # Set of constraints for interatomic distances
    # For ternary, it would be the distance between A-B and B-C pairs
    # For quaternary, it would be A-B, B-C, C-D pairs, etc.
    constraints = []
    for pair in element_pairs:
        # print("Setting constraint for", pair)
        # Get the shortest distance for the pair, considering both orders
        dist = shortest_distances.get(pair) or shortest_distances.get((pair[1], pair[0]))
        # print(f"Setting constraint for {pair[0]}-{pair[1]} with distance {dist}")
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
    # Another set of constraints that refined radii maintain the original size order.
    epsilon = 1e-4
    # Sort elements by original CIF radius (descending)
    ordered_by_size = sorted(
        elements, key=lambda el: original_radii_dict[el], reverse=True
    )

    # Helper to avoid lambda late binding
    def _make_inequality(i, j, epsilon=1e-4):
        return lambda x: x[i] - x[j] - epsilon

    if use_size_constraint:
        for e1, e2 in zip(ordered_by_size, ordered_by_size[1:]):
            i, j = index_map[e1], index_map[e2]
            constraints.append({"type": "ineq", "fun": _make_inequality(i, j, epsilon)})
    # Note, it appears that after the default iteration of 100 times, the
    # optimization does not converge but the results are still reasonable
    # with the low objective function value.
    result = minimize(
        _objective,
        original_radii,
        args=(original_radii,),
        constraints=constraints,
        options={
            "disp": True,
        },
    )
    # if result.success:
    #     print("CIF radius optimization succeeded.")
    #     print("Optimized radii:", result.x)
    #     print("Objective function value:", result.fun)
    # else:
    #     print("CIF radius optimization failed:", result.message)
    return dict(zip(elements, result.x)), float(result.fun)
