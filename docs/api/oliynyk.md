# Oliynyk

The Oliynyk elemental property database: 22 properties for 76 elements,
loaded from an Excel file packaged inside the wheel. New in cifkit
1.2.1 (migrated from `bobleesj.utils`). See the
[Elemental data tutorial](../tutorials/elemental_data) for worked
examples.

## Oliynyk

```{eval-rst}
.. autoclass:: cifkit.sources.oliynyk.Oliynyk
   :members:
   :show-inheritance:
```

## Property

`Property` is a `str` enum, so a member doubles as the column key of
the underlying database dict: `oliynyk.db["Si"][Property.AW]`.

```{eval-rst}
.. autoclass:: cifkit.sources.oliynyk.Property
   :members:
   :undoc-members:
   :show-inheritance:
```
