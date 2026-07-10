"""Parity tests between cifkit's migrated elemental-data modules and the
original bobleesj.utils implementations.

Every test feeds the SAME input to the legacy bobleesj.utils code and the
migrated cifkit code and asserts exact equality. This is the migration
safety net: if any value, ordering, or parse result drifts during the move,
these tests fail. The whole module skips gracefully once bobleesj.utils is
archived and uninstalled, because the permanent behavioral coverage lives
in the ported unit tests.
"""

import pytest

legacy = pytest.importorskip(
    "bobleesj.utils",
    reason="legacy bobleesj.utils not installed; parity already validated",
)

from bobleesj.utils import numbers as legacy_numbers  # noqa: E402
from bobleesj.utils.data.element import Element as LegacyElement  # noqa: E402
from bobleesj.utils.parsers.formula import Formula as LegacyFormula  # noqa: E402
from bobleesj.utils.sorters.element_sorter import (  # noqa: E402
    ElementSorter as LegacyElementSorter,
)
from bobleesj.utils.sources import mendeleev as legacy_mendeleev  # noqa: E402
from bobleesj.utils.sources import ptable as legacy_ptable  # noqa: E402
from bobleesj.utils.sources import radius as legacy_radius  # noqa: E402
from bobleesj.utils.sources.oliynyk import Oliynyk as LegacyOliynyk  # noqa: E402
from bobleesj.utils.sources.oliynyk import Property as LegacyProperty  # noqa: E402

from cifkit import numbers  # noqa: E402
from cifkit.data.element import Element  # noqa: E402
from cifkit.parsers.formula import Formula  # noqa: E402
from cifkit.sorters.element_sorter import ElementSorter  # noqa: E402
from cifkit.sources import mendeleev, ptable, radius  # noqa: E402
from cifkit.sources.oliynyk import Oliynyk, Property  # noqa: E402

FORMULA_BATTERY = [
    "NdSi2",
    "ThOs",
    "NdSi2Th2",
    "YNdThSi2",
    "Er11Co4In9",
    "Fe2O3",
    "LiFePO4",
    "Co1.5Fe0.5Si",
]


@pytest.fixture(scope="module")
def legacy_oliynyk():
    return LegacyOliynyk()


@pytest.fixture(scope="module")
def migrated_oliynyk():
    return Oliynyk()


# --- Oliynyk elemental property database ---


def test_oliynyk_db_parity(legacy_oliynyk, migrated_oliynyk):
    # Full nested dict from the Excel source, expect bit-identical values
    assert migrated_oliynyk.db == legacy_oliynyk.db
    assert migrated_oliynyk.elements == legacy_oliynyk.elements


def test_oliynyk_property_enum_parity():
    # Same members in the same order with the same string values
    legacy_members = [(p.name, p.value) for p in LegacyProperty]
    migrated_members = [(p.name, p.value) for p in Property]
    assert migrated_members == legacy_members


@pytest.mark.parametrize("formula", FORMULA_BATTERY)
@pytest.mark.parametrize(
    "property_name", ["AW", "MEND_NUM", "PAULING_EN", "MELTING_POINT_K"]
)
def test_oliynyk_property_data_for_formula_parity(
    legacy_oliynyk, migrated_oliynyk, formula, property_name
):
    # Per-element property lookups for a formula, expect identical dicts
    legacy_value = legacy_oliynyk.get_property_data_for_formula(
        formula, LegacyProperty[property_name]
    )
    migrated_value = migrated_oliynyk.get_property_data_for_formula(
        formula, Property[property_name]
    )
    assert migrated_value == legacy_value


def test_oliynyk_formula_support_parity(legacy_oliynyk, migrated_oliynyk):
    # Support filtering splits the same list the same way ("FeH" has H,
    # which the database does not carry)
    formulas = FORMULA_BATTERY + ["FeH", "UO2"]
    assert migrated_oliynyk.get_supported_formulas(
        formulas
    ) == legacy_oliynyk.get_supported_formulas(formulas)


# --- Formula parser ---


@pytest.mark.parametrize("formula", FORMULA_BATTERY)
def test_formula_parse_parity(formula):
    # Parsing, element/index extraction, and normalization all agree
    legacy_parsed = LegacyFormula(formula)
    migrated_parsed = Formula(formula)
    assert migrated_parsed.parsed_formula == legacy_parsed.parsed_formula
    assert migrated_parsed.elements == legacy_parsed.elements
    assert migrated_parsed.indices == legacy_parsed.indices
    assert migrated_parsed._normalized() == legacy_parsed._normalized()


def test_formula_static_helpers_parity():
    # Collection-level helpers produce identical counts and orderings
    formulas = FORMULA_BATTERY + ["NdSi2", "ThOs"]
    assert Formula.order_by_alphabetical(formulas) == LegacyFormula.order_by_alphabetical(
        formulas
    )
    assert Formula.count_unique(formulas) == LegacyFormula.count_unique(formulas)
    assert Formula.get_unique_elements(formulas) == LegacyFormula.get_unique_elements(
        formulas
    )
    assert Formula.get_element_count(formulas) == LegacyFormula.get_element_count(
        formulas
    )
    assert Formula.count_duplicates(formulas) == LegacyFormula.count_duplicates(formulas)


# --- Element sorter ---


@pytest.mark.parametrize(
    "elements",
    [
        # C1: binary, expect Mendeleev-number order
        ["Si", "Fe"],
        # C2: ternary
        ["Si", "Fe", "La"],
        # C3: quaternary
        ["Si", "Fe", "La", "Co"],
    ],
)
def test_element_sorter_mendeleev_parity(elements):
    legacy_sorted = LegacyElementSorter().sort(elements)
    migrated_sorted = ElementSorter().sort(elements)
    assert migrated_sorted == legacy_sorted


def test_element_sorter_custom_labels_parity():
    # Custom label mapping drives the same order in both implementations
    custom_labels = {
        2: {"A": ["Fe", "Co", "Ni"], "B": ["Si", "Ga", "Ge"]},
        3: {
            "R": ["Sc", "Y", "La"],
            "M": ["Fe", "Co", "Ni"],
            "X": ["Si", "Ga", "Ge"],
        },
    }
    legacy_sorter = LegacyElementSorter(label_mapping=custom_labels)
    migrated_sorter = ElementSorter(label_mapping=custom_labels)
    for elements in (["Ge", "Co"], ["Si", "La", "Fe"]):
        assert migrated_sorter.sort(elements, method="custom") == legacy_sorter.sort(
            elements, method="custom"
        )


# --- Static element data sources ---


def test_mendeleev_numbers_parity():
    assert mendeleev.numbers == legacy_mendeleev.numbers


def test_radius_data_parity():
    assert radius.data() == legacy_radius.data()
    assert radius.supported_elements() == legacy_radius.supported_elements()
    for element in radius.supported_elements():
        assert radius.value(element) == legacy_radius.value(element)


def test_ptable_data_parity():
    assert ptable.get_data() == legacy_ptable.get_data()
    # Lookup helpers agree across all three key types
    assert ptable.values_from_symbol("Fe") == legacy_ptable.values_from_symbol("Fe")
    assert ptable.values_from_atomic_number(
        26
    ) == legacy_ptable.values_from_atomic_number(26)
    assert ptable.values_from_name("Iron") == legacy_ptable.values_from_name("Iron")


def test_element_enum_parity():
    legacy_members = [(e.name, e.value) for e in LegacyElement]
    migrated_members = [(e.name, e.value) for e in Element]
    assert migrated_members == legacy_members


# --- Numbers ---


def test_calculate_basic_stats_parity():
    values = [1.5, 2.0, 3.25, 4.0, 5.75, 8.125]
    assert numbers.calculate_basic_stats(values) == legacy_numbers.calculate_basic_stats(
        values
    )
