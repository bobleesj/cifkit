# Statistics over many CIFs

When you have a **folder** of `.cif` files, use `CifEnsemble` to get
overview statistics, filter by attributes, generate histograms, and
copy/move files. This is separate from extracting physical features from
one file — see [Parse physical features from a .cif](physical-features) for
that (including **how each CN method is determined**).

Elemental composition features are **not** from these CIFs — use
[OLED](oled) (*Data in Brief* table).

## Set up a scratch folder

Preprocessing can rewrite ill-formatted files in place, and
`move_cif_files` relocates them, so work on a copy:

```python
import os
import shutil

from cifkit import CifEnsemble, Example

scratch = "demo_cifs"
os.makedirs(scratch, exist_ok=True)
for name in os.listdir(Example.demo_cif_folder_path):
    if name.endswith(".cif"):
        shutil.copy(os.path.join(Example.demo_cif_folder_path, name), scratch)

ensemble = CifEnsemble(scratch)
```

```text
CIF Preprocessing in demo_cifs begun...

Preprocessing demo_cifs/GdSb.cif (1/2)
Preprocessing demo_cifs/HoSb.cif (2/2)

SUMMARY
# of files moved to 'error_*' folders: 0 (all clean)

Initializing 2 Cif objects...
Finished initialization!
```

Ill-formatted database files are sorted into `error_*` folders during
this pass.

## Unique attributes and counts

```python
import pandas as pd

print("file_count:", ensemble.file_count)
print("unique_formulas:", ensemble.unique_formulas)
print("unique_structures:", ensemble.unique_structures)
print("unique_space_group_names:", ensemble.unique_space_group_names)
print("unique_elements:", ensemble.unique_elements)
```

As a small overview table:

```python
overview = pd.DataFrame(
    [
        ("file_count", ensemble.file_count),
        ("unique_formulas", sorted(ensemble.unique_formulas)),
        ("unique_structures", sorted(ensemble.unique_structures)),
        ("unique_space_group_names", sorted(ensemble.unique_space_group_names)),
        ("unique_elements", sorted(ensemble.unique_elements)),
    ],
    columns=["stat", "value"],
)
print(overview.to_string(index=False))
```

| stat | value |
|---|---|
| file_count | 2 |
| unique_formulas | ['GdSb', 'HoSb'] |
| unique_structures | ['NaCl'] |
| unique_space_group_names | ['Fm-3m'] |
| unique_elements | ['Gd', 'Ho', 'Sb'] |

Per-file values and formula counts are also available (e.g.
`formula_stats`, `minimum_distances`, `supercell_atom_counts` — see the
[CifEnsemble API](../api/cif-ensemble)).

## Filter file paths

```python
print(ensemble.filter_by_formulas(["GdSb"]))
print(ensemble.filter_by_elements(["Ho"]))
print(ensemble.filter_by_space_group_names(["Fm-3m"]))
```

```text
{'demo_cifs/GdSb.cif'}
{'demo_cifs/HoSb.cif'}
{'demo_cifs/GdSb.cif', 'demo_cifs/HoSb.cif'}
```

Other filters include structure, space-group number, composition type,
site-mixing type, CN ranges, min distance, and supercell size.

## Move and copy by filter

```python
ensemble.copy_cif_files(ensemble.filter_by_formulas(["GdSb"]), "sorted_GdSb")
print(os.listdir("sorted_GdSb"))
```

```text
['GdSb.cif']
```

## Histograms

```python
ensemble.generate_structure_histogram(output_dir="histograms")
print(os.listdir("histograms"))
```

```text
['structures.png']
```

Available histograms: structure, formula, tag, space group number and
name, supercell size, elements, CN by both method families, composition
type, and site mixing type.

Example structure-type histogram from a larger ensemble:

```{figure} ../img/histogram-structure.png
:alt: Structures distribution histogram from CifEnsemble
:align: center

**Structure histogram.** Counts of structure types via
`generate_structure_histogram`.
```

JOSS Figure 1 pairs a single-file polyhedron with an ensemble CN
histogram:

```{figure} ../img/ErCoIn-histogram-combined.png
:alt: JOSS Figure 1 polyhedron and CN histogram
:align: center

**Figure 1 (JOSS).** One CIF’s polyhedron (left) and ensemble CN
distribution (right).
```

## Scale

On the order of 10,000 `.cif` files is roughly 30–60 minutes on a
standard laptop (supercell + neighbors per file). Plan long runs
accordingly.

## API

Full method list: [CifEnsemble](../api/cif-ensemble).

## Next

- **[Parse physical features from a .cif](physical-features)** — distances, CN, polyhedra  
- **[OLED](oled)** — elemental / composition features (dataset table, not from CIF)

---

## Notes (demo data, citation)

- Outputs on this page use the packaged demo CIFs (**GdSb**, **HoSb**).
- Tables use **pandas → Markdown** where shown; they summarize
  **geometry / ensemble stats from CIFs**, not OLED elemental rows.
- Soft cite for geometry / ensemble work: **cifkit**
  ([JOSS](https://doi.org/10.21105/joss.07205)) ·
  [CITATION.txt](../_static/CITATION.txt) · [home page](../intro).
