import numpy as np

from cifkit.utils.string_parser import get_atom_type_from_label


def flat_site_connections(
    site_connections: dict,
) -> list[tuple[tuple[str, str], float]]:
    """Transform site connections into a sorted list of tuples, each
    containing a pair of alphabetically distance."""
    flattened_points = []
    for site_label, connections in site_connections.items():
        for connection in connections:
            other_site_label = connection[0]
            distance = float(connection[1])
            site_element = get_atom_type_from_label(site_label)
            other_site_element = get_atom_type_from_label(other_site_label)
            # Sort the site label and other site label alphabetically
            bond_pair = tuple(sorted((site_element, other_site_element)))
            flattened_points.append((bond_pair, distance))

    # Sort primarily by distance, secondarily by element pair
    flattened_points.sort(key=lambda x: (x[1], x[0]))
    return flattened_points


def calculate_normalized_distances(connections):
    """Calculate normalized distances for each connection."""
    min_dist = connections[0][1]
    normalized_distances = [
        float(np.round(dist / min_dist, 3)) for _, dist, _, _ in connections
    ]
    return normalized_distances


def calculate_normalized_dist_diffs(normalized_distances):
    """Calculate differences between consecutive normalized
    distances."""
    normalized_dist_diffs = [
        normalized_distances[k + 1] - normalized_distances[k]
        for k in range(len(normalized_distances) - 1)
    ]
    return normalized_dist_diffs
