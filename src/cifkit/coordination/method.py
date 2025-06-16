from cifkit.utils.string_parser import get_atom_type_from_label


def compute_CN_max_gap_per_site(
    radius_sum_data,
    all_labels_connections,
    is_radius_data_available: bool,
    site_mixing_type: str,
) -> dict[str : dict[str : dict[str:float]]]:
    use_all_methods = False

    if is_radius_data_available and site_mixing_type == "full_occupancy":
        use_all_methods = True

    if use_all_methods:
        methods: dict[str, list[float]] = {
            "dist_by_shortest_dist": [],
            "dist_by_CIF_radius_sum": [],
            "dist_by_CIF_radius_refined_sum": [],
            "dist_by_Pauling_radius_sum": [],
        }
    else:
        methods = {
            "dist_by_shortest_dist": [],
        }

    norm_dists_per_label: dict = {}
    max_gaps_per_label: dict = {}

    for ref_label, connection_data in all_labels_connections.items():
        # Initialize each label
        norm_dists_per_label[ref_label] = {key: [] for key in methods}
        max_gaps_per_label[ref_label] = {
            method: {"max_gap": 0, "CN": -1} for method in methods
        }
        # Limit to 20 connection data points
        connection_data = connection_data[:20]
        shortest_dist = connection_data[0][1]
        previous_values: dict[str, float] = {method: 0.0 for method in methods}

        for i, connection in enumerate(connection_data):
            pair_dist = connection[1]
            connected_label = connection[0]
            # Get new rad sum for each ref label
            if use_all_methods:
                CIF_radius_sum_norm_value = get_rad_sum_value(
                    radius_sum_data,
                    "CIF_radius_sum",
                    ref_label,
                    connected_label,
                )
                CIF_radius_sum_refined_norm_value = get_rad_sum_value(
                    radius_sum_data,
                    "CIF_radius_refined_sum",
                    ref_label,
                    connected_label,
                )
                Pauling_rad_sum_norm_value = get_rad_sum_value(
                    radius_sum_data,
                    "Pauling_radius_sum",
                    ref_label,
                    connected_label,
                )
                norm_dist_by_CIF_radius_sum = compute_normalized_value(
                    pair_dist, CIF_radius_sum_norm_value
                )
                norm_dist_by_CIF_rad_ref_sum = compute_normalized_value(
                    pair_dist, CIF_radius_sum_refined_norm_value
                )
                norm_dist_by_Pauling_radius_sum = compute_normalized_value(
                    pair_dist, Pauling_rad_sum_norm_value
                )

            # Compute normalized distances
            norm_dist_by_min_dist = compute_normalized_value(pair_dist, shortest_dist)
            # Store distances
            if use_all_methods:
                distances = {
                    "dist_by_shortest_dist": norm_dist_by_min_dist,
                    "dist_by_CIF_radius_sum": norm_dist_by_CIF_radius_sum,
                    "dist_by_CIF_radius_refined_sum": norm_dist_by_CIF_rad_ref_sum,
                    "dist_by_Pauling_radius_sum": norm_dist_by_Pauling_radius_sum,
                }
            else:
                distances = {
                    "dist_by_shortest_dist": norm_dist_by_min_dist,
                }

            for method, norm_distance in distances.items():
                norm_dists_per_label[ref_label][method].append(norm_distance)

                # Calculate and update max gaps
                if previous_values[method]:
                    current_gap = round(
                        abs(norm_distance - previous_values[method]),
                        3,
                    )
                    if current_gap > max_gaps_per_label[ref_label][method]["max_gap"]:
                        max_gaps_per_label[ref_label][method]["max_gap"] = current_gap
                        max_gaps_per_label[ref_label][method]["CN"] = i

                previous_values[method] = norm_distance

    return max_gaps_per_label


def compute_normalized_value(number: float, ref_number: float) -> float:
    return round((number / ref_number), 5)


def get_rad_sum_value(
    rad_sum_data, method_name: str, ref_label: str, other_label: str
) -> float:
    """Return the sum of radii value for a given pair of elements,
    ensuring the pair is alphabetically sorted."""

    # Extract the element types from the labels
    ref_element = get_atom_type_from_label(ref_label)
    other_element = get_atom_type_from_label(other_label)

    # Sort the elements alphabetically to form a consistent key
    sorted_elements = sorted([ref_element, other_element])
    key = f"{sorted_elements[0]}-{sorted_elements[1]}"

    # Ensure that method_name is valid and key exists in the dictionary
    if method_name not in rad_sum_data:
        raise KeyError(f"Method {method_name} not found in rad_sum")
    if key not in rad_sum_data[method_name]:
        raise KeyError(f"Key {key} not found in method {method_name} of rad_sum")

    return rad_sum_data[method_name][key]
