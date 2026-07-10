import pytest

from cifkit.parsers.formula import Formula
from cifkit.sources.oliynyk import Property as P

"""
__init__
"""

# def test_valid_formula():
#     formula = Formula("NdSi2")

# def test_invalid_formula():
#     with pytest.raises(ValueError, match="Invalid formula: 'boblee'"):
#         Formula("boblee")
"""
@staticmethod - order
"""


def test_order_by_alphabetical():
    formulas = ["AB2", "AB", "BC2D2", "BBC2"]
    actual_ordered_formulas = Formula.order_by_alphabetical(formulas)
    expected_ordered_formulas = ["AB", "AB2", "BBC2", "BC2D2"]
    assert actual_ordered_formulas == expected_ordered_formulas


def test_order_by_alphabetical_reverse():
    formulas = ["AB2", "AB", "BC2D2", "BBC2"]
    actual_ordered_formulas = Formula.order_by_alphabetical(formulas, reverse=True)
    expected_ordered_formulas = ["BC2D2", "BBC2", "AB2", "AB"]
    assert actual_ordered_formulas == expected_ordered_formulas


"""
@staticmethod - count
"""


def test_count_formulas():
    formulas = ["NdSi2", "NdSi2", "NdSi2Th2", "NdSi2Th2", "ThOs"]
    actual_count = Formula.count(formulas)
    expected_count = 5
    assert actual_count == expected_count


def test_count_unique_formulas():
    formulas = ["NdSi2", "NdSi2", "NdSi2Th2", "NdSi2Th2", "ThOs"]
    actual_count_unique_formulas = Formula.count_unique(formulas)
    expected_count_unique_formulas = 3
    assert actual_count_unique_formulas == expected_count_unique_formulas


def test_count_individual():
    formulas = ["NdSi2", "NdSi2", "NdSi2Th2", "NdSi2Th2", "ThOs"]
    actual_count_all = Formula.count_individual(formulas)
    expected_count_all = {"NdSi2": 2, "NdSi2Th2": 2, "ThOs": 1}
    assert actual_count_all == expected_count_all


def test_count_duplicates():
    formulas = ["NdSi2", "NdSi2", "NdSi2Th2", "NdSi2Th2", "ThOs"]
    actual_duplicates = Formula.count_duplicates(formulas)
    expected_duplicates = {"NdSi2": 2, "NdSi2Th2": 2}
    assert actual_duplicates == expected_duplicates


def test_count_by_formula():
    formulas = ["NdSi2", "NdSi2", "NdSi2Th2", "NdSi2Th2", "ThOs"]
    actual_count_by_formula = Formula.count_by_formula(formulas, "NdSi2")
    expected_count_by_formula = 2
    assert actual_count_by_formula == expected_count_by_formula


def test_count_by_composition():
    formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
    actual_count_dict = Formula.count_by_composition(formulas)
    expected_count_dict = {2: 2, 3: 1, 4: 1}
    assert actual_count_dict == expected_count_dict


def test_get_element_count():
    formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
    actual_element_count = Formula.get_element_count(formulas)
    expected_element_count = {
        "Nd": 3,
        "Si": 3,
        "Th": 3,
        "Os": 1,
        "Y": 1,
    }
    assert actual_element_count == expected_element_count


def test_get_unique_formulas():
    formulas = ["NdSi2", "ThOs", "ThOs"]
    actual_unique_formulas = Formula.get_unique_formulas(formulas)
    expected_unique_formulas = {"NdSi2", "ThOs"}
    assert actual_unique_formulas == expected_unique_formulas


def test_get_unique_elements():
    formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
    actual_unique_elements = Formula.get_unique_elements(formulas)
    expected_unique_elements = {"Nd", "Si", "Th", "Os", "Y"}
    assert actual_unique_elements == expected_unique_elements


"""
@staticmethod - filter
"""


def test_filter_by_composition():
    formulas = ["Cu", "Cu", "NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
    actual_sorted_formula_dict = Formula.filter_by_composition(formulas)
    expected_sorted_formula_dict = {
        1: ["Cu", "Cu"],
        2: ["NdSi2", "ThOs"],
        3: ["NdSi2Th2"],
        4: ["YNdThSi2"],
    }
    assert actual_sorted_formula_dict == expected_sorted_formula_dict


@pytest.mark.parametrize(
    "formulas, n_elements, expected_filtered_formulas",
    [
        # Binary
        (["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"], 2, ["NdSi2", "ThOs"]),
        # Ternary
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2", "FeCuAl"],
            3,
            ["NdSi2Th2", "FeCuAl"],
        ),
        # Quaternary
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2", "FeCuAlZn"],
            4,
            ["YNdThSi2", "FeCuAlZn"],
        ),
    ],
)
def test_filter_by_composition_single(formulas, n_elements, expected_filtered_formulas):
    actual_filtered_formulas = Formula.filter_by_single_composition(formulas, n_elements)
    assert actual_filtered_formulas == expected_filtered_formulas


@pytest.mark.parametrize(
    "formulas, elements, expected_filtered_formulas",
    [
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"],
            ["Nd"],
            ["NdSi2", "NdSi2Th2", "YNdThSi2"],
        ),
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"],
            ["Th"],
            ["ThOs", "NdSi2Th2", "YNdThSi2"],
        ),
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"],
            ["Si", "Th"],
            ["NdSi2Th2", "YNdThSi2"],
        ),
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"],
            ["Y"],
            ["YNdThSi2"],
        ),
    ],
)
def test_filter_by_elements_containing(formulas, elements, expected_filtered_formulas):
    actual_filtered_formulas = Formula.filter_by_elements_containing(formulas, elements)
    assert actual_filtered_formulas == expected_filtered_formulas


@pytest.mark.parametrize(
    "formulas, elements, expected_filtered_formulas",
    [
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"],
            ["Nd", "Si"],
            ["NdSi2"],
        ),
        (
            ["NdSi2", "ThOs", "ThOs2", "NdSi2Th2", "YNdThSi2"],
            ["Th", "Os"],
            ["ThOs", "ThOs2"],
        ),
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"],
            ["Nd", "Si", "Th"],
            ["NdSi2Th2"],
        ),
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"],
            ["Y", "Nd", "Th", "Si"],
            ["YNdThSi2"],
        ),
        (
            ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"],
            ["Nd"],
            [],
        ),
    ],
)
def test_filter_by_elements_matching(formulas, elements, expected_filtered_formulas):
    actual_filtered_formulas = Formula.filter_by_elements_matching(formulas, elements)
    assert actual_filtered_formulas == expected_filtered_formulas


@pytest.mark.parametrize(
    "formula, expected_parsed_formula",
    [
        ("NdSi2", [("Nd", 1), ("Si", 2)]),
        ("Th2Os", [("Th", 2), ("Os", 1)]),
        ("Sm5Co7Sb2", [("Sm", 5), ("Co", 7), ("Sb", 2)]),
        ("SmCoSb", [("Sm", 1), ("Co", 1), ("Sb", 1)]),
        ("ABCD", [("A", 1), ("B", 1), ("C", 1), ("D", 1)]),
        ("A0.1B0.2C0.3D0.4", [("A", 0.1), ("B", 0.2), ("C", 0.3), ("D", 0.4)]),
        ("A1B1C1D1", [("A", 1), ("B", 1), ("C", 1), ("D", 1)]),
    ],
)
def test_parse_formula(formula, expected_parsed_formula):
    actual_parsed_formula = Formula(formula, validate=False).parsed_formula
    assert actual_parsed_formula == expected_parsed_formula


@pytest.mark.parametrize(
    "parsed_formula, expected_string",
    [
        # Floats with 2 elements
        ([("Nd", 0.333), ("Si", 0.667)], "Nd0.333Si0.667"),
        # Floats with 3 elements
        ([("Sm", 0.25), ("Co", 0.5), ("Sb", 0.25)], "Sm0.25Co0.5Sb0.25"),
        ([("Th", 0.5), ("Os", 0.5)], "Th0.5Os0.5"),
        # Two integers with 2 elements
        ([("A", 1.0), ("B", 1.0)], "AB"),
        # One integer that is 1, expect not to display the integer of 1
        ([("A", 1.0), ("B", 0.5)], "AB0.5"),
        # One integer that is not 1, expect to display the integer
        ([("A", 2.0), ("B", 0.5)], "A2B0.5"),
    ],
)
def test_get_formula_string_from_parsed(parsed_formula, expected_string):
    actual_formula = Formula.build_formula_from_parsed(parsed_formula)
    assert actual_formula == expected_string


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("NdSi2", "Nd0.333333Si0.666667"),
        ("Th2Os", "Th0.666667Os0.333333"),
        ("Sn5Co2", "Sn0.714286Co0.285714"),
        ("ABC", "A0.333333B0.333333C0.333333"),
        ("ABC1", "A0.333333B0.333333C0.333333"),
    ],
)
def test_get_normalized_formula(formula, expected):
    actual = Formula(formula, validate=False).get_normalized_formula()
    assert actual == expected


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("NdSi2", "Nd0.333Si0.667"),
        ("Th2Os", "Th0.667Os0.333"),
        ("Sn5Co2", "Sn0.714Co0.286"),
        ("ABC", "A0.333B0.333C0.333"),
        ("ABC1", "A0.333B0.333C0.333"),
    ],
)
def test_get_normalized_formula_3_decial(
    formula,
    expected,
):
    actual = Formula(formula, validate=False).get_normalized_formula(decimals=3)
    assert actual == expected


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("NdSi2", [("Nd", 0.333), ("Si", 0.667)]),
        ("Th2Os", [("Th", 0.667), ("Os", 0.333)]),
    ],
)
def test_normalized_parsed_formula(formula, expected):
    actual = Formula(formula, validate=False).get_normalized_parsed_formula(decimals=3)
    assert actual == expected


"""
@property
"""


@pytest.mark.parametrize(
    "formula, expected_elements",
    [
        ("NdSi2", ["Nd", "Si"]),
        ("Th2Os", ["Th", "Os"]),
        ("Sm5Co7Sb2", ["Sm", "Co", "Sb"]),
        ("SmCoSb", ["Sm", "Co", "Sb"]),
        ("ABCD", ["A", "B", "C", "D"]),
        ("A1B1C1D1", ["A", "B", "C", "D"]),
    ],
)
def test_get_elements_from_formula(formula, expected_elements):
    actual = Formula(formula, validate=False).elements
    assert actual == expected_elements


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("NdSi2", 2),  # Binary
        ("Th2Os", 2),  # Binary
        ("Sm5Co7Sb2", 3),  # Ternary
        ("SmCoSb", 3),  # Tenary without numbers
        ("ABCD", 4),  # Quarternary
        ("A1B1C1D1", 4),  # Quarternary
    ],
)
def test_count_element(formula, expected):
    actual = Formula(formula, validate=False).element_count
    assert actual == expected


@pytest.mark.parametrize(
    "formula, expected_max_min_avg_index",
    [
        ("NdSi2", (2, 1, 1.5)),
        ("Sn5Co2", (5, 2, 3.5)),
        ("NdSi2Th2", (2, 1, 1.667)),
    ],
)
def test_max_min_avg_index(formula, expected_max_min_avg_index):
    actual = Formula(formula, validate=False).max_min_avg_index
    assert actual == pytest.approx(expected_max_min_avg_index, abs=1e-3)


@pytest.mark.parametrize(
    "formula, expected_indices",
    [
        ("NdSi2", [1.0, 2.0]),
        ("Th2Os", [2.0, 1.0]),
        ("Sm5Co7Sb2", [5.0, 7.0, 2.0]),
        ("SmCoSb", [1.0, 1.0, 1.0]),
        ("ABCD", [1.0, 1.0, 1.0, 1.0]),
        ("A1B1C1D1", [1.0, 1.0, 1.0, 1.0]),
    ],
)
def test_indices(formula, expected_indices):
    actual = Formula(formula, validate=False).indices
    assert actual == expected_indices


@pytest.mark.parametrize(
    "formula, expected_norm_indices",
    [
        ("NdSi2", [0.333333, 0.666667]),
        ("Th2Os", [0.666667, 0.333333]),
        ("Sm5Co7Sb2", [0.357143, 0.5, 0.142857]),
        ("SmCoSb", [0.333333, 0.333333, 0.333333]),
        ("ABCD", [0.25, 0.25, 0.25, 0.25]),
        ("A1B1C1D1", [0.25, 0.25, 0.25, 0.25]),
    ],
)
def test_get_normalized_indices_from_formula(formula, expected_norm_indices):
    actual = Formula(formula, validate=False).get_normalized_indices()
    assert actual == expected_norm_indices


"""
Sort - helper
"""


def test_convert_custom_labels_to_order_map(custom_labels_from_excel):
    actual_order_map = Formula._convert_custom_labels_to_order_map(
        custom_labels_from_excel
    )
    expected_order_map = {
        2: {"Fe": 0, "Co": 0, "Ni": 0, "Si": 1, "Ga": 1, "Ge": 1},
        3: {
            "Sc": 0,
            "Y": 0,
            "La": 0,
            "Fe": 1,
            "Co": 1,
            "Ni": 1,
            "Si": 2,
            "Ga": 2,
            "Ge": 2,
        },
        4: {
            "Sc": 0,
            "Y": 0,
            "La": 0,
            "Fe": 1,
            "Co": 1,
            "Ni": 1,
            "Si": 2,
            "Ga": 2,
            "Ge": 2,
            "Gd": 3,
            "Tb": 3,
            "Dy": 3,
        },
    }
    assert actual_order_map == expected_order_map


"""
Sort - custom label
"""


@pytest.mark.parametrize(
    "formula,expected_sorted_formula",
    [
        # Binary
        ("FeSi", "FeSi"),
        ("SiFe", "FeSi"),
        # Ternary
        ("ScFeSi", "ScFeSi"),
        ("FeScSi", "ScFeSi"),
        ("SiFeSc", "ScFeSi"),
        # Quaternary
        ("ScFeSiGd", "ScFeSiGd"),
        ("FeScSiGd", "ScFeSiGd"),
        ("SiFeScGd", "ScFeSiGd"),
        ("GdFeScSi", "ScFeSiGd"),
        ("GdSiFeSc", "ScFeSiGd"),
    ],
)
def test_sort_with_custom_order(
    formula, expected_sorted_formula, custom_labels_from_excel
):
    actual_sorted_formula = Formula(formula, validate=False).sort_by_custom_label(
        custom_labels_from_excel
    )
    assert actual_sorted_formula == expected_sorted_formula


"""
Sort - element property
"""


@pytest.mark.parametrize(
    "formula, ascending, normalize, expected_output",
    [
        # C1. Ascending (Al = 13, Cu = 29) → Al before Cu
        ("AlCu2", True, False, "AlCu2"),
        ("Cu2Al", True, False, "AlCu2"),
        # # C2. Ascending, normalized
        ("AlCu2", True, True, "Al0.333333Cu0.666667"),
        ("Cu2Al", True, True, "Al0.333333Cu0.666667"),
        # C3. Descending
        ("AlCu2", False, False, "Cu2Al"),
        ("Cu2Al1", False, False, "Cu2Al"),
        # C4. Descending, normalized
        ("AlCu2", False, True, "Cu0.666667Al0.333333"),
        ("Cu2Al", False, True, "Cu0.666667Al0.333333"),
    ],
)
def test_sort_by_element_property(formula, ascending, normalize, expected_output):
    property_data = {"Al": 26.981539, "Cu": 63.546, "Test": 100.0}
    result = Formula(formula, validate=False).sort_by_elemental_property(
        property_data, ascending, normalize
    )
    assert result == expected_output


"""
Sort - stoichiometry
"""


@pytest.mark.parametrize(
    # Li Mendeleev number = 1
    # Na Mendeleev number = 11
    # B Mendeleev number = 72
    "formula, expected_output",
    [
        # Test sorting by composiiton, ascending
        # C1. Test binary
        ("LiB", "LiB"),
        ("Li1B1", "LiB"),
        ("LiB1", "LiB"),
        ("BLi", "LiB"),
        ("B1Li1", "LiB"),
        ("BLi1", "LiB"),
        # C2 Test ternary
        # 1. All 3 element same comp, expect LiNaB
        ("LiNaB", "LiNaB"),
        ("Li1Na1B1", "LiNaB"),
        ("LiNaB1", "LiNaB"),
        ("BLiNa", "LiNaB"),
        ("BLi1Na1", "LiNaB"),
        ("BLiNa1", "LiNaB"),
        # 2. Two elements same comp, expect one element last
        ("LiNa2B", "LiBNa2"),  # Na2 should be last
        ("LiNaB2", "LiNaB2"),  # B2 should be last
        ("Li2NaB", "NaBLi2"),  # Li2 should be last
    ],
)
def test_sort_by_stoichiometry_default_with_Mendeleeve(formula, expected_output, oliynyk):
    result = Formula(formula, validate=False).sort_by_stoichiometry(
        oliynyk.get_property_data_for_formula(formula, P.MEND_NUM)
    )
    assert result == expected_output


@pytest.mark.parametrize(
    "formula, expected_output",
    [
        # Test sorting by composition, descending
        # C1. Test binary
        ("LiB", "LiB"),
        ("Li1B1", "LiB"),
        ("LiB1", "LiB"),
        ("BLi", "LiB"),
        ("B1Li1", "LiB"),
        ("BLi1", "LiB"),
        # C2 Test ternary
        # 1. Two elements same comp, expect one element last
        ("LiNa2B", "Na2LiB"),  # Li should be last
        ("LiNaB2", "B2LiNa"),  # Na should be last
        ("Li2NaB", "Li2NaB"),  # Na should be last
    ],
)
def test_sort_by_stoichiometry_descend_with_Mendeleeve(formula, expected_output, oliynyk):
    result = Formula(formula, validate=False).sort_by_stoichiometry(
        oliynyk.get_property_data_for_formula(formula, P.MEND_NUM),
        ascending=False,
    )
    assert result == expected_output
