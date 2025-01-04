import pytest
from scipy.spatial import ConvexHull

from cifkit.coordination.geometry import (
    compute_polyhedron_metrics,
    get_polyhedron_coordinates_labels,
)


@pytest.mark.fast
def test_get_polyhedron_coordinates_labels(
    CN_connections_by_min_dist_URhIn,
):
    (
        polyhedron_points,
        vertex_labels,
    ) = get_polyhedron_coordinates_labels(CN_connections_by_min_dist_URhIn, "U1")

    assert vertex_labels == [
        "Rh1",
        "Rh1",
        "Rh1",
        "Rh1",
        "Rh2",
        "In1",
        "In1",
        "In1",
        "In1",
        "In1",
        "In1",
        "U1",
    ]
    assert polyhedron_points[-1] == [4.43, 0.0, 0.0] or [
        -2.215,
        3.836,
        0.0,
    ]


@pytest.mark.fast
def test_compute_polyhedron_metrics():
    polyhedron_points = [
        [-0.0, 4.316, -1.94],
        [-0.0, 4.316, 1.94],
        [-3.738, 2.158, -1.94],
        [-3.738, 2.158, 1.94],
        [-3.738, 6.474, 0.0],
        [-0.936, 1.622, 1.94],
        [-0.936, 1.622, -1.94],
        [-4.674, 4.853, -1.94],
        [-4.674, 4.853, 1.94],
        [-1.865, 6.474, -1.94],
        [-1.865, 6.474, 1.94],
        [-2.215, 3.836, 0.0],
    ]

    hull = ConvexHull(polyhedron_points)
    polyhedron_metrics = compute_polyhedron_metrics(polyhedron_points, hull)
    assert polyhedron_metrics == {
        "volume_of_polyhedron": 60.631,
        "distance_from_avg_point_to_center": 0.328,
        "number_of_vertices": 11,
        "number_of_edges": 27,
        "number_of_faces": 18,
        "shortest_distance_to_face": 2.028,
        "shortest_distance_to_edge": 1.95,
        "volume_of_inscribed_sphere": 34.961,
        "packing_efficiency": 0.577,
    }
