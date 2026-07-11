# Coordination

Low-level coordination helpers behind `Cif.compute_CN()`. Prefer the
`Cif` attributes (`CN_max_gap_per_site`, `CN_best_methods`, …) unless you
need these functions directly.

**CN method keys (exact):** `dist_by_shortest_dist`,
`dist_by_CIF_radius_sum`, `dist_by_CIF_radius_refined_sum`,
`dist_by_Pauling_radius_sum`.

[Quick reference](quick-reference) ·
[Physical features tutorial](../tutorials/physical-features) ·
[llms.txt](../llms.txt)

## CN determination methods

```{eval-rst}
.. automodule:: cifkit.coordination.method
   :members:
```

## Best-method selection

```{eval-rst}
.. automodule:: cifkit.coordination.filter
   :members:
```

## Polyhedron geometry

```{eval-rst}
.. automodule:: cifkit.coordination.geometry
   :members:
```

## Bond composition

```{eval-rst}
.. automodule:: cifkit.coordination.composition
   :members:
```

## Connections and sites

```{eval-rst}
.. automodule:: cifkit.coordination.connection
   :members:

.. automodule:: cifkit.coordination.site
   :members:

.. automodule:: cifkit.coordination.site_distance
   :members:

.. automodule:: cifkit.coordination.bond_distance
   :members:
```
