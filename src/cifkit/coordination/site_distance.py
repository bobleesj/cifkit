def get_shortest_distance(connections: dict) -> float:
    """Return the shortest distance in the supercell."""
    min_dist = float("inf")

    # Iterate over each site's connections in the dictionary
    for _, connection_data in connections.items():
        if connection_data[0][1] < min_dist:
            min_dist = connection_data[0][1]

    # Check if the found minimum distance is less than the threshold
    return min_dist


def get_shortest_distance_per_site(
    connections: dict,
) -> dict[str, tuple[str, float]]:
    """Calculate the shortest distance for each label."""
    shortest_dist_info: dict[str, tuple[str, float]] = {}

    for label, connections in connections.items():
        # Extract only the distances from each tuple
        shortest_dist = connections[0][0]
        connection_label = connections[0][1]

        # Find the shortest distance and add it to the result dictionary
        shortest_dist_info[label] = (shortest_dist, connection_label)

    return shortest_dist_info
