import pytest

from cifkit.sources.oliynyk import Property as P


@pytest.mark.parametrize(
    "property, expected_string",
    [
        (P.AW, "atomic_weight"),
        (P.ATOMIC_NUMBER, "atomic_number"),
        (P.GROUP, "group"),
        (P.PERIOD, "period"),
        (P.MEND_NUM, "Mendeleev_number"),
        (P.VAL_TOTAL, "valencee_total"),
        (P.UNPARIED_E, "unpaired_electrons"),
        (P.GILMAN, "Gilman"),
        (P.Z_EFF, "Z_eff"),
        (P.ION_ENERGY, "ionization_energy"),
        (P.COORD_NUM, "coordination_number"),
        (P.RATIO_CLOSEST, "ratio_closest"),
        (P.POLYHEDRON_DISTORT, "polyhedron_distortion"),
        (P.CIF_RADIUS, "CIF_radius"),
        (P.PAULING_RADIUS_CN12, "Pauling_radius_CN12"),
        (P.PAULING_EN, "Pauling_EN"),
        (P.MARTYNOV_BATSANOV_EN, "Martynov_Batsanov_EN"),
        (P.MELTING_POINT_K, "melting_point_K"),
        (P.DENSITY, "density"),
        (P.SPECIFIC_HEAT, "specific_heat"),
        (P.COHESIVE_ENERGY, "cohesive_energy"),
        (P.BULK_MODULUS, "bulk_modulus"),
    ],
)
def test_property(property, expected_string):
    assert property == expected_string


def test_get_oliynyk_CAF_data(oliynyk):
    # Number of elements in the database
    assert len(oliynyk.db) == 76
    assert oliynyk.db["Nd"]["atomic_weight"] == 144.242
    assert oliynyk.db["Nd"]["atomic_number"] == 60


def test_list_supported_elements(oliynyk):
    actual_elements = oliynyk.elements
    expected_elements = [
        "Li",
        "Be",
        "B",
        "C",
        "N",
        "O",
        "F",
        "Na",
        "Mg",
        "Al",
        "Si",
        "P",
        "S",
        "Cl",
        "K",
        "Ca",
        "Sc",
        "Ti",
        "V",
        "Cr",
        "Mn",
        "Fe",
        "Co",
        "Ni",
        "Cu",
        "Zn",
        "Ga",
        "Ge",
        "As",
        "Se",
        "Br",
        "Rb",
        "Sr",
        "Y",
        "Zr",
        "Nb",
        "Mo",
        "Ru",
        "Rh",
        "Pd",
        "Ag",
        "Cd",
        "In",
        "Sn",
        "Sb",
        "Te",
        "I",
        "Cs",
        "Ba",
        "La",
        "Ce",
        "Pr",
        "Nd",
        "Sm",
        "Eu",
        "Gd",
        "Tb",
        "Dy",
        "Ho",
        "Er",
        "Tm",
        "Yb",
        "Lu",
        "Hf",
        "Ta",
        "W",
        "Re",
        "Os",
        "Ir",
        "Pt",
        "Au",
        "Tl",
        "Pb",
        "Bi",
        "Th",
        "U",
    ]
    assert actual_elements == expected_elements


def test_get_property_data(oliynyk):
    actual_values = oliynyk.get_property_data(P.AW)
    expected_values = {
        "Li": 6.941,
        "Be": 9.01218,
        "B": 10.811,
        "C": 12.011,
        "N": 14.00674,
        "O": 15.9994,
        "F": 18.998403,
        "Na": 22.989768,
        "Mg": 24.305,
        "Al": 26.981539,
        "Si": 28.0855,
        "P": 30.973762,
        "S": 32.066,
        "Cl": 35.4527,
        "K": 39.0983,
        "Ca": 40.078,
        "Sc": 44.95591,
        "Ti": 47.867,
        "V": 50.9415,
        "Cr": 51.9961,
        "Mn": 54.93805,
        "Fe": 55.847,
        "Co": 58.9332,
        "Ni": 58.6934,
        "Cu": 63.546,
        "Zn": 65.38,
        "Ga": 69.723,
        "Ge": 72.63,
        "As": 74.92159,
        "Se": 78.971,
        "Br": 79.904,
        "Rb": 85.4678,
        "Sr": 87.62,
        "Y": 88.90584,
        "Zr": 91.224,
        "Nb": 92.90638,
        "Mo": 95.95,
        "Ru": 101.07,
        "Rh": 102.9055,
        "Pd": 106.42,
        "Ag": 107.8682,
        "Cd": 112.411,
        "In": 114.818,
        "Sn": 118.71,
        "Sb": 121.76,
        "Te": 127.6,
        "I": 126.90447,
        "Cs": 132.90543,
        "Ba": 137.327,
        "La": 138.9055,
        "Ce": 140.115,
        "Pr": 140.90765,
        "Nd": 144.242,
        "Sm": 150.36,
        "Eu": 151.965,
        "Gd": 157.25,
        "Tb": 158.92534,
        "Dy": 162.5,
        "Ho": 164.93032,
        "Er": 167.259,
        "Tm": 168.93421,
        "Yb": 173.045,
        "Lu": 174.967,
        "Hf": 178.49,
        "Ta": 180.9479,
        "W": 183.84,
        "Re": 186.207,
        "Os": 190.23,
        "Ir": 192.217,
        "Pt": 195.084,
        "Au": 196.96654,
        "Tl": 204.3833,
        "Pb": 207.2,
        "Bi": 208.98037,
        "Th": 232.0381,
        "U": 238.0289,
    }
    assert actual_values == expected_values


def test_get_property_data_from_formula(oliynyk):
    formula = "NdSi2"
    actual_data = oliynyk.get_property_data_for_formula(formula, P.MEND_NUM)
    expected_data = {"Nd": 19, "Si": 78}
    assert actual_data == expected_data


"""
Methods
"""


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("NdSi2", True),
        ("FeCo", True),
        ("SiGe", True),
        ("HCo", False),
        ("FeH", False),
        ("LaNi5", True),
        ("UTh", True),
        ("PtIr", True),
    ],
)
def test_is_formula_supported(formula, expected, oliynyk):
    assert oliynyk.is_formula_supported(formula) == expected


@pytest.mark.parametrize(
    "formulas, expected_supported, expected_unsupported",
    [
        (
            ["NdSi2", "FeCo", "LaNi5", "FeH", "PtIr", "HgH"],
            ["NdSi2", "FeCo", "LaNi5", "PtIr"],
            ["FeH", "HgH"],
        ),
        (
            ["SiGe", "UTh", "HGe", "PmO"],
            ["SiGe", "UTh"],
            ["HGe", "PmO"],
        ),
        (
            ["LiFePO4", "FeH", "NdSi2"],
            ["LiFePO4", "NdSi2"],
            ["FeH"],
        ),
        (
            ["Li", "Be", "B", "C"],
            ["Li", "Be", "B", "C"],
            [],
        ),
    ],
)
def test_filter_supported_formulas(
    formulas, expected_supported, expected_unsupported, oliynyk
):
    supported, unsupported = oliynyk.get_supported_formulas(formulas)
    assert supported == expected_supported
    assert unsupported == expected_unsupported
