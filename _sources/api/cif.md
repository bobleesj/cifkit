# Cif

One `.cif` file: parse structure metadata, interatomic distances,
coordination numbers (four methods), polyhedron metrics, bond fractions,
site mixing, and polyhedron plots.

```python
from cifkit import Cif, Example

cif = Cif(Example.GdSb_file_path)           # or Cif("/path/to/file.cif")
cif = Cif(path, supercell_size=3, compute_CN=False, is_formatted=False)
```

| Parameter | Default | Role |
|---|---|---|
| `file_path` | required | Path to the `.cif` |
| `is_formatted` | `False` | If `False`, preprocess for gemmi compatibility |
| `logging_enabled` | `False` | Verbose logging |
| `supercell_size` | `3` | `3` → ±1 shifts (3×3×3 supercell) |
| `compute_CN` | `False` | If `True`, run coordination at init |

**Calibrated attribute / method tables:** [API quick reference](quick-reference).  
**Tutorial:** [Parse physical features from a .cif](../tutorials/physical-features).  
**LLM recipes:** [llms.txt](../llms.txt).

## Common attributes (GdSb demo types)

| Name | Type | Example / notes |
|---|---|---|
| `formula` | `str` | `'GdSb'` |
| `structure` | `str` | `'NaCl'` |
| `space_group_name` | `str` | `'Fm-3m'` |
| `space_group_number` | `int` | `225` |
| `unitcell_lengths` | `list[float]` | `[6.21, 6.21, 6.21]` |
| `unitcell_angles` | `list[float]` | radians, not degrees |
| `site_labels` | `list[str]` | `['Sb', 'Gd']` |
| `shortest_distance` | `float` | Å |
| `shortest_bond_pair_distance` | `dict` | `{('Gd','Sb'): 3.105, …}` |
| `connections` | `dict` | per-site neighbor lists |
| `CN_best_methods` | `dict` | after `compute_CN()` |
| `CN_bond_fractions_by_min_dist_method` | `dict` | after `compute_CN()` |
| `site_mixing_type` | `str` | e.g. `'full_occupancy'` |

## Methods

- `compute_connections()` - neighbor search (also lazy)
- `compute_CN()` - four CN methods + best method + polyhedron metrics
- `plot_polyhedron(label, show_labels=True, is_displayed=False, output_dir=None)`
- `get_polyhedron_labels_by_CN_min_dist_method` / `…_by_CN_best_methods`

## Full autodoc

```{eval-rst}
.. autoclass:: cifkit.models.cif.Cif
   :members:
   :undoc-members:
   :show-inheritance:
```
