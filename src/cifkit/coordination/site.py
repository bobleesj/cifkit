from cifkit.utils import sort, string_parser


def get_min_distance_pair(
    connections: dict,
) -> tuple[tuple[str, str], float]:
    """Return an alphabetically sorted element pair with the global
    minimum distance in the entire supercell."""
    sorted_tuples = get_min_distance_pair_per_site_label(connections)
    min_dist_tuple = sorted_tuples[0]
    return min_dist_tuple


def get_min_distance_pair_per_site_label(
    connections: dict,
) -> list[tuple[tuple[str, str], float]]:
    """Return a list of tuples containing element pairs and the minimum
    distance from each site label in the loop."""
    element_pairs = []
    # Iterate over each pair and their list of distances
    for ref_label, pair_data in connections.items():
        min_dist_pair_data = pair_data[0]
        other_label = min_dist_pair_data[0]
        distance = min_dist_pair_data[1]

        ref_element = string_parser.get_atom_type_from_label(ref_label)
        other_element = string_parser.get_atom_type_from_label(other_label)

        element_pairs.append(((ref_element, other_element), distance))
    sorted_tuples = sort.sort_element_pair_tuples(element_pairs)
    return sorted_tuples
