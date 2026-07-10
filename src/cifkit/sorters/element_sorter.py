import itertools

import pandas as pd

from cifkit.sources import mendeleev


class ElementSorter:
    """Sort chemical elements by custom labels, Mendeleev numbers, or
    alphabetically.

    Parameters
    ----------
    label_mapping : dict, optional
        The custom label mapping for sorting elements.
    excel_path : str, optional
        The path to Excel file with custom labels.
        It overrides `label_mapping` if provided.

    Examples
    --------
    >>> element_sorter = ElementSorter(excel_path="labels.xlsx")
    >>> element_sorter.sort(["Fe", "Si"], method="custom")
    ('Fe', 'Si')
    >>> custom_labels = {
    ...     2: {"A": ["Fe", "Co"], "B": ["Si", "Ga"]},
    ...     3: {"R": ["Sc", "Y"], "M": ["Fe", "Co"],
                "X": ["Si", "Ga"]},
    ...     4: {"A": ["Sc", "Y"], "B": ["Fe", "Co"],
                "C": ["Si", "Ga"], "D": ["Gd", "Tb", "Dy"]},
    ... }
    >>> element_sorter = ElementSorter(label_mapping=custom_labels)
    >>> element_sorter.sort(["Sc", "Fe", "Si"], method="custom")
    ('Sc', 'Fe', 'Si')
    >>> element_sorter.sort(["O", "Fe"], method="mendeleev")
    ('O', 'Fe')
    """

    def __init__(self, label_mapping: dict = None, excel_path: str = None):
        if label_mapping:
            self.label_mapping = label_mapping
        elif excel_path:
            self.label_mapping = self._load_labels_from_excel(excel_path)

    def _load_labels_from_excel(self, excel_path: str) -> dict:
        sheet_map = {
            2: ("Binary", ["Element_A", "Element_B"]),
            3: ("Ternary", ["Element_R", "Element_M", "Element_X"]),
            4: (
                "Quaternary",
                ["Element_A", "Element_B", "Element_C", "Element_D"],
            ),
        }
        label_keys_map = {
            2: ["A", "B"],
            3: ["R", "M", "X"],
            4: ["A", "B", "C", "D"],
        }

        custom_labels = {}
        for num_elements, (sheet, columns) in sheet_map.items():
            df = pd.read_excel(excel_path, sheet_name=sheet, engine="openpyxl")
            element_lists = [df[col].dropna().tolist() for col in columns]
            label_keys = label_keys_map[num_elements]
            custom_labels[num_elements] = {
                label: elements for label, elements in zip(label_keys, element_lists)
            }
        return custom_labels

    def sort(self, elements: list[str], method=None, descending: bool = True) -> tuple:
        """Sort a list of elements.

        Parameters
        ----------
        elements : list of str
            Element symbols to sort (e.g., ['Fe', 'O']).
        method : str or None, optional
            'custom': custom label-based sorting.
            'mendeleev': by Mendeleev numbers.
            None/other: alphabetical (default).
        descending : bool, default=True
            Sort descending.

        Returns
        -------
        tuple
            Sorted element symbols.

        Raises
        ------
        ValueError
            If method is unsupported or custom sorting fails.

        Examples
        --------
        >>> elements.sort(["O", "Fe"], descending=False)
        ('Fe', 'O')
        >>> elements.sort(['O', 'Fe'], method="mendeleev")
        ('O', 'Fe')
        >>> elements.sort(["Fe", "O"], method="custom")
        ('Fe', 'O')
        """
        length = len(elements)
        if method is None:
            return tuple(sorted(elements, reverse=descending))
        elif method == "mendeleev":
            try:
                sorted_elements = sorted(
                    elements,
                    key=lambda el: mendeleev.numbers[el],
                    reverse=descending,
                )
                return tuple(sorted_elements)
            except KeyError as e:
                raise ValueError(f"Unknown element in Mendeleev sort: {e}")
        elif method == "custom":
            if self.label_mapping is None:
                raise ValueError(
                    "Custom label mapping is not defined. "
                    "Provide a valid label_mapping or excel_path "
                    "when you instantiate the Elements class."
                )
            if length not in self.label_mapping:
                raise ValueError(f"No label mapping found for {length}-element systems.")
            if length == 2:
                return self._sort_binary(elements)
            elif length == 3:
                return self._sort_ternary(elements)
            elif length == 4:
                return self._sort_quaternary(elements)
            else:
                raise ValueError("Only 2, 3, or 4-element systems are supported.")
        else:
            raise ValueError(f"Unknown sort method: {method}")

    def _sort_binary(self, elements: list[str]) -> tuple[str, str]:
        if len(elements) != 2:
            raise ValueError("Input must contain exactly 2 elements.")
        labels = self.label_mapping[2]
        A, B = labels["A"], labels["B"]
        e0, e1 = elements
        if e0 in A and e1 in B:
            return e0, e1
        elif e1 in A and e0 in B:
            return e1, e0
        return tuple(sorted(elements))

    def _sort_ternary(self, elements: list[str]) -> tuple[str, str, str]:
        if len(elements) != 3:
            raise ValueError("Input must contain exactly 3 elements.")
        labels = self.label_mapping[3]
        for perm in itertools.permutations(elements):
            if (
                perm[0] in labels["R"]
                and perm[1] in labels["M"]
                and perm[2] in labels["X"]
            ):
                return perm
        raise ValueError(f"Could not determine R-M-X order for: {elements}")

    def _sort_quaternary(self, elements: list[str]) -> tuple[str, str, str, str]:
        if len(elements) != 4:
            raise ValueError("Input must contain exactly 4 elements.")
        labels = self.label_mapping[4]
        for perm in itertools.permutations(elements):
            if (
                perm[0] in labels["A"]
                and perm[1] in labels["B"]
                and perm[2] in labels["C"]
                and perm[3] in labels["D"]
            ):
                return perm
        raise ValueError(f"Could not determine A-B-C-D order for: {elements}")
