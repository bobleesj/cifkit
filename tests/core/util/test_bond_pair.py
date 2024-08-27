import pytest

from cifkit.utils.bond_pair import (
    get_bond_pairs,
    get_pairs_sorted_by_mendeleev,
    order_tuple_pair_by_mendeleev,
)


@pytest.mark.fast
def test_get_unique_sorted_pairs():
    labels = {"Er1", "Co2", "In3"}
    assert get_bond_pairs(labels) == {
        ("Co2", "Er1"),
        ("Er1", "Er1"),
        ("In3", "In3"),
        ("Co2", "In3"),
        ("Er1", "In3"),
        ("Co2", "Co2"),
    }

    labels = {"Co1", "In"}
    assert get_bond_pairs(labels) == {
        ("Co1", "In"),
        ("In", "In"),
        ("Co1", "Co1"),
    }


@pytest.mark.fast
def test_get_unique_sorted_pairs_by_mendeleev():
    labels = {"Er1", "Co2", "In3"}
    result = get_pairs_sorted_by_mendeleev(labels)
    assert result == {
        ("Co2", "Co2"),
        ("Co2", "In3"),
        ("Er1", "Co2"),
        ("Er1", "Er1"),
        ("Er1", "In3"),
        ("In3", "In3"),
    }


@pytest.mark.parametrize(
    "input_pair,expected",
    [
        (("In", "U"), ("U", "In")),
        (("U", "In"), ("U", "In")),
        (("Rh", "U"), ("U", "Rh")),
        (("In", "Rh"), ("Rh", "In")),
        (("Rh4", "Rh2"), ("Rh2", "Rh4")),
        (("Co2B", "Co2A"), ("Co2A", "Co2B")),
        (("Co2A", "Co2B"), ("Co2A", "Co2B")),
    ],
)
def test_order_tuple_pair_by_mendeleev(input_pair, expected):
    # U = 20 Rh = 59 In = 75
    result = order_tuple_pair_by_mendeleev(input_pair)
    assert result == expected
