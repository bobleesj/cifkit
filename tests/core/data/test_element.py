import pytest

from cifkit.data.element import Element


@pytest.mark.parametrize(
    "element, expected_name, expected_value",
    [
        (Element.H, "H", "Hydrogen"),
        (Element.He, "He", "Helium"),
        (Element.Li, "Li", "Lithium"),
    ],
)
def test_element_enum_names_and_values(element, expected_name, expected_value):
    assert element.symbol == expected_name
    assert element.full_name == expected_value


def test_element_enum_length():
    # Test that there are exactly 118 elements
    assert len(Element) == 118


def test_element_enum_values_unique():
    # Test that all enum values are unique
    values = [e.value for e in Element]
    assert len(values) == len(set(values))


def test_element_supported():
    all_symbols = Element.all_symbols()
    assert len(all_symbols) == 118
    assert "H" in all_symbols
    assert "He" in all_symbols
