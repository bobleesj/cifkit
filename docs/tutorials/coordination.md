# Coordination

`cifkit` determines the coordination number (CN) of each atomic site
with **four methods**, then selects the best one per site. Each method
sorts neighbor distances and looks for the largest gap in a normalized
distance curve:

| Method key | Distance normalized by |
|---|---|
| `dist_by_shortest_dist` | shortest distance from the site |
| `dist_by_CIF_radius_sum` | sum of CIF radii of the pair |
| `dist_by_CIF_radius_refined_sum` | sum of refined CIF radii |
| `dist_by_Pauling_radius_sum` | sum of Pauling CN12 radii |

All outputs below are real outputs on the packaged GdSb example.

## Compute CN metrics

CN work is deferred by default. Either construct with
`Cif(path, compute_CN=True)` or call `compute_CN()` when you need it:

```python
from cifkit import Cif, Example

cif = Cif(Example.GdSb_file_path)
cif.compute_CN()
```

## The max-gap table

`CN_max_gap_per_site` records, per site and per method, where the
largest gap in the normalized neighbor-distance curve occurs and the CN
it implies:

```python
print(cif.CN_max_gap_per_site)
```

```text
{'Sb': {'dist_by_shortest_dist': {'max_gap': 0.414, 'CN': 6}, 'dist_by_CIF_radius_sum': {'max_gap': 0.567, 'CN': 6}, 'dist_by_CIF_radius_refined_sum': {'max_gap': 0.581, 'CN': 6}, 'dist_by_Pauling_radius_sum': {'max_gap': 0.464, 'CN': 6}}, 'Gd': {'dist_by_shortest_dist': {'max_gap': 0.414, 'CN': 6}, 'dist_by_CIF_radius_sum': {'max_gap': 0.441, 'CN': 18}, 'dist_by_CIF_radius_refined_sum': {'max_gap': 0.453, 'CN': 18}, 'dist_by_Pauling_radius_sum': {'max_gap': 0.366, 'CN': 18}}}
```

Note the methods disagree for Gd (6 vs 18) - this is exactly why
`cifkit` computes all four and then picks a best method per site.

## Best method per site

The best method minimizes the distance from the polyhedron center to
its vertices' average point, and its polyhedron metrics come along for
free:

```python
import json

print(json.dumps(cif.CN_best_methods["Gd"], indent=2))
```

```text
{
  "volume_of_polyhedron": 39.914,
  "distance_from_avg_point_to_center": 0.0,
  "number_of_vertices": 6,
  "number_of_edges": 12,
  "number_of_faces": 8,
  "shortest_distance_to_face": 1.793,
  "shortest_distance_to_edge": 2.196,
  "volume_of_inscribed_sphere": 24.132,
  "packing_efficiency": 0.605,
  "method_used": "dist_by_shortest_dist"
}
```

Both GdSb sites form an octahedron (6 vertices, 12 edges, 8 faces) with
a packing efficiency of 0.605 - the rock-salt structure, as expected.

## CN summary properties

Every metric exists in a `_by_min_dist_method` and a
`_by_best_methods` variant:

```python
print("CN values:", cif.CN_unique_values_by_min_dist_method)
print("CN avg / min / max:",
      cif.CN_avg_by_min_dist_method,
      cif.CN_min_by_min_dist_method,
      cif.CN_max_by_min_dist_method)
print("bond counts:", cif.CN_bond_count_by_min_dist_method)
print("bond fractions:", cif.CN_bond_fractions_by_min_dist_method)
```

```text
CN values: {6}
CN avg / min / max: 6.0 6 6
bond counts: {'Sb': {('Gd', 'Sb'): 6}, 'Gd': {('Gd', 'Sb'): 6}}
bond fractions: {('Gd', 'Sb'): 1.0}
```

## Coordination environment

The actual neighbors within the CN shell are available per site. Each
connection is `(label, distance, self_coordinates, neighbor_coordinates)`:

```python
connections = cif.CN_connections_by_min_dist_method
print(len(connections["Gd"]), "neighbors")
print(connections["Gd"][0])
```

```text
6 neighbors
('Sb', 3.105, [0.0, 0.0, 0.0], [-0.0, -0.0, 3.105])
```

## Render the polyhedron

`plot_polyhedron` renders the coordination polyhedron of a site with
pyvista and saves a `{formula}_{site_label}.png` per label (GdSb yields
`GdSb_Gd.png` and `GdSb_Sb.png`). It uses the best-method connections,
so call `compute_CN()` first:

```python
for label in cif.site_labels:
    cif.plot_polyhedron(label, is_displayed=False, output_dir="polyhedrons")
```

Pass `is_displayed=True` to open an interactive 3D window instead of
saving quietly.

## Reference

The geometry math (polyhedron metrics), CN method selection, and
site/composition helpers are documented in the
[Coordination API reference](../api/coordination).
