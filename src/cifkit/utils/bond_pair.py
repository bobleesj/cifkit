from itertools import product

from cifkit.data.mendeleeve_handler import get_mendeleev_nums_from_pair_tuple


def get_bond_pairs(labels: list[str]) -> set[tuple[str, str]]:
    """Generate all possible unique pairs, each tuple sorted
    alphabetically, including pairs with identical elements."""
    # Generate all combinations of two labels (this time including identical pairs)
    possible_pairs = product(labels, repeat=2)
    sorted_pairs = [tuple(sorted((a, b))) for a, b in possible_pairs]
    return set(sorted_pairs)


def get_pairs_sorted_by_mendeleev(
    labels: list[str],
) -> set[tuple[str, str]]:
    """Generate all unique pairs, each tuple sorted by the Mendeleeve
    number."""
    pairs = get_bond_pairs(labels)
    sorted_pairs = {order_tuple_pair_by_mendeleev(pair) for pair in pairs}
    return sorted_pairs


def order_tuple_pair_by_mendeleev(label_pair_tuple):
    """Order a pair of elements based on Mendeleev numbers."""
    first_label = label_pair_tuple[0]
    second_label = label_pair_tuple[1]
    (
        first_mend_num,
        second_mend_num,
    ) = get_mendeleev_nums_from_pair_tuple(label_pair_tuple)

    # If first element num is smaller
    if first_mend_num > second_mend_num:
        return (second_label, first_label)
    # If first and second, same number, sort alphabetically
    elif first_mend_num == second_mend_num:
        return tuple(sorted(label_pair_tuple))
    # If it in correct order, return as it is
    else:
        return label_pair_tuple
