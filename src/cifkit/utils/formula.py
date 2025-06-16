"""Parses a formula."""

import re

from cifkit.utils.error_messages import GeneralError


def get_validated_formula_label(formula: str) -> str:
    if not isinstance(formula, str):
        raise TypeError(GeneralError.INVALID_TYPE.value)
    if not formula:
        raise ValueError(GeneralError.EMPTY_STRING_INPUT.value)
    trimmed_formula = formula.strip()
    if not trimmed_formula or not trimmed_formula[0].isalpha():
        raise ValueError(GeneralError.NON_ALPHABETIC_START.value)
    return trimmed_formula


def get_parsed_formula(formula: str) -> list[tuple[str, str]]:
    """Return a list of tuples, each tuple containing an element and its
    index."""
    trimmed_formula = get_validated_formula_label(formula)
    pattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
    elements = re.findall(pattern, trimmed_formula)
    return elements


def get_normalized_formula(formula: str, demical_places=3) -> str:
    """Return a formula with the stoichiometry coefficient sum of 1."""
    index_sum = 0.0
    normalized_formula_parts = []
    parsed_formula_set = get_parsed_formula(formula)

    # Calculate the sum of all indices
    for element, element_index in parsed_formula_set:
        if element_index == "":
            index_sum += 1.0
        else:
            index_sum += float(element_index)

    for element, element_index in parsed_formula_set:
        if element_index == "":
            normalized_index = 1 / index_sum
        else:
            normalized_index = float(element_index) / index_sum

        normalized_formula_parts.append(f"{element}{normalized_index:.{demical_places}f}")

    # Join all parts into one string for the normalized formula
    normalized_formula = "".join(normalized_formula_parts)
    return normalized_formula


def get_parsed_norm_formula(formula: str) -> list[tuple[str, str]]:
    """Return a list of tuples, each tuple containing element and
    normalized index."""
    normalized_formula = get_normalized_formula(formula)
    parsed_normalized_formula = get_parsed_formula(normalized_formula)
    return parsed_normalized_formula


def get_unique_elements(formula: str) -> list[str]:
    "Return a set of elements parsed from a formula."
    elements = get_parsed_formula(formula)
    unique_elements = [element for element, _ in elements]
    return unique_elements


def get_unique_element_count(formula: str) -> int:
    """Return the number of unique elements in the chemical formula."""
    return len(get_unique_elements(formula))


def get_unique_elements_from_formulas(formulas: list) -> set[str]:
    """Return unique elements from a list of formulas."""
    unique_elements = set()  # Create a set to store unique elements

    for formula in formulas:
        parsed_formula = get_parsed_formula(
            formula
        )  # Assume this function returns a list of tuples
        for element, _ in parsed_formula:
            if element:  # Ensure that element is not empty
                unique_elements.add(element)  # Add the element to the set

    return unique_elements


def get_subscripted_formula(formula: str) -> str:
    """Return a subscripted formula used for plotting."""
    validated_formula = get_validated_formula_label(formula)
    # Use regular expression to find elements and numbers
    subscripted_formula = re.sub(
        r"([A-Z][a-z]*)(\d*\.?\d*)", r"\1$_{\2}$", validated_formula
    )
    return subscripted_formula
