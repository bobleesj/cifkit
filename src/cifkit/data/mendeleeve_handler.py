from bobleesj.utils.sources import mendeleev

from cifkit.utils import string_parser


def get_mendeleev_nums_from_pair_tuple(
    label_pair_tuple: tuple[str, str],
) -> tuple[int, int]:
    """Parse Mendeleev number for each label in the tuple.

    If no number is found, default to 0 for that element.
    """
    # Parse the first and second elements
    first_element = string_parser.get_atom_type_from_label(label_pair_tuple[0])
    second_element = string_parser.get_atom_type_from_label(label_pair_tuple[1])
    mendeleev_numbers = mendeleev.numbers
    # Get Mendeleev number for the first element, default to 0 if not found
    first_mendeleev_num = mendeleev_numbers.get(first_element, 0)
    # Get Mendeleev number for the second element, default to 0 if not found
    second_mendeleev_num = mendeleev_numbers.get(second_element, 0)
    return first_mendeleev_num, second_mendeleev_num
