import pytest

from cifkit.coordination.filter import (
    find_best_polyhedron,
    get_CN_connections_by_min_dist_method,
)


@pytest.mark.fast
def test_find_best_polyhedron(max_gaps_per_label_URhIn, connections_URhIn):
    result = find_best_polyhedron(max_gaps_per_label_URhIn, connections_URhIn)
    # Define a dictionary of expected values for specific keys
    expected_values = {
        "In1": {
            "method_used": "dist_by_shortest_dist",
            "number_of_vertices": 14,
            "distance_from_avg_point_to_center": 0.137,
        },
        "U1": {
            "method_used": "dist_by_CIF_radius_refined_sum",
            "number_of_vertices": 17,
            "distance_from_avg_point_to_center": 0.032,
        },
        "Rh1": {
            "method_used": "dist_by_shortest_dist",
            "number_of_vertices": 9,
            "distance_from_avg_point_to_center": 0.0,
        },
        "Rh2": {
            "method_used": "dist_by_shortest_dist",
            "number_of_vertices": 9,
            "distance_from_avg_point_to_center": 0.0,
        },
    }

    # Iterate over the keys and check only the specified fields
    for key, expected in expected_values.items():
        assert result[key]["method_used"] == expected["method_used"]
        assert result[key]["number_of_vertices"] == expected["number_of_vertices"]
        assert (
            result[key]["distance_from_avg_point_to_center"]
            == expected["distance_from_avg_point_to_center"]
        )


@pytest.mark.fast
def test_get_CN_connections_by_dist_min_method(
    max_gaps_per_label_URhIn, connections_URhIn
):
    CN_connections = get_CN_connections_by_min_dist_method(
        max_gaps_per_label_URhIn, connections_URhIn
    )
    assert len(CN_connections["In1"]) == 14
    assert len(CN_connections["Rh1"]) == 9
    assert len(CN_connections["Rh2"]) == 9
    assert len(CN_connections["U1"]) == 11
