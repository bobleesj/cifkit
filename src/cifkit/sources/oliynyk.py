import importlib
from enum import Enum

import pandas as pd

from cifkit.parsers.formula import Formula


class Property(str, Enum):
    AW = "atomic_weight"
    ATOMIC_NUMBER = "atomic_number"
    PERIOD = "period"
    GROUP = "group"
    MEND_NUM = "Mendeleev_number"
    VAL_TOTAL = "valencee_total"
    UNPARIED_E = "unpaired_electrons"
    GILMAN = "Gilman"
    Z_EFF = "Z_eff"
    ION_ENERGY = "ionization_energy"
    COORD_NUM = "coordination_number"
    RATIO_CLOSEST = "ratio_closest"
    POLYHEDRON_DISTORT = "polyhedron_distortion"
    CIF_RADIUS = "CIF_radius"
    PAULING_RADIUS_CN12 = "Pauling_radius_CN12"
    PAULING_EN = "Pauling_EN"
    MARTYNOV_BATSANOV_EN = "Martynov_Batsanov_EN"
    MELTING_POINT_K = "melting_point_K"
    DENSITY = "density"
    SPECIFIC_HEAT = "specific_heat"
    COHESIVE_ENERGY = "cohesive_energy"
    BULK_MODULUS = "bulk_modulus"

    @classmethod
    def display(cls):
        """Display the available elemental properties in a user-friendly
        format.

        Examples
        --------
        >>> Property.display()
        Available elemental properties:
          1. AW - atomic_weight
          2. ATOMIC_NUMBER - atomic_number
          ...
        """
        print("\nAvailable elemental properties:")
        for index, prop in enumerate(cls, start=1):
            print(f"  {index}. {prop.name} - {prop.value}")

    @classmethod
    def select(cls):
        """Prompt the user to select an elemental property from the
        available options. Returns the selected property.

        Examples
        --------
        >>> selected_property = Property.select()
        Available elemental properties:
          1. AW - atomic_weight
          2. ATOMIC_NUMBER - atomic_number
          ...

        Enter the number of the property to use: 1
        """

        cls.display()
        try:
            choice = int(input("\nEnter the number of the property to use: "))
            selected = list(cls)[choice - 1]
            print(f"\nYou selected: {selected.name} → {selected.value}")
            return selected
        except (IndexError, ValueError):
            print("Invalid choice. Please enter a valid number.")
            return None


class Oliynyk:
    """Oliynyk elemental property database interface."""

    def __init__(self):
        self.db = self.get_oliynyk_CAF_data()
        self.elements = self.list_supported_elements()

    def get_oliynyk_CAF_data(self) -> dict[str, dict[str, float]]:
        """Load the Oliynyk elemental property data from an Excel file.
        The data is stored in a dictionary format with element symbols
        as keys.

        Examples
        --------
        >>> oliynyk = Oliynyk()
        >>> data = oliynyk.get_oliynyk_CAF_data()
        {
            "Li": {"atomic_weight": 6.941, ...},
            "Be": {"atomic_weight": 9.0122, ...},
            ...
        }
        >>> data["Li"]["atomic_weight"]
        6.941
        """

        with importlib.resources.path(
            "cifkit.data.db", "oliynyk-elemental-property-list.xlsx"
        ) as path:
            oliynyk_df = pd.read_excel(path)
        oliynyk_df.columns = oliynyk_df.columns.str.replace(" ", "", regex=False)
        oliynyk_df = oliynyk_df.fillna(0)
        oliynyk_dict = oliynyk_df.set_index("symbol").to_dict(orient="index")
        return oliynyk_dict

    def is_formula_supported(self, formula: str) -> bool:
        """Check if a formula is supported by the Oliynyk database.

        Examples
        --------
        >>> oliynyk = Oliynyk()
        >>> oliynyk.is_formula_supported("LiFePO4")
        True
        >>> oliynyk.is_formula_supported("FeH")
        False
        """
        elements_parsed = Formula(formula).elements
        return all(element in self.elements for element in elements_parsed)

    def get_supported_formulas(self, formulas: list[str]) -> tuple[list[str], list[str]]:
        """Filter formulas to only include those with supported
        elements.

        Examples
        --------
        >>> oliynyk = Oliynyk()
        >>> formulas = ["FeH", "NdSi2"]
        >>> supported, unsupported = oliynyk.get_supported_formulas(formulas)
        >>> supported
        ["NdSi2"]
        >>> unsupported
        ["FeH"]
        """
        supported, unsupported = [], []
        for formula in formulas:
            if self.is_formula_supported(formula):
                supported.append(formula)
            else:
                unsupported.append(formula)
        return supported, unsupported

    def list_supported_elements(self) -> list[str]:
        """List all elements in the Oliynyk database.

        Examples
        --------
        >>> oliynyk = Oliynyk()
        >>> elements = oliynyk.list_supported_elements()
        >>> elements
        ["Li", "Be", "B", "C", "Na", "Mg", "Al", "Si", "P", "S", ...]
        """
        return list(self.db.keys())

    def get_property_data_for_formula(
        self, formula: str, property: Property
    ) -> dict[str, float]:
        """Get property data for individual elements in a given formula.

        Examples
        --------
        >>> oliynyk = Oliynyk()
        >>> oliynyk.get_property_data_for_formula("LiFeP", Property.AW)
        {"Li": 6.941, "Fe": 55.845, "O": 15.999}
        """
        elements = Formula(formula).elements
        return {element: self.db[element][property] for element in elements}

    def get_property_data(self, property: Property) -> dict[str, float]:
        """Get the given property data for all elements in the database.

        Examples
        --------
        >>> oliynyk = Oliynyk()
        >>> property_data = oliynyk.get_property_data(Property.AW)
        >>> property_data
        {"Li": 6.941, "Be": 9.0122, "B": 10.81, ...}
        """
        return {element: self.db[element][property] for element in self.elements}
