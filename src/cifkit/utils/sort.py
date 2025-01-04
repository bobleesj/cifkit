def sort_element_pair_tuples(
    element_pair_tuples: list[tuple[tuple[str, str], float]],
) -> list[tuple[tuple[str, str], float]]:
    """Alphabetically sort the pair tuple of elements."""
    # First, sort the elements within each tuple
    alp_sorted_tuples = [
        ((min(a, b), max(a, b)), distance) for (a, b), distance in element_pair_tuples
    ]

    # Priotize alphabetic sort, and sort by distance
    sorted_tuples = sorted(alp_sorted_tuples, key=lambda x: (x[0], x[1]))

    return sorted_tuples
