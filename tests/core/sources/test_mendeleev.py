from cifkit.sources import mendeleev


def test_mendeleev():
    assert len(mendeleev.numbers) == 85
    # Check that all elements have unique atomic numbers
    assert len(set(mendeleev.numbers.keys())) == 85
    # Check that all values are integers
    assert all(isinstance(num, int) for num in mendeleev.numbers.values())
    # Check the value ca be retrieved for a known element
    assert mendeleev.numbers["H"] == 92
