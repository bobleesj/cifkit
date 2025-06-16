import pytest

from cifkit.utils.error_messages import GeneralError
from cifkit.utils.formula import (
    get_normalized_formula,
    get_parsed_formula,
    get_parsed_norm_formula,
    get_subscripted_formula,
    get_unique_element_count,
    get_unique_elements,
    get_unique_elements_from_formulas,
    get_validated_formula_label,
)


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("H2O", "H2O"),
        (" H2O", "H2O"),
        ("H2O ", "H2O"),
        ("  H2O  ", "H2O"),
        ("C6H12O6", "C6H12O6"),
        ("NaCl", "NaCl"),
        ("Na0.5Cl0.5", "Na0.5Cl0.5"),
    ],
)
def test_get_validated_formula_valid_input(formula, expected):
    assert get_validated_formula_label(formula) == expected


def test_get_validated_formula_error():
    with pytest.raises(TypeError) as e:
        get_validated_formula_label(123)
    assert str(e.value) == GeneralError.INVALID_TYPE.value

    with pytest.raises(ValueError) as e:
        get_validated_formula_label("2Fe")
    assert str(e.value) == GeneralError.NON_ALPHABETIC_START.value


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("H2O", [("H", "2"), ("O", "")]),
        ("C6H12O6", [("C", "6"), ("H", "12"), ("O", "6")]),
        ("NaCl", [("Na", ""), ("Cl", "")]),
        ("Na0.5Cl0.5", [("Na", "0.5"), ("Cl", "0.5")]),
        (" H2O", [("H", "2"), ("O", "")]),
        ("H2O  ", [("H", "2"), ("O", "")]),
        ("  C6H12O6  ", [("C", "6"), ("H", "12"), ("O", "6")]),
    ],
)
def test_get_parsed_formula_valid_input(formula, expected):
    assert get_parsed_formula(formula) == expected


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("H2", ["H"]),
        ("C6H12O6", ["C", "H", "O"]),
        ("Na0.5Cl0.5", ["Na", "Cl"]),
    ],
)
def test_get_unique_element(formula, expected):
    assert get_unique_elements(formula) == expected


@pytest.mark.parametrize(
    "formula, expected",
    [("H2", 1), ("C6H12O6", 3), ("NaCl", 2), ("Na0.5Cl0.5", 2)],
)
def test_get_unique_element_count(formula, expected):
    assert get_unique_element_count(formula) == expected


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("H2O", "H$_{2}$O$_{}$"),
        ("C6H12O6", "C$_{6}$H$_{12}$O$_{6}$"),
        ("NaCl", "Na$_{}$Cl$_{}$"),
        ("Fe2.5O4.1", "Fe$_{2.5}$O$_{4.1}$"),
    ],
)
def test_get_subscripted_formula_parametrized(formula, expected):
    assert get_subscripted_formula(formula) == expected


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("H2O", "H0.667O0.333"),
        ("C6H12O6", "C0.250H0.500O0.250"),
        ("NaCl", "Na0.500Cl0.500"),
        ("Fe2", "Fe1.000"),
        ("K", "K1.000"),
        (" K ", "K1.000"),
        ("Na0.5Cl0.5", "Na0.500Cl0.500"),
    ],
)
def test_get_normalized_formula(formula, expected):
    result = get_normalized_formula(formula)
    assert (
        result == expected
    ), f"Failed on formula {formula}: expected {expected}, got {result}"


def test_get_get_unique_elements_from_formulas():
    formulas = ["NaCl", "H2O", "Fe2"]
    result = get_unique_elements_from_formulas(formulas)
    assert result == {"H", "Cl", "Na", "O", "Fe"}


@pytest.mark.parametrize(
    "formula, expected",
    [
        # Basic formulas
        (
            "H2O",
            [("H", "0.667"), ("O", "0.333")],
        ),
        (
            "NaCl",
            [("Na", "0.500"), ("Cl", "0.500")],
        ),
        (
            "Na0.5Cl0.5",
            [("Na", "0.500"), ("Cl", "0.500")],
        ),
        (
            " MgCl2 ",
            [("Mg", "0.333"), ("Cl", "0.667")],
        ),
    ],
)
def test_get_parsed_norm_formula_valid(formula, expected):
    assert get_parsed_norm_formula(formula) == expected
