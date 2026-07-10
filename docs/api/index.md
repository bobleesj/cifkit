# API reference

Complete reference for the two primary classes, the coordination
machinery, and the elemental-data modules. The class pages are
generated directly from the source docstrings by autodoc, so they never
drift from the code.

## At a glance

| Page | Import | Use it for |
|---|---|---|
| [Cif](cif) | `from cifkit import Cif` | One `.cif` file: parsed properties, supercell, distances, mixing, CN |
| [CifEnsemble](cif-ensemble) | `from cifkit import CifEnsemble` | A folder of `.cif` files: unique attributes, filters, move/copy, histograms |
| [Coordination](coordination) | `cifkit.coordination.*` | CN determination methods and polyhedron geometry math |
| [Oliynyk](oliynyk) | `from cifkit.sources.oliynyk import Oliynyk, Property` | Elemental property database (22 properties, 76 elements) |
| [Formula](formula) | `from cifkit.parsers.formula import Formula` | Parse, normalize, sort, and filter chemical formulas |
| [ElementSorter](element-sorter) | `from cifkit.sorters.element_sorter import ElementSorter` | Sort elements by custom labels, Mendeleev number, or alphabetically |
| [Sources](sources) | `cifkit.sources.*`, `cifkit.data.element` | Raw Mendeleev numbers, periodic table data, radii, `Element` enum |

The package root re-exports the everyday names:

```python
from cifkit import Cif, CifEnsemble, Example
```

`Example` provides the packaged demo data paths used throughout the
tutorials: `Example.GdSb_file_path` (one rock-salt CIF) and
`Example.demo_cif_folder_path` (a folder with GdSb.cif and HoSb.cif).
