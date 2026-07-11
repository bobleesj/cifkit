# API quick reference

Calibrated import paths, attribute types, and method names for agents and
humans. Prefer this page + [llms.txt](../llms.txt) for copy-paste; use the
class pages for full autodoc.

**Package:** `cifkit` · **pip:** `pip install cifkit`  
**Docs:** https://bobleesj.github.io/cifkit/  
**LLM recipes:** https://bobleesj.github.io/cifkit/llms.txt

## Imports (canonical)

```python
from cifkit import Cif, CifEnsemble, Example
from cifkit.sources.oliynyk import Oliynyk, Property  # OLED
from cifkit.parsers.formula import Formula
from cifkit.sorters.element_sorter import ElementSorter
```

**OLED** = **O**liynyk **E**lemental **D**ata. Load only via
`cifkit.sources.oliynyk.Oliynyk`. Not a separate package.

## `Example` — demo data paths

```python
from cifkit import Example

Example.GdSb_file_path       # str path to packaged GdSb.cif
Example.demo_cif_folder_path # str path to folder with GdSb.cif + HoSb.cif
```

## `Cif` — one `.cif` file

```python
cif = Cif(
    file_path,           # str, required
    is_formatted=False,  # if False, preprocess for gemmi
    logging_enabled=False,
    supercell_size=3,    # 3 → ±1 shifts (3×3×3)
    compute_CN=False,    # True runs coordination at init
)
```

### Parsed structure attributes

| Attribute | Type (typical) | Meaning |
|---|---|---|
| `file_path` | `str` | Path given to the constructor |
| `file_name` | `str` | Basename, e.g. `'GdSb.cif'` |
| `formula` | `str` | e.g. `'GdSb'` |
| `structure` | `str` | Structure type label, e.g. `'NaCl'` |
| `space_group_name` | `str` | e.g. `'Fm-3m'` |
| `space_group_number` | `int` | e.g. `225` |
| `unitcell_lengths` | `list[float]` | `[a, b, c]` |
| `unitcell_angles` | `list[float]` | `[α, β, γ]` **in radians** |
| `site_labels` | `list[str]` | e.g. `['Sb', 'Gd']` |
| `unique_elements` | `set[str]` | Element symbols in the file |
| `composition_type` | `int` | Number of unique elements (1 unary, 2 binary, …) |
| `tag` | `str` | Tag parsed from the CIF header line |
| `db_source` | `str` | Origin DB if known (`PCD`, `ICSD`, `MP`, `CCDC`, …) |
| `unitcell_atom_count` | `int` | Atoms in the unit cell |
| `supercell_atom_count` | `int` | Atoms in the generated supercell |
| `atom_site_info` | `dict` | Occupancy / site info from the CIF loops |

### Distance attributes (lazy: may call `compute_connections()`)

| Attribute | Type | Meaning |
|---|---|---|
| `shortest_distance` | `float` | Global shortest neighbor distance (Å) |
| `shortest_bond_pair_distance` | `dict[tuple[str,str], float]` | Shortest per element-pair, e.g. `{('Gd','Sb'): 3.105}` |
| `shortest_site_pair_distance` | `dict[str, tuple[str,float]]` | Per site label: nearest neighbor label + distance |
| `connections` | `dict[str, list[tuple]]` | Per site: `(neighbor_label, dist, self_xyz, neighbor_xyz)` |
| `connections_flattened` | `list` | Flattened neighbor records |
| `bond_pairs` | `set[tuple[str,str]]` | Element pairs present |
| `site_label_pairs` | varies | Site-label pairing helpers |
| `*_sorted_by_mendeleev` | same shape | Mendeleev-ordered variants of pair structures |

### Mixing and radii

| Attribute | Type | Meaning |
|---|---|---|
| `site_mixing_type` | `str` | e.g. `'full_occupancy'` |
| `mixing_info_per_label_pair` | `dict` | Mixing label per site-label pair |
| `radius_values` | `dict` | Per element: CIF / refined / Pauling radii |
| `radius_sum` | varies | Pair radius sums used in CN methods |
| `is_radius_data_available` | `bool` | Whether radius tables cover the elements |

### Coordination (after `compute_CN()` or `compute_CN=True`)

CN method keys (exact strings):

- `dist_by_shortest_dist`
- `dist_by_CIF_radius_sum`
- `dist_by_CIF_radius_refined_sum`
- `dist_by_Pauling_radius_sum`

| Attribute | Type | Meaning |
|---|---|---|
| `CN_max_gap_per_site` | `dict` | Per site → per method → `{max_gap, CN}` |
| `CN_best_methods` | `dict` | Per site: chosen method + polyhedron metrics |
| `CN_connections_by_min_dist_method` | `dict` | Neighbor shell using min-dist CN |
| `CN_connections_by_best_methods` | `dict` | Neighbor shell using best-method CN |
| `CN_bond_count_by_min_dist_method` | `dict` | Bond counts per site |
| `CN_bond_fractions_by_min_dist_method` | `dict[tuple, float]` | Global bond-pair fractions |
| `CN_unique_values_by_min_dist_method` | `set[int]` | Unique CN values |
| `CN_avg_by_min_dist_method` / `CN_min_*` / `CN_max_*` | numeric | Summary stats |
| `*_by_best_methods` | same family | Parallel attributes using best-method CN |

**`CN_best_methods[site]` metric keys (exact):**
`volume_of_polyhedron`, `distance_from_avg_point_to_center`,
`number_of_vertices`, `number_of_edges`, `number_of_faces`,
`shortest_distance_to_face`, `shortest_distance_to_edge`,
`volume_of_inscribed_sphere`, `packing_efficiency`, `method_used`.

### Methods

| Method | Role |
|---|---|
| `compute_connections()` | Build neighbor lists (also triggered lazily) |
| `compute_CN()` | Run four CN methods + best-method selection |
| `plot_polyhedron(label, show_labels=True, is_displayed=False, output_dir=None)` | PyVista polyhedron PNG / interactive window |
| `get_polyhedron_labels_by_CN_min_dist_method(...)` | Coordinates/labels for min-dist shell |
| `get_polyhedron_labels_by_CN_best_methods(...)` | Coordinates/labels for best-method shell |

Full autodoc: [Cif](cif). Tutorial: [physical features](../tutorials/physical-features).

## `CifEnsemble` — folder of `.cif` files

```python
ensemble = CifEnsemble(
    cif_dir_path,          # str folder
    add_nested_files=...,  # include nested dirs if supported
    # preprocessing runs on init for database compatibility
)
```

### Overview attributes

| Attribute | Meaning |
|---|---|
| `file_paths` / `file_count` | Paths and count after preprocess |
| `unique_formulas` | Formulas present |
| `unique_structures` | Structure-type labels |
| `unique_space_group_names` / `unique_space_group_numbers` | Space groups |
| `unique_elements` | Elements across the folder |
| `unique_tags` / `unique_composition_types` / `unique_site_mixing_types` | Other uniques |
| `formula_stats` / `structure_stats` / `tag_stats` / … | Count maps |
| `minimum_distances` | Per-file shortest distances |
| `supercell_atom_counts` | Per-file supercell sizes |
| `CN_unique_values_by_min_dist_method` / `*_by_best_methods` | CN uniques |

### Filters (return path sets / collections)

Exact method names:

- `filter_by_formulas`
- `filter_by_structures`
- `filter_by_space_group_names` / `filter_by_space_group_numbers`
- `filter_by_elements_containing` / `filter_by_elements_exact_matching`
- `filter_by_tags` / `filter_by_composition_types` / `filter_by_site_mixing_types`
- `filter_by_min_distance` / `filter_by_supercell_count`
- `filter_by_CN_min_dist_method_containing` / `filter_by_CN_min_dist_method_exact_matching`
- `filter_by_CN_best_methods_containing` / `filter_by_CN_best_methods_exact_matching`

### File ops and histograms

- `copy_cif_files(paths, dest_dir)` / `move_cif_files(paths, dest_dir)`
- `generate_structure_histogram` / `generate_formula_histogram` /
  `generate_tag_histogram` / `generate_space_group_name_histogram` /
  `generate_space_group_number_histogram` / `generate_elements_histogram` /
  `generate_supercell_size_histogram` / `generate_composition_type_histogram` /
  `generate_site_mixing_type_histogram` /
  `generate_CN_by_min_dist_method_histogram` /
  `generate_CN_by_best_methods_histogram`

Full autodoc: [CifEnsemble](cif-ensemble). Tutorial: [statistics](../tutorials/statistics-many-cifs).

## OLED — `Oliynyk` + `Property`

```python
from cifkit.sources.oliynyk import Oliynyk, Property

oled = Oliynyk()
oled.elements          # list[str], length 76
oled.db                # dict[symbol, dict[property_key, float]]
oled.db["Si"][Property.AW]
```

### Methods

| Method | Role |
|---|---|
| `list_supported_elements()` | Same as `.elements` |
| `is_formula_supported(formula: str) -> bool` | All elements in OLED? |
| `get_supported_formulas(formulas) -> (supported, unsupported)` | Split lists |
| `get_property_data(property: Property) -> dict[str, float]` | One property, all elements |
| `get_property_data_for_formula(formula, property) -> dict[str, float]` | One property, elements in formula |
| `to_dataframe() -> pandas.DataFrame` | Full table `(76, 23)` |
| `to_csv(path: str) -> str` | Write CSV, return path |
| `get_oliynyk_CAF_data()` | Raw load of the nested dict (also used by `__init__`) |

### Exact `Property` enum (do not rename)

| Enum name | `.value` column key |
|---|---|
| `AW` | `atomic_weight` |
| `ATOMIC_NUMBER` | `atomic_number` |
| `PERIOD` | `period` |
| `GROUP` | `group` |
| `MEND_NUM` | `Mendeleev_number` |
| `VAL_TOTAL` | `valencee_total` |
| `UNPARIED_E` | `unpaired_electrons` |
| `GILMAN` | `Gilman` |
| `Z_EFF` | `Z_eff` |
| `ION_ENERGY` | `ionization_energy` |
| `COORD_NUM` | `coordination_number` |
| `RATIO_CLOSEST` | `ratio_closest` |
| `POLYHEDRON_DISTORT` | `polyhedron_distortion` |
| `CIF_RADIUS` | `CIF_radius` |
| `PAULING_RADIUS_CN12` | `Pauling_radius_CN12` |
| `PAULING_EN` | `Pauling_EN` |
| `MARTYNOV_BATSANOV_EN` | `Martynov_Batsanov_EN` |
| `MELTING_POINT_K` | `melting_point_K` |
| `DENSITY` | `density` |
| `SPECIFIC_HEAT` | `specific_heat` |
| `COHESIVE_ENERGY` | `cohesive_energy` |
| `BULK_MODULUS` | `bulk_modulus` |

Spelling as shipped: `UNPARIED_E` (not `UNPAIRED_E`), column
`valencee_total` (double “e”).

### What each OLED property means

Subset of the Oliynyk table (22 of ~98 features in the dataset paper).
Short definitions follow Data in Brief Table 1
(https://doi.org/10.1016/j.dib.2024.110178). Full narrative:
[OLED tutorial — What each property means](../tutorials/oled).

| Enum | Column | Meaning (short) |
|---|---|---|
| `AW` | `atomic_weight` | Isotopic-mean atomic mass |
| `ATOMIC_NUMBER` | `atomic_number` | Proton count *Z* |
| `PERIOD` | `period` | Periodic-table period (row) |
| `GROUP` | `group` | Periodic-table group (column) |
| `MEND_NUM` | `Mendeleev_number` | Similarity-based element order |
| `VAL_TOTAL` | `valencee_total` | Total valence electrons |
| `UNPARIED_E` | `unpaired_electrons` | Unpaired valence electrons |
| `GILMAN` | `Gilman` | Gilman valence-electron count |
| `Z_EFF` | `Z_eff` | Effective nuclear charge (shielded) |
| `ION_ENERGY` | `ionization_energy` | First ionization energy |
| `COORD_NUM` | `coordination_number` | Characteristic CN in this table |
| `RATIO_CLOSEST` | `ratio_closest` | Size / packing ratio descriptor |
| `POLYHEDRON_DISTORT` | `polyhedron_distortion` | Local packing distortion metric |
| `CIF_RADIUS` | `CIF_radius` | Radius for CIF-radius normalization (Å) |
| `PAULING_RADIUS_CN12` | `Pauling_radius_CN12` | Pauling metallic radius (CN12) |
| `PAULING_EN` | `Pauling_EN` | Pauling electronegativity |
| `MARTYNOV_BATSANOV_EN` | `Martynov_Batsanov_EN` | Martynov–Batsanov electronegativity |
| `MELTING_POINT_K` | `melting_point_K` | Melting point (K) |
| `DENSITY` | `density` | Bulk density |
| `SPECIFIC_HEAT` | `specific_heat` | Specific heat capacity |
| `COHESIVE_ENERGY` | `cohesive_energy` | Solid → free-atom energy |
| `BULK_MODULUS` | `bulk_modulus` | Resistance to compression |

### Formula → feature vector (ML)

```python
from cifkit.parsers.formula import Formula
from cifkit.sources.oliynyk import Oliynyk, Property

oled = Oliynyk()
parsed = Formula("NdSi2").parsed_formula  # [('Nd', 1.0), ('Si', 2.0)]
total = sum(c for _, c in parsed)
features = {
    prop.value: sum(oled.db[el][prop] * c for el, c in parsed) / total
    for prop in Property
}
```

Tutorial: [OLED](../tutorials/oled). Autodoc: [Oliynyk](oliynyk).

## `Formula`

```python
from cifkit.parsers.formula import Formula

f = Formula("NdSi2")
f.formula                 # str
f.elements                # ['Nd', 'Si']
f.parsed_formula          # [('Nd', 1.0), ('Si', 2.0)]
f.indices                 # [1.0, 2.0]
f.element_count           # int number of element types
f.get_normalized_formula()
```

Class/static helpers include: `filter_by_elements_containing`,
`filter_by_elements_matching`, `filter_by_composition`,
`sort_by_stoichiometry`, `sort_by_elemental_property`,
`order_by_alphabetical`, `count_by_formula`, `get_unique_formulas`, …

Autodoc: [Formula](formula).

## `ElementSorter`

```python
from cifkit.sorters.element_sorter import ElementSorter

sorter = ElementSorter(...)  # see autodoc for label maps / Excel sheets
sorter.sort(elements)
```

Autodoc: [ElementSorter](element-sorter).

## Coordination submodules

Low-level helpers under `cifkit.coordination.*` (method, filter, geometry,
composition, connection, bond_distance, site_distance). Prefer the `Cif`
attributes above unless you need the functions directly.

Autodoc: [Coordination](coordination).

## Publications

- cifkit (JOSS): https://doi.org/10.21105/joss.07205  
- OLED / Oliynyk dataset (Data in Brief): https://doi.org/10.1016/j.dib.2024.110178  
