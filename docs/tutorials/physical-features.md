# Parse physical features from a .cif

This is the main use of `cifkit`: turn one crystallographic `.cif` file
into **physical numbers** you can plot, compare, or feed into a
featurizer / machine-learning model (geometry and site environment).

What you get, in order:

1. Useful structure facts (parse)
2. **Interatomic distances**
3. **Coordination numbers** (four methods)
4. **Polyhedron metrics** (volume, packing efficiency, …)
5. Bond fractions and site mixing
6. Optional polyhedron plot

For **composition / elemental** descriptors (atomic weight,
electronegativity, Mendeleev number, …) use **[OLED](oled)** — that is a
separate table, not read from the `.cif` (dataset paper:
[Data in Brief](https://doi.org/10.1016/j.dib.2024.110178)).

All numbers below are real outputs on the packaged **GdSb** demo
(`Example.GdSb_file_path`). Tables use **pandas → Markdown** so you can
copy the same pattern into a notebook.

If these geometry features were useful, consider citing **cifkit**
([JOSS 10.21105/joss.07205](https://doi.org/10.21105/joss.07205);
BibTeX in [CITATION.txt](../_static/CITATION.txt)).

```{figure} ../img/GdSb_Sb.png
:alt: GdSb Sb-centered coordination polyhedron, CN=6
:align: center
:width: 55%

**Example feature visualization.** Sb-centered polyhedron in GdSb
(CN=6) from `plot_polyhedron` — same demo file used throughout this
page.
```

## 1. Load a CIF and see what was parsed

```python
import pandas as pd
from cifkit import Cif, Example

cif = Cif(Example.GdSb_file_path)

props = pd.DataFrame(
    [
        ("file_name", cif.file_name),
        ("formula", cif.formula),
        ("structure", cif.structure),
        ("space_group_name", cif.space_group_name),
        ("space_group_number", cif.space_group_number),
        ("unitcell_lengths", cif.unitcell_lengths),
        ("unitcell_angles (rad)", cif.unitcell_angles),
        ("site_labels", cif.site_labels),
        ("unique_elements", sorted(cif.unique_elements)),
        ("composition_type", cif.composition_type),
        ("tag", cif.tag),
        ("db_source", cif.db_source),
        ("unitcell_atom_count", cif.unitcell_atom_count),
        ("supercell_atom_count", cif.supercell_atom_count),
    ],
    columns=["attribute", "value"],
)
print(props.to_string(index=False))
```

| attribute | value |
|---|---|
| file_name | GdSb.cif |
| formula | GdSb |
| structure | NaCl |
| space_group_name | Fm-3m |
| space_group_number | 225 |
| unitcell_lengths | [6.21, 6.21, 6.21] |
| unitcell_angles (rad) | [1.5708, 1.5708, 1.5708] |
| site_labels | ['Sb', 'Gd'] |
| unique_elements | ['Gd', 'Sb'] |
| composition_type | 2 |
| tag | rt |
| db_source | PCD |
| unitcell_atom_count | 8 |
| supercell_atom_count | 1000 |

By default the constructor preprocesses for gemmi compatibility, builds
a 3×3×3 supercell, and defers coordination work until you ask
(`compute_CN=False`).

## 2. Interatomic distances

Distances come from the supercell neighbor search — **before**
coordination methods run.

```python
print("shortest_distance:", cif.shortest_distance)
print("shortest_site_pair_distance:", cif.shortest_site_pair_distance)
print("shortest_bond_pair_distance:", cif.shortest_bond_pair_distance)
```

```text
shortest_distance: 3.105
shortest_site_pair_distance: {'Sb': ('Gd', 3.105), 'Gd': ('Sb', 3.105)}
shortest_bond_pair_distance: {('Gd', 'Sb'): 3.105, ('Gd', 'Gd'): 4.391, ('Sb', 'Sb'): 4.391}
```

As a table — shortest distance between each element-pair type:

```python
bond_d = pd.DataFrame(
    [
        {"pair": str(k), "shortest (Å)": v}
        for k, v in cif.shortest_bond_pair_distance.items()
    ]
)
print(bond_d.to_string(index=False))
```

| pair | shortest (Å) |
|---|---:|
| ('Gd', 'Sb') | 3.105 |
| ('Gd', 'Gd') | 4.391 |
| ('Sb', 'Sb') | 4.391 |

Unique neighbor distances from site **Gd** (first shell and beyond):

```python
seen = set()
rows = []
for label, dist, *_ in cif.connections["Gd"]:
    key = (label, round(dist, 4))
    if key in seen:
        continue
    seen.add(key)
    rows.append({"neighbor": label, "distance (Å)": round(dist, 4)})
dist_table = pd.DataFrame(rows)
print(dist_table.head(8).to_string(index=False))
```

| neighbor | distance (Å) |
|---|---:|
| Sb | 3.105 |
| Gd | 4.391 |
| Sb | 5.378 |
| Gd | 6.21 |
| Sb | 6.943 |
| Gd | 7.606 |
| Gd | 8.782 |
| Sb | 9.315 |

These shells are the raw material for coordination-number methods.

## 3. Coordination numbers (four methods)

Each method sorts neighbor distances and finds the largest gap on a
normalized curve:

| Method key | Distance normalized by |
|---|---|
| `dist_by_shortest_dist` | shortest distance from the site |
| `dist_by_CIF_radius_sum` | sum of CIF radii of the pair |
| `dist_by_CIF_radius_refined_sum` | sum of refined CIF radii |
| `dist_by_Pauling_radius_sum` | sum of Pauling CN12 radii |

```python
cif.compute_CN()  # or Cif(path, compute_CN=True)

rows = []
for site, methods in cif.CN_max_gap_per_site.items():
    for method, d in methods.items():
        rows.append(
            {"site": site, "method": method, "CN": d["CN"], "max_gap": d["max_gap"]}
        )
print(pd.DataFrame(rows).to_string(index=False))
```

| site | method | CN | max_gap |
|---|---|---:|---:|
| Sb | dist_by_shortest_dist | 6 | 0.414 |
| Sb | dist_by_CIF_radius_sum | 6 | 0.567 |
| Sb | dist_by_CIF_radius_refined_sum | 6 | 0.581 |
| Sb | dist_by_Pauling_radius_sum | 6 | 0.464 |
| Gd | dist_by_shortest_dist | 6 | 0.414 |
| Gd | dist_by_CIF_radius_sum | 18 | 0.441 |
| Gd | dist_by_CIF_radius_refined_sum | 18 | 0.453 |
| Gd | dist_by_Pauling_radius_sum | 18 | 0.366 |

Methods disagree for Gd (6 vs 18) — that is why cifkit computes all four
and then picks a **best method per site**.

## 4. Polyhedron metrics (best method)

The best method minimizes the distance from the polyhedron center to the
average of its vertices. Metrics are ready-made features:

```python
best = pd.DataFrame(
    [
        {
            "site": site,
            "method_used": m["method_used"],
            "CN (vertices)": m["number_of_vertices"],
            "edges": m["number_of_edges"],
            "faces": m["number_of_faces"],
            "volume": round(m["volume_of_polyhedron"], 3),
            "packing_eff": round(m["packing_efficiency"], 3),
        }
        for site, m in cif.CN_best_methods.items()
    ]
)
print(best.to_string(index=False))
```

| site | method_used | CN (vertices) | edges | faces | volume | packing_eff |
|---|---|---:|---:|---:|---:|---:|
| Sb | dist_by_shortest_dist | 6 | 12 | 8 | 39.914 | 0.605 |
| Gd | dist_by_shortest_dist | 6 | 12 | 8 | 39.914 | 0.605 |

Octahedra (6 / 12 / 8) with packing efficiency 0.605 — rock salt.

Neighbors in the CN shell for **Gd** (min-dist method):

```python
conns = cif.CN_connections_by_min_dist_method["Gd"]
neighbors = pd.DataFrame(
    [
        {"i": i + 1, "neighbor": c[0], "distance (Å)": round(c[1], 4)}
        for i, c in enumerate(conns)
    ]
)
print(neighbors.to_string(index=False))
```

| i | neighbor | distance (Å) |
|---:|---|---:|
| 1 | Sb | 3.105 |
| 2 | Sb | 3.105 |
| 3 | Sb | 3.105 |
| 4 | Sb | 3.105 |
| 5 | Sb | 3.105 |
| 6 | Sb | 3.105 |

## 5. Bond fractions and site mixing

```python
bonds = pd.DataFrame(
    [
        {"pair": str(k), "fraction": v}
        for k, v in cif.CN_bond_fractions_by_min_dist_method.items()
    ]
)
print(bonds.to_string(index=False))
print("site_mixing_type:", cif.site_mixing_type)
```

| pair | fraction |
|---|---:|
| ('Gd', 'Sb') | 1.0 |

```text
site_mixing_type: full_occupancy
```

Mixing info at the label-pair level is also available as
`mixing_info_per_label_pair` (useful when sites are partially occupied
or mixed).

## 6. Render the polyhedron

```python
for label in cif.site_labels:
    cif.plot_polyhedron(label, is_displayed=False, output_dir="polyhedrons")
# → GdSb_Sb.png, GdSb_Gd.png
```

Pass `is_displayed=True` for an interactive 3D window. A richer
polyhedron example from the
[JOSS paper](https://doi.org/10.21105/joss.07205) (ErCoIn₅, In1, CN=12):

```{figure} ../img/ErCoIn-polyhedron.png
:alt: ErCoIn5 In1 polyhedron CN=12
:align: center
:width: 60%

**JOSS Figure 1 (left).** ErCoIn₅ around In1 (CN=12).
```

## API reference

- [`Cif`](../api/cif) — parse, distances, mixing  
- [Coordination helpers](../api/coordination) — CN methods, geometry  

## What else?

Worth knowing, but not expanded on this page:

| Topic | Where |
|---|---|
| Radii used in CN methods (`radius_values`, `radius_sum`) | [`Cif` API](../api/cif) |
| Site mixing types beyond full occupancy | `site_mixing_type`, `mixing_info_per_label_pair` above; [API](../api/cif) |
| Folder-level CN / structure histograms before ML | [Statistics over many CIFs](statistics-many-cifs) |
| **Elemental properties for ML (OLED)** | **[OLED tutorial](oled)** · [Data in Brief](https://doi.org/10.1016/j.dib.2024.110178) |
| Downstream geometry featurizer built on cifkit | [SAF](https://github.com/bobleesj/structure-analyzer-featurizer) |

## Next

- **[Statistics over many CIFs](statistics-many-cifs)** — filter, histograms, sort a folder  
- **[OLED](oled)** — elemental / composition features for ML (Data in Brief dataset)
