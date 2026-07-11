# OLED / Oliynyk

**OLED** = **O**liynyk **E**lemental **D**ata: 22 physics/chemistry
properties for 76 elements, for **composition featurization** (ML).

```python
from cifkit.sources.oliynyk import Oliynyk, Property

oled = Oliynyk()                    # not a separate package
oled.db["Si"][Property.AW]          # Property is a str Enum (column key)
oled.to_csv("oled.csv")
df = oled.to_dataframe()            # shape (76, 23)
```

| Method | Returns |
|---|---|
| `list_supported_elements()` | `list[str]` (76 symbols) |
| `is_formula_supported(formula)` | `bool` |
| `get_supported_formulas(formulas)` | `(supported, unsupported)` |
| `get_property_data(Property)` | `dict[symbol, float]` |
| `get_property_data_for_formula(formula, Property)` | `dict[symbol, float]` |
| `to_dataframe()` | `pandas.DataFrame` |
| `to_csv(path)` | `str` path written |

## Exact `Property` members

`AW`, `ATOMIC_NUMBER`, `PERIOD`, `GROUP`, `MEND_NUM`, `VAL_TOTAL`,
`UNPARIED_E`, `GILMAN`, `Z_EFF`, `ION_ENERGY`, `COORD_NUM`,
`RATIO_CLOSEST`, `POLYHEDRON_DISTORT`, `CIF_RADIUS`,
`PAULING_RADIUS_CN12`, `PAULING_EN`, `MARTYNOV_BATSANOV_EN`,
`MELTING_POINT_K`, `DENSITY`, `SPECIFIC_HEAT`, `COHESIVE_ENERGY`,
`BULK_MODULUS`.

Use **`UNPARIED_E`** (as shipped). Column for `VAL_TOTAL` is
**`valencee_total`**.

**What each property means** (definitions + ML context from the dataset
paper’s Table 1): see the full table on the
[OLED tutorial](../tutorials/oled) and the short list in the
[API quick reference](quick-reference). Parent 98-feature Excel:
[Mendeley Data bt6gv5z6yv](https://data.mendeley.com/datasets/bt6gv5z6yv).

## Formula → ML feature vector

```python
from cifkit.parsers.formula import Formula
from cifkit.sources.oliynyk import Oliynyk, Property

oled = Oliynyk()
parsed = Formula("NdSi2").parsed_formula
total = sum(c for _, c in parsed)
features = {
    prop.value: sum(oled.db[el][prop] * c for el, c in parsed) / total
    for prop in Property
}
```

**Tutorial (full table + CSV):** [OLED](../tutorials/oled)  
**Calibrated tables:** [API quick reference](quick-reference)  
**LLM recipes:** [llms.txt](../llms.txt)  
**Dataset paper:** https://doi.org/10.1016/j.dib.2024.110178

## Oliynyk

```{eval-rst}
.. autoclass:: cifkit.sources.oliynyk.Oliynyk
   :members:
   :show-inheritance:
```

## Property

```{eval-rst}
.. autoclass:: cifkit.sources.oliynyk.Property
   :members:
   :undoc-members:
   :show-inheritance:
```
