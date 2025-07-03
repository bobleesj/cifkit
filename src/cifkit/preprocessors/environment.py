import numpy as np

from cifkit.utils import unit


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
    # convert to cartesian
    filtered_unitcell_points_cart = []
    for x, y, z, label in filtered_unitcell_points:
        cx, cy, cz = unit.fractional_to_cartesian(
            [x, y, z],
            lengths,
            angles_rad,
        )
        filtered_unitcell_points_cart.append((cx, cy, cz, label))

    supercell_points_cart = []
    supercell_points_cart_labels = []
    for x, y, z, label in supercell_points:
        cx, cy, cz = unit.fractional_to_cartesian(
            [x, y, z],
            lengths,
            angles_rad,
        )
        supercell_points_cart.append((cx, cy, cz))
        supercell_points_cart_labels.append(label)
    supercell_points_cart = np.array(supercell_points_cart, dtype=np.float64)
    supercell_points_cart_labels = np.array(supercell_points_cart_labels)

    # Loop through each point in the filtered list
    for i, point_1 in enumerate(filtered_unitcell_points_cart):
        dist = np.linalg.norm(supercell_points_cart - np.array(point_1[:3]), axis=1)
        dist = np.round(dist, 3)
        selected_indices = np.where(np.logical_and(dist < cutoff_radius, dist > 0.1))[0]
        point_2_info = [
            (
                str(supercell_points_cart_labels[index]),
                float(dist[index]),
                [
                    float(np.round(point_1[0], 3)),
                    float(np.round(point_1[1], 3)),
                    float(np.round(point_1[2], 3)),
                ],
                [
                    float(np.round(supercell_points_cart[index][0], 3)),
                    float(np.round(supercell_points_cart[index][1], 3)),
                    float(np.round(supercell_points_cart[index][2], 3)),
                ],
            )
            for index in selected_indices
        ]
        dist_set.update(dist[selected_indices].tolist())
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
