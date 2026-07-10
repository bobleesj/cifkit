# Elemental data

New in **cifkit 1.2.1**: the elemental-data modules from the retired
`bobleesj.utils` package now live in cifkit. One install covers CIF
geometry and elemental features for featurization and sorting:

- `cifkit.sources.oliynyk` - the `Oliynyk` elemental property database
  (Excel-backed, 22 properties per element) and the `Property` enum
- `cifkit.parsers.formula` - the `Formula` parser
- `cifkit.sorters.element_sorter` - `ElementSorter`
- `cifkit.sources.mendeleev` / `ptable` / `radius` - raw data sources
- `cifkit.data.element` - the `Element` enum (all 118 elements)

All outputs below are real outputs from cifkit 1.2.1.

## Oliynyk elemental property database

The Oliynyk database ships inside the wheel as an Excel file and loads
into a plain nested dict - element symbol first, property second:

```python
from cifkit.sources.oliynyk import Oliynyk, Property

oliynyk = Oliynyk()
print(len(oliynyk.elements), "supported elements")
print(oliynyk.elements[:10])
```

```text
76 supported elements
['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Na', 'Mg', 'Al']
```

Look up single values through the `db` dict with a `Property` member
(it is a `str` enum, so it doubles as the column key):

```python
print(oliynyk.db["Si"][Property.AW])
print(oliynyk.db["Si"][Property.PAULING_EN])
print(oliynyk.db["Fe"][Property.MEND_NUM])
```

```text
28.0855
1.9
55
```

The 22 available properties:

```python
print(list(oliynyk.db["Si"].keys()))
```

```text
['atomic_weight', 'atomic_number', 'period', 'group', 'Mendeleev_number', 'valencee_total', 'unpaired_electrons', 'Gilman', 'Z_eff', 'ionization_energy', 'coordination_number', 'ratio_closest', 'polyhedron_distortion', 'CIF_radius', 'Pauling_radius_CN12', 'Pauling_EN', 'Martynov_Batsanov_EN', 'melting_point_K', 'density', 'specific_heat', 'cohesive_energy', 'bulk_modulus']
```

Call `Property.display()` in a terminal for a numbered menu, or
`Property.select()` for an interactive prompt.

### Per-formula and per-property views

```python
print(oliynyk.get_property_data_for_formula("NdSi2", Property.AW))

atomic_weights = oliynyk.get_property_data(Property.AW)
print(dict(list(atomic_weights.items())[:3]))
```

```text
{'Nd': 144.242, 'Si': 28.0855}
{'Li': 6.941, 'Be': 9.01218, 'B': 10.811}
```

### Screen formulas for support

Not every element is in the database (76 of 118), so screen input
formulas before featurizing:

```python
print(oliynyk.is_formula_supported("LiFePO4"))
supported, unsupported = oliynyk.get_supported_formulas(["FeH", "NdSi2", "UO2"])
print(supported, unsupported)
```

```text
True
['NdSi2', 'UO2'] ['FeH']
```

## Formula parsing

`Formula` parses a composition string into `(element, count)` pairs and
provides normalization plus list-level utilities:

```python
from cifkit.parsers.formula import Formula

formula = Formula("NdSi2")
print(formula.parsed_formula)
print(formula.elements)
print(formula.element_count)
print(formula.max_min_avg_index)
print(formula.get_normalized_formula())
print(formula.get_normalized_parsed_formula())
print(formula.get_normalized_indices())
```

```text
[('Nd', 1.0), ('Si', 2.0)]
['Nd', 'Si']
2
(2.0, 1.0, 1.5)
Nd0.333333Si0.666667
[('Nd', 0.333333), ('Si', 0.666667)]
[0.333333, 0.666667]
```

Element symbols are validated against the periodic table at parse time;
pass `validate=False` to allow placeholder symbols.

List-level helpers are static methods, so no instance is needed:

```python
formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
print(Formula.order_by_alphabetical(formulas))
print(Formula.count_by_composition(formulas))
print(Formula.get_unique_elements(["NdSi2", "ThOs"]))
```

```text
['NdSi2', 'NdSi2Th2', 'ThOs', 'YNdThSi2']
{2: 2, 3: 1, 4: 1}
{'Nd', 'Si', 'Os', 'Th'}
```

## ElementSorter

`ElementSorter` sorts element lists three ways: by custom site labels
(e.g. R/M/X roles in intermetallics), by Mendeleev number, or
alphabetically:

```python
from cifkit.sorters.element_sorter import ElementSorter

custom_labels = {
    2: {"A": ["Fe", "Co"], "B": ["Si", "Ga"]},
    3: {"R": ["Sc", "Y"], "M": ["Fe", "Co"], "X": ["Si", "Ga"]},
    4: {"A": ["Sc", "Y"], "B": ["Fe", "Co"], "C": ["Si", "Ga"], "D": ["Gd", "Tb", "Dy"]},
}
element_sorter = ElementSorter(label_mapping=custom_labels)
print(element_sorter.sort(["Si", "Fe"], method="custom"))
print(element_sorter.sort(["Si", "Sc", "Fe"], method="custom"))

plain_sorter = ElementSorter()
print(plain_sorter.sort(["O", "Fe"], method="mendeleev"))
print(plain_sorter.sort(["Si", "Fe"]))
```

```text
('Fe', 'Si')
('Sc', 'Fe', 'Si')
('O', 'Fe')
('Si', 'Fe')
```

The custom mapping can also come from an Excel file with `Binary`,
`Ternary`, and `Quaternary` sheets:
`ElementSorter(excel_path="labels.xlsx")`. Note the default sort order
is `descending=True`; the alphabetical example above returns
`('Si', 'Fe')` for that reason - pass `descending=False` for A-to-Z.

## Raw data sources

For direct access without the database object:

```python
from cifkit.sources import mendeleev, ptable, radius

print(mendeleev.numbers["Fe"])
print(ptable.get_data()[0])
print(radius.data()["Fe"])
```

```text
55
{'atomic_number': 1, 'name': 'Hydrogen', 'symbol': 'H', 'atomic_mass': 1.008}
{'CIF': 1.242, 'Pauling_CN12': 1.26}
```

## Element enum and quick stats

```python
from cifkit.data.element import Element
from cifkit.numbers import calculate_basic_stats

print(Element.Fe.symbol, Element.Fe.full_name)
print(len(Element.all_symbols()), "elements")
print(calculate_basic_stats([1.0, 2.0, 3.0, 4.0]))
```

```text
Fe Iron
118 elements
{'max': 4.0, 'min': 1.0, 'mid': 2.5, 'avg': 2.5, 'std': 1.118033988749895, 'var': 1.25}
```

Full signatures live in the API reference: [Oliynyk](../api/oliynyk),
[Formula](../api/formula), [ElementSorter](../api/element-sorter), and
[Sources](../api/sources).
