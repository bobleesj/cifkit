# CifEnsemble

`CifEnsemble` is initialized with a folder path containing `.cif`
files. It identifies unique attributes (formulas, structures, space
groups, elements, ...) across the folder, filters file paths by those
attributes, moves and copies files, and generates histograms. All
outputs below are real outputs on the packaged demo CIFs (GdSb.cif and
HoSb.cif).

## Set up a scratch folder

Filtering never modifies files, but preprocessing rewrites ill-formatted
files in place and `move_cif_files` relocates them, so work on a copy of
the packaged read-only examples:

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
# of files moved to 'error_no_labels' folder: 0
# of files moved to 'error_operations' folder: 0
# of files moved to 'error_duplicate_labels' folder: 0
# of files moved to 'error_wrong_loop_value' folder: 0
# of files moved to 'error_coords' folder: 0
# of files moved to 'error_invalid_label' folder: 0
# of files moved to 'error_others' folder: 0

Initializing 2 Cif objects...
Finished initialization!
```

The preprocessing pass is the filter feature in action: files with
missing labels, broken symmetry operations, duplicate labels, wrong
loop values, or missing coordinates are moved into `error_*` subfolders
instead of crashing the run. Pass `preprocess=False` when the folder is
already clean.

## Unique attributes

```python
print("file_count:", ensemble.file_count)
print("unique_formulas:", ensemble.unique_formulas)
print("unique_structures:", ensemble.unique_structures)
print("unique_elements:", ensemble.unique_elements)
print("unique_space_group_names:", ensemble.unique_space_group_names)
print("unique_space_group_numbers:", ensemble.unique_space_group_numbers)
print("unique_composition_types:", ensemble.unique_composition_types)
print("unique_site_mixing_types:", ensemble.unique_site_mixing_types)
```

```text
file_count: 2
unique_formulas: {'GdSb', 'HoSb'}
unique_structures: {'NaCl'}
unique_elements: {'Gd', 'Sb', 'Ho'}
unique_space_group_names: {'Fm-3m'}
unique_space_group_numbers: {225}
unique_composition_types: {2}
unique_site_mixing_types: {'full_occupancy'}
```

## Stats and per-file values

Every unique attribute has a `_stats` counterpart that counts the files
per value, and per-file lists are available for distances and atom
counts:

```python
print("structure_stats:", ensemble.structure_stats)
print("formula_stats:", ensemble.formula_stats)
print("minimum_distances:", ensemble.minimum_distances)
print("supercell_atom_counts:", ensemble.supercell_atom_counts)
```

```text
structure_stats: {'NaCl': 2}
formula_stats: {'GdSb': 1, 'HoSb': 1}
minimum_distances: [('demo_cifs/GdSb.cif', 3.105), ('demo_cifs/HoSb.cif', 3.065)]
supercell_atom_counts: [('demo_cifs/GdSb.cif', 1000), ('demo_cifs/HoSb.cif', 1000)]
```

## Filter file paths by attributes

Filters return the set of matching file paths:

```python
print(ensemble.filter_by_formulas(["GdSb"]))
print(ensemble.filter_by_elements_containing(["Ho"]))
print(ensemble.filter_by_structures(["NaCl"]))
```

```text
{'demo_cifs/GdSb.cif'}
{'demo_cifs/HoSb.cif'}
{'demo_cifs/GdSb.cif', 'demo_cifs/HoSb.cif'}
```

Other filters follow the same pattern: `filter_by_space_group_names`,
`filter_by_space_group_numbers`, `filter_by_site_mixing_types`,
`filter_by_tags`, `filter_by_composition_types`,
`filter_by_elements_exact_matching`, CN-based filters, and range filters
`filter_by_min_distance(min, max)` /
`filter_by_supercell_count(min, max)`.

## Move and copy by filter result

Chain a filter into `copy_cif_files` or `move_cif_files` to sort a
database folder by attribute:

```python
ensemble.copy_cif_files(ensemble.filter_by_formulas(["GdSb"]), "sorted_GdSb")
print(os.listdir("sorted_GdSb"))
```

```text
['GdSb.cif']
```

## Histograms

Each attribute also has a `generate_*_histogram` method that saves a
matplotlib `.png` (into the ensemble folder by default, or
`output_dir`):

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

## Scale expectations

Processing roughly 10,000 `.cif` files takes about 30 to 60 minutes on
a standard laptop (M1 iMac class), because each file builds a supercell
and computes nearest neighbors. Plan long runs accordingly.

Every method is documented in the
[CifEnsemble API reference](../api/cif-ensemble).
