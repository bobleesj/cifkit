def data() -> dict:
    """Return a dictionary of element radius data."""
    rad_data = {
        "Si": [1.176, 1.316],
        "Sc": [1.641, 1.620],
        "Fe": [1.242, 1.260],
        "Co": [1.250, 1.252],
        "Ni": [1.246, 1.244],
        "Ga": [1.243, 1.408],
        "Ge": [1.225, 1.366],
        "Y": [1.783, 1.797],
        "Ru": [1.324, 1.336],
        "Rh": [1.345, 1.342],
        "Pd": [1.376, 1.373],
        "In": [1.624, 1.660],
        "Sn": [1.511, 1.620],
        "Sb": [1.434, 1.590],
        "La": [1.871, 1.871],
        "Ce": [1.819, 1.818],
        "Pr": [1.820, 1.824],
        "Nd": [1.813, 1.818],
        "Sm": [1.793, 1.850],
        "Eu": [1.987, 2.084],
        "Gd": [1.787, 1.795],
        "Tb": [1.764, 1.773],
        "Dy": [1.752, 1.770],
        "Ho": [1.745, 1.761],
        "Er": [1.734, 1.748],
        "Tm": [1.726, 1.743],
        "Yb": [1.939, 1.933],
        "Lu": [1.718, 1.738],
        "Os": [1.337, 1.350],
        "Ir": [1.356, 1.355],
        "Pt": [1.387, 1.385],
        "Th": [1.798, 1.795],
        "U": [1.377, 1.516],
        "Al": [1.310, 1.310],
        "Mo": [1.362, 1.386],
        "Hf": [1.5635, 1.585],
        "Ta": [1.430, 1.457],
        "Ag": [1.443, 1.442],
        "As": [1.247, 1.39],
        "Au": [1.435, 1.439],
        "B": [0.807, 0.98],
        "Ba": [1.994, 2.215],
        "Be": [1.072, 1.123],
        "Bi": [1.53, 1.7],
        "C": [0.76, 0.914],
        "Ca": [1.716, 1.97],
        "Cd": [1.49, 1.543],
        "Cr": [1.204, 1.357],
        "Cs": [1.894, 2.67],
        "Cu": [1.275, 1.276],
        "Hg": [1.45, 1.57],
        "K": [1.823, 2.349],
        "Li": [1.488, 1.549],
        "Mg": [1.587, 1.598],
        "Mn": [1.164, 1.306],
        "Na": [1.662, 1.896],
        "Nb": [1.426, 1.456],
        "P": [1.123, 1.28],
        "Pb": [1.725, 1.746],
        "Rb": [1.781, 2.48],
        "Re": [1.345, 1.373],
        "S": [1.074, 1.27],
        "Se": [1.237, 1.4],
        "Sr": [1.977, 2.148],
        "Te": [1.417, 1.6],
        "Ti": [1.406, 1.467],
        "Tl": [1.663, 1.712],
        "V": [1.307, 1.338],
        "W": [1.364, 1.394],
        "Zn": [1.333, 1.379],
        "Zr": [1.553, 1.597],
        # Below values were interpolated using GPR
        # https://github.com/bobleesj/structure-analyzer-featurizer/pull/9
        "N": [0.536, 0.880],
        "O": [0.611, 1.115],
        "F": [0.709, 1.600],
        "Cl": [0.968, 1.448],
        "Br": [1.141, 1.659],
        "I": [1.359, 1.338],
        "Tc": [1.355, 1.803],
        "Pm": [1.797, 1.635],
    }
    data: dict = {k: {"CIF": v[0], "Pauling_CN12": v[1]} for k, v in rad_data.items()}

    return data


def value(element: str) -> dict[str, float]:
    """Get the radius data for a given element.

    Parameters
    ----------
    element : str
        The chemical symbol of the element.

    Returns
    -------
    dict[str, float]
        A dictionary containing the CIF radius and Pauling radius.

    Raises
    ------
    KeyError
        If the element is not found in the radius data.
    Examples
    --------
    >>> get_radius("Fe")
    {'CIF': 1.242, 'Pauling_CN12': 1.26}
    """

    rad_data = data()
    if element not in rad_data:
        raise KeyError(f"Element '{element}' not found in radius data.")

    return rad_data[element]


def supported_elements() -> list[str]:
    """Get a list of supported elements.

    Returns
    -------
    list[str]
        A list of chemical symbols for the elements that have radius data.

    Examples
    --------
    >>> get_supported_elements()
    ['Si', 'Sc', 'Fe', ...]
    """
    return list(data().keys())


def are_available(elements: list[str]) -> bool:
    """Check if all elements in the list are supported.

    Parameters
    ----------
    elements : list[str]
        A list of chemical symbols of elements.

    Returns
    -------
    bool
        True if all elements are supported, False otherwise.

    Examples
    --------
    >>> are_all_available(["Fe", "O", "N"])
    True
    >>> are_all_available(["Fe", "UnknownElement"])
    False
    """
    return all(is_available(element) for element in elements)


def is_available(element: str) -> bool:
    """Check if an element is supported.

    Parameters
    ----------
    element : str
        The chemical symbol of the element.

    Returns
    -------
    bool
        True if the element is supported, False otherwise.

    Examples
    --------
    >>> is_supported("Fe")
    True
    >>> is_supported("UnknownElement")
    False
    """
    return element in supported_elements()
