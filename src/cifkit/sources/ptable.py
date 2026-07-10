from cifkit.data.element import Element as E


def get_data():
    """Get the periodic table data.

    Sourced from
    https://pubchem.ncbi.nlm.nih.gov/ptable/atomic-mass/
    """

    def n(element):
        # Get the name of the element
        return element.full_name

    def s(element):
        # Get the symbol of the element.
        return element.symbol

    data = [
        (1, n(E.H), s(E.H), 1.008),
        (2, n(E.He), s(E.He), 4.0026),
        (3, n(E.Li), s(E.Li), 7.0),
        (4, n(E.Be), s(E.Be), 9.012183),
        (5, n(E.B), s(E.B), 10.81),
        (6, n(E.C), s(E.C), 12.011),
        (7, n(E.N), s(E.N), 14.007),
        (8, n(E.O), s(E.O), 15.999),
        (9, n(E.F), s(E.F), 18.99840316),
        (10, n(E.Ne), s(E.Ne), 20.18),
        (11, n(E.Na), s(E.Na), 22.9897693),
        (12, n(E.Mg), s(E.Mg), 24.305),
        (13, n(E.Al), s(E.Al), 26.981538),
        (14, n(E.Si), s(E.Si), 28.085),
        (15, n(E.P), s(E.P), 30.973762),
        (16, n(E.S), s(E.S), 32.07),
        (17, n(E.Cl), s(E.Cl), 35.45),
        (18, n(E.Ar), s(E.Ar), 39.9),
        (19, n(E.K), s(E.K), 39.0983),
        (20, n(E.Ca), s(E.Ca), 40.08),
        (21, n(E.Sc), s(E.Sc), 44.95591),
        (22, n(E.Ti), s(E.Ti), 47.867),
        (23, n(E.V), s(E.V), 50.9415),
        (24, n(E.Cr), s(E.Cr), 51.996),
        (25, n(E.Mn), s(E.Mn), 54.93804),
        (26, n(E.Fe), s(E.Fe), 55.84),
        (27, n(E.Co), s(E.Co), 58.93319),
        (28, n(E.Ni), s(E.Ni), 58.693),
        (29, n(E.Cu), s(E.Cu), 63.55),
        (30, n(E.Zn), s(E.Zn), 65.4),
        (31, n(E.Ga), s(E.Ga), 69.723),
        (32, n(E.Ge), s(E.Ge), 72.63),
        (33, n(E.As), s(E.As), 74.92159),
        (34, n(E.Se), s(E.Se), 78.97),
        (35, n(E.Br), s(E.Br), 79.9),
        (36, n(E.Kr), s(E.Kr), 83.8),
        (37, n(E.Rb), s(E.Rb), 85.468),
        (38, n(E.Sr), s(E.Sr), 87.62),
        (39, n(E.Y), s(E.Y), 88.90584),
        (40, n(E.Zr), s(E.Zr), 91.22),
        (41, n(E.Nb), s(E.Nb), 92.90637),
        (42, n(E.Mo), s(E.Mo), 95.95),
        (43, n(E.Tc), s(E.Tc), 96.90636),
        (44, n(E.Ru), s(E.Ru), 101.1),
        (45, n(E.Rh), s(E.Rh), 102.9055),
        (46, n(E.Pd), s(E.Pd), 106.42),
        (47, n(E.Ag), s(E.Ag), 107.868),
        (48, n(E.Cd), s(E.Cd), 112.41),
        (49, n(E.In), s(E.In), 114.818),
        (50, n(E.Sn), s(E.Sn), 118.71),
        (51, n(E.Sb), s(E.Sb), 121.76),
        (52, n(E.Te), s(E.Te), 127.6),
        (53, n(E.I), s(E.I), 126.9045),
        (54, n(E.Xe), s(E.Xe), 131.29),
        (55, n(E.Cs), s(E.Cs), 132.905452),
        (56, n(E.Ba), s(E.Ba), 137.33),
        (57, n(E.La), s(E.La), 138.9055),
        (58, n(E.Ce), s(E.Ce), 140.116),
        (59, n(E.Pr), s(E.Pr), 140.90766),
        (60, n(E.Nd), s(E.Nd), 144.24),
        (61, n(E.Pm), s(E.Pm), 144.91276),
        (62, n(E.Sm), s(E.Sm), 150.4),
        (63, n(E.Eu), s(E.Eu), 151.964),
        (64, n(E.Gd), s(E.Gd), 157.25),
        (65, n(E.Tb), s(E.Tb), 158.92535),
        (66, n(E.Dy), s(E.Dy), 162.5),
        (67, n(E.Ho), s(E.Ho), 164.93033),
        (68, n(E.Er), s(E.Er), 167.26),
        (69, n(E.Tm), s(E.Tm), 168.93422),
        (70, n(E.Yb), s(E.Yb), 173.05),
        (71, n(E.Lu), s(E.Lu), 174.9667),
        (72, n(E.Hf), s(E.Hf), 178.49),
        (73, n(E.Ta), s(E.Ta), 180.9479),
        (74, n(E.W), s(E.W), 183.84),
        (75, n(E.Re), s(E.Re), 186.207),
        (76, n(E.Os), s(E.Os), 190.2),
        (77, n(E.Ir), s(E.Ir), 192.22),
        (78, n(E.Pt), s(E.Pt), 195.08),
        (79, n(E.Au), s(E.Au), 196.96657),
        (80, n(E.Hg), s(E.Hg), 200.59),
        (81, n(E.Tl), s(E.Tl), 204.383),
        (82, n(E.Pb), s(E.Pb), 207),
        (83, n(E.Bi), s(E.Bi), 208.9804),
        (84, n(E.Po), s(E.Po), 208.98243),
        (85, n(E.At), s(E.At), 209.98715),
        (86, n(E.Rn), s(E.Rn), 222.01758),
        (87, n(E.Fr), s(E.Fr), 223.01973),
        (88, n(E.Ra), s(E.Ra), 226.02541),
        (89, n(E.Ac), s(E.Ac), 227.02775),
        (90, n(E.Th), s(E.Th), 232.038),
        (91, n(E.Pa), s(E.Pa), 231.03588),
        (92, n(E.U), s(E.U), 238.0289),
        (93, n(E.Np), s(E.Np), 237.048172),
        (94, n(E.Pu), s(E.Pu), 244.0642),
        (95, n(E.Am), s(E.Am), 243.06138),
        (96, n(E.Cm), s(E.Cm), 247.07035),
        (97, n(E.Bk), s(E.Bk), 247.07031),
        (98, n(E.Cf), s(E.Cf), 251.07959),
        (99, n(E.Es), s(E.Es), 252.083),
        (100, n(E.Fm), s(E.Fm), 257.09511),
        (101, n(E.Md), s(E.Md), 258.09843),
        (102, n(E.No), s(E.No), 259.101),
        (103, n(E.Lr), s(E.Lr), 266.12),
        (104, n(E.Rf), s(E.Rf), 267.122),
        (105, n(E.Db), s(E.Db), 268.126),
        (106, n(E.Sg), s(E.Sg), 269.128),
        (107, n(E.Bh), s(E.Bh), 270.133),
        (108, n(E.Hs), s(E.Hs), 269.1336),
        (109, n(E.Mt), s(E.Mt), 277.154),
        (110, n(E.Ds), s(E.Ds), 282.166),
        (111, n(E.Rg), s(E.Rg), 282.169),
        (112, n(E.Cn), s(E.Cn), 286.179),
        (113, n(E.Nh), s(E.Nh), 286.182),
        (114, n(E.Fl), s(E.Fl), 290.192),
        (115, n(E.Mc), s(E.Mc), 290.196),
        (116, n(E.Lv), s(E.Lv), 293.205),
        (117, n(E.Ts), s(E.Ts), 294.211),
        (118, n(E.Og), s(E.Og), 295.216),
    ]

    data = [
        {
            "atomic_number": num,
            "name": name,
            "symbol": symbol,
            "atomic_mass": atomic_mass,
        }
        for num, name, symbol, atomic_mass in data
    ]
    return data


def _get_element_by_key(key, value):
    """Helper to get element data by a specific key."""
    data = get_data()
    for element in data:
        if str(element[key]).lower() == str(value).lower():
            return element
    raise ValueError(f"Element with {key} '{value}' not found.")


def values_from_atomic_number(atomic_number):
    """Get the element data by atomic number."""
    return _get_element_by_key("atomic_number", atomic_number)


def values_from_symbol(symbol):
    """Get the element data by chemical symbol."""
    return _get_element_by_key("symbol", symbol)


def values_from_name(name):
    """Get the element data by name."""
    return _get_element_by_key("name", name)
