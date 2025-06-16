from cifkit.utils.sort import sort_element_pair_tuples


def test_sort_element_pair_tuples():
    input_tuples = [
        (("B", "A"), 2.0),
        (("A", "C"), 3.0),
        (("A", "B"), 1.5),
        (("A", "B"), 1.0),
    ]
    expected_output = [
        (("A", "B"), 1.0),
        (("A", "B"), 1.5),
        (("A", "B"), 2.0),
        (("A", "C"), 3.0),
    ]
    assert sort_element_pair_tuples(input_tuples) == expected_output
