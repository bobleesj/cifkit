import numpy as np

from cifkit.utils import distance, unit


def get_site_connections(
    parsed_data: list[str],
    unitcell_points,
    supercell_points,
    cutoff_radius: float,
) -> dict:
    """Compute all pair distances per site label."""
    labels, lengths, angles = parsed_data

    all_labels_connections = {}
    for site_label in labels:
        filtered_unitcell_points = [
            point for point in unitcell_points if point[3] == site_label
        ]

        dist_result = get_nearest_dists_per_site(
            filtered_unitcell_points,
            supercell_points,
            cutoff_radius,
            lengths,
            angles,
        )

        dist_dict, dist_set = dist_result

        (
            label,
            connections,
        ) = get_most_connected_point_per_site(site_label, dist_dict, dist_set)

        all_labels_connections[label] = connections
    return remove_duplicate_connections(all_labels_connections)


def get_nearest_dists_per_site(
    filtered_unitcell_points,
    supercell_points,
    cutoff_radius: float,
    lengths,
    angles_rad,
):
    # Initialize a dictionary to store the relationships
    dist_dict = {}
    dist_set = set()

    # Loop through each point in the filtered list
    for i, point_1 in enumerate(filtered_unitcell_points):
        point_2_info = []
        for j, point_2 in enumerate(supercell_points):
            if point_1 == point_2:
                continue  # Skip comparison with itself
            # Convert fractional to Cartesian coordinates
            cart_1 = unit.fractional_to_cartesian(
                [point_1[0], point_1[1], point_1[2]],
                lengths,
                angles_rad,
            )
            cart_2 = unit.fractional_to_cartesian(
                [point_2[0], point_2[1], point_2[2]],
                lengths,
                angles_rad,
            )
            # Calculate the dist between two points
            dist = distance.calc_dist_two_cart_points(cart_1, cart_2)
            dist = float(np.round(dist, 3))
            # Check the dist
            if dist < cutoff_radius and dist > 0.1:
                point_2_info.append(
                    (
                        point_2[3],  # site label
                        dist,
                        [
                            float(np.round(cart_1[0], 3)),  # x
                            float(np.round(cart_1[1], 3)),  # y
                            float(np.round(cart_1[2], 3)),  # z
                        ],
                        [
                            float(np.round(cart_2[0], 3)),  # x
                            float(np.round(cart_2[1], 3)),  # y
                            float(np.round(cart_2[2], 3)),  # z
                        ],
                    )
                )
            dist_set.add(dist)
        # Store the list in the dictionary with `i` as the key
        if point_2_info:
            dist_dict[i] = point_2_info

    return dist_dict, dist_set


def get_most_connected_point_per_site(label: str, dist_dict: dict, dist_set: set):
    """Identify the reference point with the highest number of
    connections within the 50 shortest distances from a set of
    distances."""
    sorted_unique_dists = sorted(dist_set)
    shortest_dists = sorted_unique_dists[:50]
    # Variables to track the reference point with the highest count
    max_count = 0
    max_ref_point = None
    max_connections = []

    for ref_idx, connections in dist_dict.items():
        # Initialize a dictionary to count occurrences of each shortest
        dist_counts = {dist: 0 for dist in shortest_dists}

        # Count the occurrences of the shortest distances
        for _, dist, _, _ in connections:
            if dist in dist_counts:
                dist_counts[dist] += 1

        # Calculate the total count of occurrences for this reference point
        total_count = sum(dist_counts.values())

        # Check if this is the maximum we've encountered so far
        if total_count > max_count:
            max_count = total_count
            max_ref_point = ref_idx
            max_connections = sorted(connections, key=lambda x: x[1])

    # Return the max point
    if max_ref_point is not None:
        return label, [
            (other_label, dist, cart_1, cart_2)
            for other_label, dist, cart_1, cart_2 in max_connections
        ]


def remove_duplicate_connections(connections):
    """Remove duplicate connections based on the last set of
    coordinates."""
    unique_connections = {}
    for key, value in connections.items():
        seen = set()
        unique_list = []
        for item in value:
            # The tuple representing the endpoint coordinates is item[3]
            coords = tuple(item[3])  # Need to convert list to tuple to use it in a set
            if coords not in seen:
                seen.add(coords)
                unique_list.append(item)
        unique_connections[key] = unique_list
    return unique_connections
