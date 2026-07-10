import pytest

"""
Test init with custom labels from a dictionary
"""


def test_get_custom_labels_from_dict(element_sorter_from_dict):
    assert element_sorter_from_dict.label_mapping == {
        2: {"A": ["Fe", "Co", "Ni"], "B": ["Si", "Ga", "Ge"]},
        3: {
            "R": ["Sc", "Y", "La"],
            "M": ["Fe", "Co", "Ni"],
            "X": ["Si", "Ga", "Ge"],
        },
        4: {
            "A": ["Sc", "Y", "La"],
            "B": ["Fe", "Co", "Ni"],
            "C": ["Si", "Ga", "Ge"],
            "D": ["Gd", "Tb", "Dy"],
        },
    }


def test_get_custom_labels_from_excel(element_sorter_from_excel):
    assert element_sorter_from_excel.label_mapping == {
        2: {"A": ["Fe", "Co", "Ni"], "B": ["Si", "Ga", "Ge"]},
        3: {
            "R": ["Sc", "Y", "La"],
            "M": ["Fe", "Co", "Ni"],
            "X": ["Si", "Ga", "Ge"],
        },
        4: {
            "A": ["Sc", "Y", "La"],
            "B": ["Fe", "Co", "Ni"],
            "C": ["Si", "Ga", "Ge"],
            "D": ["Gd", "Tb", "Dy"],
        },
    }


"""
Sort by custom labels defined
"""


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["Fe", "Si"], ("Fe", "Si")),
        (["Si", "Fe"], ("Fe", "Si")),
        (["Ge", "Ni"], ("Ni", "Ge")),
        (["Ga", "Co"], ("Co", "Ga")),
    ],
)
def test_custom_sort_binary(elements, expected, element_sorter_from_dict):
    result = element_sorter_from_dict.sort(elements, method="custom")
    assert result == expected


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["Sc", "Fe", "Si"], ("Sc", "Fe", "Si")),
        (["Si", "Fe", "Sc"], ("Sc", "Fe", "Si")),
        (["Fe", "Si", "Sc"], ("Sc", "Fe", "Si")),
    ],
)
def test_custom_sort_ternary(elements, expected, element_sorter_from_dict):
    result = element_sorter_from_dict.sort(elements, method="custom")
    assert result == expected


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["Gd", "Sc", "Fe", "Si"], ("Sc", "Fe", "Si", "Gd")),
        (["Gd", "Si", "Fe", "Sc"], ("Sc", "Fe", "Si", "Gd")),
        (["Y", "Co", "Ga", "Dy"], ("Y", "Co", "Ga", "Dy")),
    ],
)
def test_custom_sort_quaternary(elements, expected, element_sorter_from_dict):
    result = element_sorter_from_dict.sort(elements, method="custom")
    assert result == expected


"""
Sort by Mendeleev number order.
"""


@pytest.mark.parametrize(
    "elements,expected",
    [
        (
            ["Fe", "Si"],
            ("Si", "Fe"),
        ),  # Fe=55, Si=78 → Si before Fe in descending order
        (["Si", "Fe"], ("Si", "Fe")),
        (["Ga", "Co"], ("Ga", "Co")),  # Ga=74, Co=58 → Ga before Co
    ],
)
def test_mendeleev_sort_descend(elements, expected, element_sorter_from_dict):
    result = element_sorter_from_dict.sort(elements, method="mendeleev")
    assert result == expected


@pytest.mark.parametrize(
    "elements,expected",
    [
        (
            ["Fe", "Si"],
            ("Fe", "Si"),
        ),  # Fe=55, Si=78 → Fe before Si in ascending order
        (["Si", "Fe"], ("Fe", "Si")),
        (["Co", "Ga"], ("Co", "Ga")),  # Co=58, Ga=74
    ],
)
def test_mendeleev_sort_ascend(elements, expected, element_sorter_from_dict):
    result = element_sorter_from_dict.sort(elements, method="mendeleev", descending=False)
    assert result == expected


"""
Sort by alphabetical order.
"""


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["Fe", "Si"], ("Si", "Fe")),
        (["Si", "Fe"], ("Si", "Fe")),
        (["C", "B", "A"], ("C", "B", "A")),
    ],
)
def test_alphabetical_sort_descend(elements, expected, element_sorter_from_dict):
    result = element_sorter_from_dict.sort(elements, descending=True)
    assert result == expected


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["Fe", "Si"], ("Fe", "Si")),
        (["Si", "Fe"], ("Fe", "Si")),
        (["C", "B", "A"], ("A", "B", "C")),
    ],
)
def test_alphabetical_sort_ascend(elements, expected, element_sorter_from_dict):
    result = element_sorter_from_dict.sort(elements, descending=False)
    assert result == expected
