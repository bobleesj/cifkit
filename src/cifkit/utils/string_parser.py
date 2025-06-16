import re

from cifkit.utils import formula
from cifkit.utils.error_messages import GeneralError


def get_atom_type_from_label(site_label: str) -> str:
    """Return the element from the given label."""
    validated_label = formula.get_validated_formula_label(site_label)
    if not isinstance(validated_label, str):
        raise TypeError(GeneralError.INVALID_TYPE.value)
    if not validated_label:
        raise ValueError(GeneralError.EMPTY_STRING_INPUT.value)
    if not validated_label[0].isalpha():
        raise ValueError(GeneralError.NON_ALPHABETIC_START.value)

    parts = re.split(r"[()]", validated_label)
    for part in parts:
        # Attempt to extract the atom type
        match = re.search(r"([A-Z][a-z]*)", part)
        if match:
            return match.group(1)
    return ""


def get_string_to_formatted_float(str_value: str) -> float:
    """Remove parentheses from a value string and convert to float."""
    str_value = str_value.strip()

    return float(str_value.split("(")[0]) if "(" in str_value else float(str_value)


def trim_string(formula: str) -> str:
    """Remove "~", " ", and "'" characters from the parsed formula."""
    return formula.replace("~", "").replace(" ", "").replace("'", "")


def clean_parsed_structure(structure_type: str) -> str:
    """Split the parsed structure text and remove "~"."""
    return structure_type.split(",")[0].replace("~", "")


def strip_numbers_and_symbols(value: str) -> str:
    """Removes all digits and '+' and '-' characters from the input
    string.

    Some ICSD, COD have charges in atomic site element e.g. "Fe0+".
    """
    return re.sub(r"[\d\+\-]", "", value)
