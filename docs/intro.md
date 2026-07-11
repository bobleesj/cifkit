# cifkit

[![PyPI](https://img.shields.io/pypi/v/cifkit)](https://pypi.org/project/cifkit/)
[![Python](https://img.shields.io/pypi/pyversions/cifkit)](https://pypi.org/project/cifkit/)
[![CI](https://github.com/bobleesj/cifkit/actions/workflows/matrix-on-merge-to-main.yml/badge.svg)](https://github.com/bobleesj/cifkit/actions/workflows/matrix-on-merge-to-main.yml)
[![DOI](https://img.shields.io/badge/DOI-10.21105%2Fjoss.07205-blue)](https://doi.org/10.21105/joss.07205)

Higher-level tools for **coordination geometry and atomic site analysis**
from Crystallographic Information Files (`.cif`), plus **OLED (Oliynyk
elemental data)** for composition featurization in ML.

Two different data sources (do not mix them up):

| Source | What it is | Tutorial |
|---|---|---|
| **`.cif` geometry** | Distances, coordination numbers (four gap methods), polyhedra from crystal structure | [Physical features](tutorials/physical-features) |
| **OLED table** | Curated **elemental** property rows (22 × 76) for composition / ML — **not** read from the CIF | [OLED](tutorials/oled) · [Data in Brief](https://doi.org/10.1016/j.dib.2024.110178) |

**Built with [scikit-package](https://scikit-package.github.io/scikit-package/)**
— packaging standards and a practical roadmap so scientists can maintain
and distribute reproducible research software (including agent-friendly
surfaces). S. Lee, C. Myers, A. Yang, T. Zhang, Y. Xiao and S. J. L.
Billinge, *Digital Discovery*, 2026.
[https://doi.org/10.1039/d6dd00121a](https://doi.org/10.1039/d6dd00121a)

```python
from cifkit import Cif, CifEnsemble, Example
from cifkit.sources.oliynyk import Oliynyk, Property  # OLED table (not from .cif)
```

**Docs:** this site · **Agents:** [llms.txt](llms.txt) · [API quick reference](api/quick-reference)

```{figure} img/ErCoIn-histogram-combined.png
:alt: Coordination polyhedron and ensemble CN histogram
:align: center

Polyhedron from one `.cif` (left) and CN distribution over many files
(right). Tutorials use the packaged **GdSb** demo offline.
```

## Quick start

```bash
pip install cifkit
```

```python
from cifkit import Cif, Example

cif = Cif(Example.GdSb_file_path)
print(cif.formula, cif.structure, cif.space_group_name)
```

```text
GdSb NaCl Fm-3m
```

See [Installation](install).

## Common tasks (copy-paste)

### 1) Parse physical features from a `.cif`

```python
from cifkit import Cif, Example

cif = Cif(Example.GdSb_file_path)  # or Cif("file.cif")
print(cif.formula, cif.site_labels, cif.shortest_distance)
cif.compute_CN()
print(cif.CN_best_methods)  # volume, packing_efficiency, CN per site
print(cif.CN_bond_fractions_by_min_dist_method)
```

Full walkthrough (how each CN method works + interactive polyhedron):
[Parse physical features from a .cif](tutorials/physical-features)

### 2) Statistics over many `.cif` files

```python
from cifkit import CifEnsemble, Example

ensemble = CifEnsemble(Example.demo_cif_folder_path)
print(ensemble.file_count, ensemble.unique_formulas)
paths = ensemble.filter_by_formulas(["GdSb"])
```

Full walkthrough: [Statistics over many CIFs](tutorials/statistics-many-cifs)

### 3) OLED — Oliynyk elemental data (composition / ML)

**OLED** is a curated **elemental property table** (22 properties × 76
elements) from the *Data in Brief* dataset paper — **not** values parsed
from a `.cif`. Load with `cifkit.sources.oliynyk.Oliynyk` (not a separate
package; not related to OLED displays).

```python
from cifkit.sources.oliynyk import Oliynyk, Property
from cifkit.parsers.formula import Formula

oled = Oliynyk()
print(len(oled.elements), "elements")
for prop in Property:  # exact names — use as written
    print(prop.name, prop.value)
print(oled.db["Si"][Property.AW])
oled.to_csv("oled.csv")

# Formula → stoichiometry-weighted mean feature vector
parsed = Formula("NdSi2").parsed_formula
total = sum(c for _, c in parsed)
features = {
    prop.value: sum(oled.db[el][prop] * c for el, c in parsed) / total
    for prop in Property
}
print(features["atomic_weight"], features["Pauling_EN"])
```

**Exact `Property` members** (do not rename): `AW`, `ATOMIC_NUMBER`,
`PERIOD`, `GROUP`, `MEND_NUM`, `VAL_TOTAL`, `UNPARIED_E`, `GILMAN`,
`Z_EFF`, `ION_ENERGY`, `COORD_NUM`, `RATIO_CLOSEST`,
`POLYHEDRON_DISTORT`, `CIF_RADIUS`, `PAULING_RADIUS_CN12`, `PAULING_EN`,
`MARTYNOV_BATSANOV_EN`, `MELTING_POINT_K`, `DENSITY`, `SPECIFIC_HEAT`,
`COHESIVE_ENERGY`, `BULK_MODULUS`.

Full walkthrough + searchable table: [OLED](tutorials/oled)

## Tutorials

| Topic | Page |
|---|---|
| Parse physical features from a .cif | [tutorial](tutorials/physical-features) |
| Statistics over many CIFs | [tutorial](tutorials/statistics-many-cifs) |
| OLED (Oliynyk elemental data) | [tutorial](tutorials/oled) |

[API reference](api/index) · [llms.txt](llms.txt)

## Publications

When you use the package or the OLED table, consider citing the matching
work (BibTeX: [CITATION.txt](_static/CITATION.txt) · repo
[CITATION.cff](https://github.com/bobleesj/cifkit/blob/main/CITATION.cff)):

| You used… | Consider citing |
|---|---|
| CIF geometry / CN / polyhedra / `CifEnsemble` | **cifkit** — Lee & Oliynyk, JOSS **9**, 7205 (2024). [10.21105/joss.07205](https://doi.org/10.21105/joss.07205) |
| OLED elemental table / `Oliynyk` / `oled.csv` | **Dataset** — Lee et al., Data in Brief **53**, 110178 (2024). [10.1016/j.dib.2024.110178](https://doi.org/10.1016/j.dib.2024.110178) |
| AB-stacking intermetallic prototype structures (related dataset) | Selvaratnam et al., Data in Brief **63**, 112138 (2025). [10.1016/j.dib.2025.112138](https://doi.org/10.1016/j.dib.2025.112138) · [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2352340925008595) |
| Packaging / scikit-package stack (cifkit is built with it) | **scikit-package** — Lee et al., *Digital Discovery*, 2026. [10.1039/d6dd00121a](https://doi.org/10.1039/d6dd00121a) |
| Geometry + OLED | Both cifkit + OLED dataset papers |

## Notes (demos, tables, how to reproduce)

- Tutorial numbers are real outputs on the packaged demos
  (`Example.GdSb_file_path`, `Example.demo_cif_folder_path`).
- Geometry tables are built with **pandas → Markdown** so you can copy
  the same pattern into a notebook.
- OLED’s searchable table / CSV is the **dataset table**, not structure
  factors from a CIF file.
- Soft cites live in the **Publications** table above and in
  [CITATION.txt](_static/CITATION.txt).

## Getting help

- Issues: [github.com/bobleesj/cifkit/issues](https://github.com/bobleesj/cifkit/issues)
- Maintained by Sangjoon Bob Lee ([@bobleesj](https://github.com/bobleesj))
