from cifkit.coordination.geometry import get_polyhedron_coordinates_labels


def test_CN_connections_by_min_dist(
    CN_connections_by_min_dist_URhIn,
):
    expected_labels = [
        "Rh2",
        "Rh2",
        "Rh1",
        "Rh1",
        "U1",
        "U1",
        "In1",
        "In1",
        "U1",
        "U1",
        "U1",
        "U1",
        "In1",
        "In1",
        "In1",
    ]

    polyhedron_points, labels = get_polyhedron_coordinates_labels(
        CN_connections_by_min_dist_URhIn, "In1"
    )
    assert len(polyhedron_points) == 15
    assert labels == expected_labels
