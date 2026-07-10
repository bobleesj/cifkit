# cifkit

[![PyPI](https://img.shields.io/pypi/v/cifkit)](https://pypi.org/project/cifkit/)
[![Conda](https://img.shields.io/conda/vn/conda-forge/cifkit)](https://anaconda.org/conda-forge/cifkit)
[![Python](https://img.shields.io/pypi/pyversions/cifkit)](https://pypi.org/project/cifkit/)
[![CI](https://github.com/bobleesj/cifkit/actions/workflows/matrix-and-codecov-on-merge-to-main.yml/badge.svg)](https://github.com/bobleesj/cifkit/actions/workflows/matrix-and-codecov-on-merge-to-main.yml)
[![Codecov](https://codecov.io/gh/bobleesj/cifkit/branch/main/graph/badge.svg)](https://codecov.io/gh/bobleesj/cifkit)
[![DOI](https://img.shields.io/badge/DOI-10.21105%2Fjoss.07205-blue)](https://doi.org/10.21105/joss.07205)

A Python package for coordination geometry and atomic site analysis of
CIF (Crystallographic Information File) files, plus - new in 1.2.1 - a
built-in elemental property toolkit.

```python
from cifkit import Cif, CifEnsemble, Example
```

`cifkit` offers higher-level functions and variables that let
solid-state synthesists obtain intuitive, measurable properties in a few
lines of code. It visualizes coordination geometry from each atomic site
using four coordination determination methods and extracts physics-based
features like polyhedron volume and packing efficiency - crucial for
structural analysis in machine learning tasks. It also extracts atomic
mixing information at the bond-pair level, tasks that would otherwise
require extensive manual effort with GUI-based tools like VESTA,
Diamond, and CrystalMaker.

## Quick start

`cifkit` ships example CIF files so the first run needs no downloads:

```python
from cifkit import Cif, Example

cif = Cif(Example.GdSb_file_path)
print(cif.formula, cif.structure, cif.space_group_name)
```

```text
GdSb NaCl Fm-3m
```

## What is in the box

| Area | Use it for | Tutorial · API |
|---|---|---|
| `Cif` | One `.cif` file: parsed properties, supercell, distances, atomic mixing | [tutorial](tutorials/cif) · [API](api/cif) |
| `CifEnsemble` | A folder of `.cif` files: unique attributes, filters, move/copy, histograms | [tutorial](tutorials/cif_ensemble) · [API](api/cif-ensemble) |
| Coordination | CN by four methods, polyhedron metrics and rendering | [tutorial](tutorials/coordination) · [API](api/coordination) |
| `Oliynyk` | Excel-backed elemental property database (22 properties per element) | [tutorial](tutorials/elemental_data) · [API](api/oliynyk) |
| `Formula` | Parse, normalize, sort, and filter chemical formulas | [tutorial](tutorials/elemental_data) · [API](api/formula) |
| `ElementSorter` | Sort elements by custom labels, Mendeleev number, or alphabetically | [tutorial](tutorials/elemental_data) · [API](api/element-sorter) |
| Sources | Mendeleev numbers, periodic table data, CIF/Pauling radii | [tutorial](tutorials/elemental_data) · [API](api/sources) |

The elemental data rows are new in **cifkit 1.2.1**: the `Oliynyk`
database, `Formula` parser, `ElementSorter`, and the raw
mendeleev/ptable/radius sources migrated here from the retired
`bobleesj.utils` package, so one install now covers both CIF geometry
and elemental features.

## Highlights

- **Coordination geometry** - functions for visualizing coordination
  geometry from each site, with physics-based features like volume and
  packing efficiency of each polyhedron.
- **Atomic mixing** - atomic mixing information at the bond-pair level,
  categorized into four types (full occupancy, full occupancy with
  mixing, deficiency without mixing, deficiency with mixing).
- **Filter** - systematic preprocessing of common issues in database CIF
  files, such as incorrect loop values and missing fractional
  coordinates, including relabeling sites like `M1` to `Fe1` in files
  with atomic mixing.
- **Sort** - copy, move, and sort `.cif` files by coordination numbers,
  space groups, unit cells, shortest distances, elements, and more.
- **Elemental data** - a curated elemental property database and formula
  tooling for featurization, no extra package required.

## Citation

If you use `cifkit` in your scientific publication, please cite:

- *cifkit: A Python package for coordination geometry and atomic site
  analysis*, [https://doi.org/10.21105/joss.07205](https://doi.org/10.21105/joss.07205)

## Research software using cifkit

- [CIF Bond Analyzer (CBA)](https://github.com/bobleesj/cif-bond-analyzer)
- [Structure Analysis/Featurizer (SAF)](https://github.com/bobleesj/structure-analyzer-featurizer)
- [CIF Cleaner](https://github.com/bobleesj/cif-cleaner)

## Getting help

- **Questions or bugs:** open an issue at
  [github.com/bobleesj/cifkit/issues](https://github.com/bobleesj/cifkit/issues).
- **Maintained by** Sangjoon (Bob) Lee
  ([@bobleesj](https://github.com/bobleesj)) with contributions from
  Anton Oliynyk, Balaranjan Selvaratnam, Danila Shiryaev, and the wider
  community. Contributions and feedback are welcome via pull request or
  issue.

See [Installation](install) to get started.
