def get_shortest_distance_per_bond_pair(
    flattened_connections: list[tuple[tuple[str, str], float]],
) -> dict[tuple[str, str], float]:
    """Determine the min distance for all possible unique pair of
    elements."""

    # Initialize the dictionary with a specific type
    min_dist_per_element_pair: dict[tuple[str, str], float] = {}
    for connection in flattened_connections:
        element_pair = connection[0]
        distance = connection[1]
        if (
            element_pair not in min_dist_per_element_pair
            or distance < min_dist_per_element_pair[element_pair]
        ):
            min_dist_per_element_pair[element_pair] = distance
    return min_dist_per_element_pair
