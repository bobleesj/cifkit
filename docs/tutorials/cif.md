# Cif

`Cif` is initialized with a `.cif` file path. It parses the file,
generates a supercell, and computes nearest neighbors on demand. This
page walks through the packaged GdSb example so every snippet runs
offline; all outputs below are real outputs from cifkit 1.2.1.

## Load the packaged example

`cifkit` ships example CIF files under `cifkit.data.example.Example` so
you can try the API without hunting for data:

```python
from cifkit import Cif, Example

cif = Cif(Example.GdSb_file_path)
print(cif.file_name)
```

```text
GdSb.cif
```

By default the constructor preprocesses the file for compatibility with
the gemmi parser (pass `is_formatted=True` to skip), builds a 3x3x3
supercell (`supercell_size=3`), and defers coordination-number work
until you ask for it (`compute_CN=False`).

## Parsed properties

The heavily used attributes are plain Python values:

```python
print("formula:", cif.formula)
print("structure:", cif.structure)
print("space_group_name:", cif.space_group_name)
print("space_group_number:", cif.space_group_number)
print("unitcell_lengths:", cif.unitcell_lengths)
print("unitcell_angles:", cif.unitcell_angles)
print("site_labels:", cif.site_labels)
print("unique_elements:", cif.unique_elements)
print("composition_type:", cif.composition_type)
print("tag:", cif.tag)
print("db_source:", cif.db_source)
```

```text
formula: GdSb
structure: NaCl
space_group_name: Fm-3m
space_group_number: 225
unitcell_lengths: [6.21, 6.21, 6.21]
unitcell_angles: [1.5708, 1.5708, 1.5708]
site_labels: ['Sb', 'Gd']
unique_elements: {'Sb', 'Gd'}
composition_type: 2
tag: rt
db_source: PCD
```

Unit cell angles are reported in radians. `composition_type` is the
number of unique elements (1 unary, 2 binary, 3 ternary, ...), and
`db_source` identifies the origin database (PCD, ICSD, MP, CCDC).

## Supercell and atom counts

```python
print("unitcell_atom_count:", cif.unitcell_atom_count)
print("supercell_atom_count:", cif.supercell_atom_count)
```

```text
unitcell_atom_count: 8
supercell_atom_count: 1000
```

## Distances

Nearest-neighbor connections are computed lazily on first access, so
the first distance property takes a moment while the supercell is
searched:

```python
print("shortest_distance:", cif.shortest_distance)
print("shortest_bond_pair_distance:", cif.shortest_bond_pair_distance)
print("shortest_site_pair_distance:", cif.shortest_site_pair_distance)
```

```text
shortest_distance: 3.105
shortest_bond_pair_distance: {('Gd', 'Sb'): 3.105, ('Gd', 'Gd'): 4.391, ('Sb', 'Sb'): 4.391}
shortest_site_pair_distance: {'Sb': ('Gd', 3.105), 'Gd': ('Sb', 3.105)}
```

## Atomic mixing

`cifkit` classifies every site and bond pair into one of four occupancy
categories: `full_occupancy`, `full_occupancy_atomic_mixing`,
`deficiency_without_atomic_mixing`, and `deficiency_atomic_mixing`.

```python
print("site_mixing_type:", cif.site_mixing_type)
print("mixing_info_per_label_pair:", cif.mixing_info_per_label_pair)
```

```text
site_mixing_type: full_occupancy
mixing_info_per_label_pair: {('Gd', 'Sb'): 'full_occupancy', ('Gd', 'Gd'): 'full_occupancy', ('Sb', 'Sb'): 'full_occupancy'}
```

## Radii

Pauling and CIF radii (with refined values optimized against the
shortest observed distances) are available per element:

```python
print(cif.radius_values)
```

```text
{'Sb': {'CIF_radius': 1.434, 'CIF_radius_refined': 1.389, 'Pauling_radius_CN12': 1.59}, 'Gd': {'CIF_radius': 1.787, 'CIF_radius_refined': 1.716, 'Pauling_radius_CN12': 1.795}}
```

## Next steps

Coordination numbers and polyhedron rendering are covered in the
[Coordination tutorial](coordination); processing a whole folder at
once is covered in the [CifEnsemble tutorial](cif_ensemble). Every
attribute and method is documented in the [Cif API reference](../api/cif).
