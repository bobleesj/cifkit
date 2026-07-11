# API reference

Agent-oriented entry points (no interactive UI required):

| Resource | URL path |
|---|---|
| **LLM recipes (plain text)** | [llms.txt](../llms.txt) |
| **Calibrated API tables** | [API quick reference](quick-reference) |
| Human tutorials | [physical features](../tutorials/physical-features) · [statistics](../tutorials/statistics-many-cifs) · [OLED](../tutorials/oled) |

## Imports

```python
from cifkit import Cif, CifEnsemble, Example
from cifkit.sources.oliynyk import Oliynyk, Property  # OLED
from cifkit.parsers.formula import Formula
from cifkit.sorters.element_sorter import ElementSorter
```

**OLED** = Oliynyk elemental data (composition / ML). Not a separate
package. Demo paths: `Example.GdSb_file_path`,
`Example.demo_cif_folder_path`.

## Pages

| Page | Import | Use it for |
|---|---|---|
| [Quick reference](quick-reference) | — | Full attribute/method tables for agents |
| [Cif](cif) | `from cifkit import Cif` | One `.cif`: parse, distances, CN, polyhedra |
| [CifEnsemble](cif-ensemble) | `from cifkit import CifEnsemble` | Folder: stats, filters, histograms |
| [Coordination](coordination) | `cifkit.coordination.*` | Low-level CN / geometry helpers |
| [Oliynyk / OLED](oliynyk) | `from cifkit.sources.oliynyk import Oliynyk, Property` | Elemental property database |
| [Formula](formula) | `from cifkit.parsers.formula import Formula` | Parse / normalize formulas |
| [ElementSorter](element-sorter) | `from cifkit.sorters.element_sorter import ElementSorter` | Sort elements by role / Mendeleev |
| [Sources](sources) | `cifkit.sources.*` | Mendeleev numbers, ptable, radii |

## Naming rules for generated code

1. Use exact `Property` enum names (`UNPARIED_E`, not `UNPAIRED_E`).
2. `unitcell_angles` are **radians**.
3. Call `compute_CN()` before `CN_*` attributes unless `compute_CN=True`.
4. Do not invent top-level `import oled` / `import oliynyk`.
