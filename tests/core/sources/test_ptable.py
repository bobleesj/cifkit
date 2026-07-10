from cifkit.data.element import Element
from cifkit.sources.ptable import (
    get_data,
    values_from_atomic_number,
    values_from_name,
    values_from_symbol,
)


def test_get_values_from_atomic_number():
    element = values_from_atomic_number(1)
    assert element["atomic_number"] == 1
    assert element["name"] == "Hydrogen"
    assert element["symbol"] == "H"
    assert element["atomic_mass"] == 1.008


def test_get_values_from_symbol():
    element = values_from_symbol(Element.He.symbol)
    assert element["atomic_number"] == 2
    assert element["name"] == "Helium"
    assert element["symbol"] == "He"
    assert element["atomic_mass"] == 4.0026


def test_get_values_from_name():
    element = values_from_name(Element.Li.full_name)
    assert element["atomic_number"] == 3
    assert element["name"] == "Lithium"
    assert element["symbol"] == "Li"
    assert element["atomic_mass"] == 7


def test_get_data():
    actual_data = get_data()
    assert actual_data == [
        {
            "atomic_number": 1,
            "name": "Hydrogen",
            "symbol": "H",
            "atomic_mass": 1.008,
        },
        {
            "atomic_number": 2,
            "name": "Helium",
            "symbol": "He",
            "atomic_mass": 4.0026,
        },
        {
            "atomic_number": 3,
            "name": "Lithium",
            "symbol": "Li",
            "atomic_mass": 7,
        },
        {
            "atomic_number": 4,
            "name": "Beryllium",
            "symbol": "Be",
            "atomic_mass": 9.012183,
        },
        {
            "atomic_number": 5,
            "name": "Boron",
            "symbol": "B",
            "atomic_mass": 10.81,
        },
        {
            "atomic_number": 6,
            "name": "Carbon",
            "symbol": "C",
            "atomic_mass": 12.011,
        },
        {
            "atomic_number": 7,
            "name": "Nitrogen",
            "symbol": "N",
            "atomic_mass": 14.007,
        },
        {
            "atomic_number": 8,
            "name": "Oxygen",
            "symbol": "O",
            "atomic_mass": 15.999,
        },
        {
            "atomic_number": 9,
            "name": "Fluorine",
            "symbol": "F",
            "atomic_mass": 18.99840316,
        },
        {
            "atomic_number": 10,
            "name": "Neon",
            "symbol": "Ne",
            "atomic_mass": 20.18,
        },
        {
            "atomic_number": 11,
            "name": "Sodium",
            "symbol": "Na",
            "atomic_mass": 22.9897693,
        },
        {
            "atomic_number": 12,
            "name": "Magnesium",
            "symbol": "Mg",
            "atomic_mass": 24.305,
        },
        {
            "atomic_number": 13,
            "name": "Aluminum",
            "symbol": "Al",
            "atomic_mass": 26.981538,
        },
        {
            "atomic_number": 14,
            "name": "Silicon",
            "symbol": "Si",
            "atomic_mass": 28.085,
        },
        {
            "atomic_number": 15,
            "name": "Phosphorus",
            "symbol": "P",
            "atomic_mass": 30.973762,
        },
        {
            "atomic_number": 16,
            "name": "Sulfur",
            "symbol": "S",
            "atomic_mass": 32.07,
        },
        {
            "atomic_number": 17,
            "name": "Chlorine",
            "symbol": "Cl",
            "atomic_mass": 35.45,
        },
        {
            "atomic_number": 18,
            "name": "Argon",
            "symbol": "Ar",
            "atomic_mass": 39.9,
        },
        {
            "atomic_number": 19,
            "name": "Potassium",
            "symbol": "K",
            "atomic_mass": 39.0983,
        },
        {
            "atomic_number": 20,
            "name": "Calcium",
            "symbol": "Ca",
            "atomic_mass": 40.08,
        },
        {
            "atomic_number": 21,
            "name": "Scandium",
            "symbol": "Sc",
            "atomic_mass": 44.95591,
        },
        {
            "atomic_number": 22,
            "name": "Titanium",
            "symbol": "Ti",
            "atomic_mass": 47.867,
        },
        {
            "atomic_number": 23,
            "name": "Vanadium",
            "symbol": "V",
            "atomic_mass": 50.9415,
        },
        {
            "atomic_number": 24,
            "name": "Chromium",
            "symbol": "Cr",
            "atomic_mass": 51.996,
        },
        {
            "atomic_number": 25,
            "name": "Manganese",
            "symbol": "Mn",
            "atomic_mass": 54.93804,
        },
        {
            "atomic_number": 26,
            "name": "Iron",
            "symbol": "Fe",
            "atomic_mass": 55.84,
        },
        {
            "atomic_number": 27,
            "name": "Cobalt",
            "symbol": "Co",
            "atomic_mass": 58.93319,
        },
        {
            "atomic_number": 28,
            "name": "Nickel",
            "symbol": "Ni",
            "atomic_mass": 58.693,
        },
        {
            "atomic_number": 29,
            "name": "Copper",
            "symbol": "Cu",
            "atomic_mass": 63.55,
        },
        {
            "atomic_number": 30,
            "name": "Zinc",
            "symbol": "Zn",
            "atomic_mass": 65.4,
        },
        {
            "atomic_number": 31,
            "name": "Gallium",
            "symbol": "Ga",
            "atomic_mass": 69.723,
        },
        {
            "atomic_number": 32,
            "name": "Germanium",
            "symbol": "Ge",
            "atomic_mass": 72.63,
        },
        {
            "atomic_number": 33,
            "name": "Arsenic",
            "symbol": "As",
            "atomic_mass": 74.92159,
        },
        {
            "atomic_number": 34,
            "name": "Selenium",
            "symbol": "Se",
            "atomic_mass": 78.97,
        },
        {
            "atomic_number": 35,
            "name": "Bromine",
            "symbol": "Br",
            "atomic_mass": 79.9,
        },
        {
            "atomic_number": 36,
            "name": "Krypton",
            "symbol": "Kr",
            "atomic_mass": 83.8,
        },
        {
            "atomic_number": 37,
            "name": "Rubidium",
            "symbol": "Rb",
            "atomic_mass": 85.468,
        },
        {
            "atomic_number": 38,
            "name": "Strontium",
            "symbol": "Sr",
            "atomic_mass": 87.62,
        },
        {
            "atomic_number": 39,
            "name": "Yttrium",
            "symbol": "Y",
            "atomic_mass": 88.90584,
        },
        {
            "atomic_number": 40,
            "name": "Zirconium",
            "symbol": "Zr",
            "atomic_mass": 91.22,
        },
        {
            "atomic_number": 41,
            "name": "Niobium",
            "symbol": "Nb",
            "atomic_mass": 92.90637,
        },
        {
            "atomic_number": 42,
            "name": "Molybdenum",
            "symbol": "Mo",
            "atomic_mass": 95.95,
        },
        {
            "atomic_number": 43,
            "name": "Technetium",
            "symbol": "Tc",
            "atomic_mass": 96.90636,
        },
        {
            "atomic_number": 44,
            "name": "Ruthenium",
            "symbol": "Ru",
            "atomic_mass": 101.1,
        },
        {
            "atomic_number": 45,
            "name": "Rhodium",
            "symbol": "Rh",
            "atomic_mass": 102.9055,
        },
        {
            "atomic_number": 46,
            "name": "Palladium",
            "symbol": "Pd",
            "atomic_mass": 106.42,
        },
        {
            "atomic_number": 47,
            "name": "Silver",
            "symbol": "Ag",
            "atomic_mass": 107.868,
        },
        {
            "atomic_number": 48,
            "name": "Cadmium",
            "symbol": "Cd",
            "atomic_mass": 112.41,
        },
        {
            "atomic_number": 49,
            "name": "Indium",
            "symbol": "In",
            "atomic_mass": 114.818,
        },
        {
            "atomic_number": 50,
            "name": "Tin",
            "symbol": "Sn",
            "atomic_mass": 118.71,
        },
        {
            "atomic_number": 51,
            "name": "Antimony",
            "symbol": "Sb",
            "atomic_mass": 121.76,
        },
        {
            "atomic_number": 52,
            "name": "Tellurium",
            "symbol": "Te",
            "atomic_mass": 127.6,
        },
        {
            "atomic_number": 53,
            "name": "Iodine",
            "symbol": "I",
            "atomic_mass": 126.9045,
        },
        {
            "atomic_number": 54,
            "name": "Xenon",
            "symbol": "Xe",
            "atomic_mass": 131.29,
        },
        {
            "atomic_number": 55,
            "name": "Cesium",
            "symbol": "Cs",
            "atomic_mass": 132.905452,
        },
        {
            "atomic_number": 56,
            "name": "Barium",
            "symbol": "Ba",
            "atomic_mass": 137.33,
        },
        {
            "atomic_number": 57,
            "name": "Lanthanum",
            "symbol": "La",
            "atomic_mass": 138.9055,
        },
        {
            "atomic_number": 58,
            "name": "Cerium",
            "symbol": "Ce",
            "atomic_mass": 140.116,
        },
        {
            "atomic_number": 59,
            "name": "Praseodymium",
            "symbol": "Pr",
            "atomic_mass": 140.90766,
        },
        {
            "atomic_number": 60,
            "name": "Neodymium",
            "symbol": "Nd",
            "atomic_mass": 144.24,
        },
        {
            "atomic_number": 61,
            "name": "Promethium",
            "symbol": "Pm",
            "atomic_mass": 144.91276,
        },
        {
            "atomic_number": 62,
            "name": "Samarium",
            "symbol": "Sm",
            "atomic_mass": 150.4,
        },
        {
            "atomic_number": 63,
            "name": "Europium",
            "symbol": "Eu",
            "atomic_mass": 151.964,
        },
        {
            "atomic_number": 64,
            "name": "Gadolinium",
            "symbol": "Gd",
            "atomic_mass": 157.25,
        },
        {
            "atomic_number": 65,
            "name": "Terbium",
            "symbol": "Tb",
            "atomic_mass": 158.92535,
        },
        {
            "atomic_number": 66,
            "name": "Dysprosium",
            "symbol": "Dy",
            "atomic_mass": 162.5,
        },
        {
            "atomic_number": 67,
            "name": "Holmium",
            "symbol": "Ho",
            "atomic_mass": 164.93033,
        },
        {
            "atomic_number": 68,
            "name": "Erbium",
            "symbol": "Er",
            "atomic_mass": 167.26,
        },
        {
            "atomic_number": 69,
            "name": "Thulium",
            "symbol": "Tm",
            "atomic_mass": 168.93422,
        },
        {
            "atomic_number": 70,
            "name": "Ytterbium",
            "symbol": "Yb",
            "atomic_mass": 173.05,
        },
        {
            "atomic_number": 71,
            "name": "Lutetium",
            "symbol": "Lu",
            "atomic_mass": 174.9667,
        },
        {
            "atomic_number": 72,
            "name": "Hafnium",
            "symbol": "Hf",
            "atomic_mass": 178.49,
        },
        {
            "atomic_number": 73,
            "name": "Tantalum",
            "symbol": "Ta",
            "atomic_mass": 180.9479,
        },
        {
            "atomic_number": 74,
            "name": "Tungsten",
            "symbol": "W",
            "atomic_mass": 183.84,
        },
        {
            "atomic_number": 75,
            "name": "Rhenium",
            "symbol": "Re",
            "atomic_mass": 186.207,
        },
        {
            "atomic_number": 76,
            "name": "Osmium",
            "symbol": "Os",
            "atomic_mass": 190.2,
        },
        {
            "atomic_number": 77,
            "name": "Iridium",
            "symbol": "Ir",
            "atomic_mass": 192.22,
        },
        {
            "atomic_number": 78,
            "name": "Platinum",
            "symbol": "Pt",
            "atomic_mass": 195.08,
        },
        {
            "atomic_number": 79,
            "name": "Gold",
            "symbol": "Au",
            "atomic_mass": 196.96657,
        },
        {
            "atomic_number": 80,
            "name": "Mercury",
            "symbol": "Hg",
            "atomic_mass": 200.59,
        },
        {
            "atomic_number": 81,
            "name": "Thallium",
            "symbol": "Tl",
            "atomic_mass": 204.383,
        },
        {
            "atomic_number": 82,
            "name": "Lead",
            "symbol": "Pb",
            "atomic_mass": 207,
        },
        {
            "atomic_number": 83,
            "name": "Bismuth",
            "symbol": "Bi",
            "atomic_mass": 208.9804,
        },
        {
            "atomic_number": 84,
            "name": "Polonium",
            "symbol": "Po",
            "atomic_mass": 208.98243,
        },
        {
            "atomic_number": 85,
            "name": "Astatine",
            "symbol": "At",
            "atomic_mass": 209.98715,
        },
        {
            "atomic_number": 86,
            "name": "Radon",
            "symbol": "Rn",
            "atomic_mass": 222.01758,
        },
        {
            "atomic_number": 87,
            "name": "Francium",
            "symbol": "Fr",
            "atomic_mass": 223.01973,
        },
        {
            "atomic_number": 88,
            "name": "Radium",
            "symbol": "Ra",
            "atomic_mass": 226.02541,
        },
        {
            "atomic_number": 89,
            "name": "Actinium",
            "symbol": "Ac",
            "atomic_mass": 227.02775,
        },
        {
            "atomic_number": 90,
            "name": "Thorium",
            "symbol": "Th",
            "atomic_mass": 232.038,
        },
        {
            "atomic_number": 91,
            "name": "Protactinium",
            "symbol": "Pa",
            "atomic_mass": 231.03588,
        },
        {
            "atomic_number": 92,
            "name": "Uranium",
            "symbol": "U",
            "atomic_mass": 238.0289,
        },
        {
            "atomic_number": 93,
            "name": "Neptunium",
            "symbol": "Np",
            "atomic_mass": 237.048172,
        },
        {
            "atomic_number": 94,
            "name": "Plutonium",
            "symbol": "Pu",
            "atomic_mass": 244.0642,
        },
        {
            "atomic_number": 95,
            "name": "Americium",
            "symbol": "Am",
            "atomic_mass": 243.06138,
        },
        {
            "atomic_number": 96,
            "name": "Curium",
            "symbol": "Cm",
            "atomic_mass": 247.07035,
        },
        {
            "atomic_number": 97,
            "name": "Berkelium",
            "symbol": "Bk",
            "atomic_mass": 247.07031,
        },
        {
            "atomic_number": 98,
            "name": "Californium",
            "symbol": "Cf",
            "atomic_mass": 251.07959,
        },
        {
            "atomic_number": 99,
            "name": "Einsteinium",
            "symbol": "Es",
            "atomic_mass": 252.083,
        },
        {
            "atomic_number": 100,
            "name": "Fermium",
            "symbol": "Fm",
            "atomic_mass": 257.09511,
        },
        {
            "atomic_number": 101,
            "name": "Mendelevium",
            "symbol": "Md",
            "atomic_mass": 258.09843,
        },
        {
            "atomic_number": 102,
            "name": "Nobelium",
            "symbol": "No",
            "atomic_mass": 259.101,
        },
        {
            "atomic_number": 103,
            "name": "Lawrencium",
            "symbol": "Lr",
            "atomic_mass": 266.12,
        },
        {
            "atomic_number": 104,
            "name": "Rutherfordium",
            "symbol": "Rf",
            "atomic_mass": 267.122,
        },
        {
            "atomic_number": 105,
            "name": "Dubnium",
            "symbol": "Db",
            "atomic_mass": 268.126,
        },
        {
            "atomic_number": 106,
            "name": "Seaborgium",
            "symbol": "Sg",
            "atomic_mass": 269.128,
        },
        {
            "atomic_number": 107,
            "name": "Bohrium",
            "symbol": "Bh",
            "atomic_mass": 270.133,
        },
        {
            "atomic_number": 108,
            "name": "Hassium",
            "symbol": "Hs",
            "atomic_mass": 269.1336,
        },
        {
            "atomic_number": 109,
            "name": "Meitnerium",
            "symbol": "Mt",
            "atomic_mass": 277.154,
        },
        {
            "atomic_number": 110,
            "name": "Darmstadtium",
            "symbol": "Ds",
            "atomic_mass": 282.166,
        },
        {
            "atomic_number": 111,
            "name": "Roentgenium",
            "symbol": "Rg",
            "atomic_mass": 282.169,
        },
        {
            "atomic_number": 112,
            "name": "Copernicium",
            "symbol": "Cn",
            "atomic_mass": 286.179,
        },
        {
            "atomic_number": 113,
            "name": "Nihonium",
            "symbol": "Nh",
            "atomic_mass": 286.182,
        },
        {
            "atomic_number": 114,
            "name": "Flerovium",
            "symbol": "Fl",
            "atomic_mass": 290.192,
        },
        {
            "atomic_number": 115,
            "name": "Moscovium",
            "symbol": "Mc",
            "atomic_mass": 290.196,
        },
        {
            "atomic_number": 116,
            "name": "Livermorium",
            "symbol": "Lv",
            "atomic_mass": 293.205,
        },
        {
            "atomic_number": 117,
            "name": "Tennessine",
            "symbol": "Ts",
            "atomic_mass": 294.211,
        },
        {
            "atomic_number": 118,
            "name": "Oganesson",
            "symbol": "Og",
            "atomic_mass": 295.216,
        },
    ]
