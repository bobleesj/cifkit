import pytest

from cifkit.sources.radius import (
    are_available,
    data,
    is_available,
    supported_elements,
    value,
)


def test_get_radius_data():
    """Test the get_radius_data function."""
    radius_data = data()

    # Check if the data is a dictionary
    assert isinstance(radius_data, dict)

    # Check if it contains expected elements
    expected_elements = ["Li", "Fe", "O", "N"]
    for element in expected_elements:
        assert element in radius_data

    # Check if each element has the correct structure
    for element in expected_elements:
        assert isinstance(radius_data[element], dict)
        assert "CIF" in radius_data[element]
        assert "Pauling_CN12" in radius_data[element]


def test_is_available():
    """Test the is_available function."""
    assert is_available("Fe") is True
    assert is_available("UnknownElement") is False


def test_are_available():
    """Test the are_available function."""
    assert are_available(["Fe", "O", "N"]) is True
    assert are_available(["Fe", "UnknownElement"]) is False


def test_get_radius():
    """Test the get_radius function."""
    assert value("Fe") == {
        "CIF": 1.242,
        "Pauling_CN12": 1.26,
    }
    # Test for an unknown element
    with pytest.raises(
        KeyError, match="Element 'UnknownElement' not found in radius data."
    ):
        value("UnknownElement")


def test_get_supported_elements():
    """Test the get_supported_elements function."""
    actual_elements = supported_elements()

    # Check if the result is a list
    assert isinstance(actual_elements, list)

    # Check if it contains expected elements
    expected_elements = ["Li", "Fe", "O", "N"]
    for element in expected_elements:
        assert element in actual_elements
    assert len(actual_elements) == 79


def test_is_supported():
    """Test the is_supported function."""
    assert is_available("Fe") is True
    assert is_available("UnknownElement") is False
