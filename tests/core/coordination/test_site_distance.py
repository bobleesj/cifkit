import pytest

from cifkit.coordination.site_distance import (
    get_shortest_distance,
    get_shortest_distance_per_site,
)


def test_get_shortest_distance(connections_URhIn):
    assert get_shortest_distance(connections_URhIn) == 2.697


def test_get_shortest_distance_per_site(connections_URhIn):
    expected = {
        "In1": ("Rh2", 2.697),
        "Rh1": ("In1", 2.852),
        "Rh2": ("In1", 2.697),
        "U1": ("Rh1", 2.984),
    }
    result = get_shortest_distance_per_site(connections_URhIn)

    assert all(
        result[label][0] == expected[label][0]
        and pytest.approx(result[label][1], 0.001) == expected[label][1]
        for label in expected
    )
