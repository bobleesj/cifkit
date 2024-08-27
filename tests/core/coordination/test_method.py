import pytest

from cifkit.coordination.method import compute_CN_max_gap_per_site


@pytest.mark.fast
def test_compute_CN_max_gap_per_site(
    radius_sum_data_URhIn,
    connections_URhIn,
    max_gaps_per_label_URhIn,
):
    result = compute_CN_max_gap_per_site(
        radius_sum_data_URhIn,
        connections_URhIn,
        True,
        "full_occupancy",
    )

    for key, actual_data in result.items():
        expected_data = max_gaps_per_label_URhIn[key]
        for method, actual_metrics in actual_data.items():
            expected_metrics = expected_data[method]
            assert actual_metrics["CN"] == expected_metrics["CN"]
            assert actual_metrics["max_gap"] == pytest.approx(
                expected_metrics["max_gap"], abs=0.002
            )


@pytest.mark.fast
def test_compute_CN_max_gap_per_site_dist_min_method_only(
    radius_sum_data_URhIn, connections_URhIn
):
    CN_max_gap_per_site = compute_CN_max_gap_per_site(
        radius_sum_data_URhIn,
        connections_URhIn,
        True,
        "full_occupancy_with_atomic_mixing",
    )

    assert CN_max_gap_per_site == {
        "In1": {"dist_by_shortest_dist": {"max_gap": 0.306, "CN": 14}},
        "U1": {"dist_by_shortest_dist": {"max_gap": 0.197, "CN": 11}},
        "Rh1": {"dist_by_shortest_dist": {"max_gap": 0.315, "CN": 9}},
        "Rh2": {"dist_by_shortest_dist": {"max_gap": 0.31, "CN": 9}},
    }
