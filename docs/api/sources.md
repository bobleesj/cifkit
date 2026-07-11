# Sources

Raw elemental data sources behind the higher-level classes, plus the
`Element` enum and quick stats helper. New in cifkit 1.2.1 (migrated
from `bobleesj.utils`). See the
[OLED tutorial](../tutorials/oled) for elemental-data context.

## Mendeleev numbers

`cifkit.sources.mendeleev.numbers` maps each element symbol to its
Mendeleev number (e.g. `numbers["Fe"] == 55`), the ordering used by all
`_sorted_by_mendeleev` properties in `Cif`.

```{eval-rst}
.. automodule:: cifkit.sources.mendeleev
   :members:
```

## Periodic table

```{eval-rst}
.. automodule:: cifkit.sources.ptable
   :members:
```

## Radii

```{eval-rst}
.. automodule:: cifkit.sources.radius
   :members:
```

## Element enum

All 118 elements, symbol to full name:

```python
from cifkit.data.element import Element

Element.Fe.symbol     # 'Fe'
Element.Fe.full_name  # 'Iron'
Element.all_symbols() # ['H', 'He', ..., 'Og']
```

```{eval-rst}
.. autoclass:: cifkit.data.element.Element
   :members: symbol, full_name, all_symbols
   :undoc-members:
   :show-inheritance:
```

## Quick stats

```{eval-rst}
.. automodule:: cifkit.numbers
   :members:
```
