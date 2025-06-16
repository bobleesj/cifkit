import numpy as np
import pytest

from cifkit.preprocessors.environment import remove_duplicate_connections


def assert_minimum_distance(label, connections_dict, expected_min_distance):
    """Asserts that the minimum distance for a given label in the
    connections dictionary matches the expected minimum distance."""
    connections = connections_dict.get(label, [])

    # Check if there are any connections, and calculate the minimum distance
    if connections:
        min_distance = min(connection[1] for connection in connections)
        assert np.isclose(min_distance, expected_min_distance, atol=1e-2)


def test_get_nearest_dists_per_site_cooridnation_number(
    connections_URhIn,
):
    assert_minimum_distance("In1", connections_URhIn, 2.697)
    assert_minimum_distance("U1", connections_URhIn, 2.984)
    assert_minimum_distance("Rh1", connections_URhIn, 2.852)
    assert_minimum_distance("Rh2", connections_URhIn, 2.697)


@pytest.mark.fast
def test_remove_duplicate_connections():
    connections = {
        "CoM1": [
            ("CoM1", 2.618, [-1.33, -0.768, 1.06], [-1.33, 0.768, -1.06]),
            ("OsM2", 2.618, [-1.33, -0.768, 1.06], [-2.66, -1.536, 3.18]),
            ("CoM1", 2.618, [-1.33, -0.768, 1.06], [-2.66, -1.536, 3.18]),
            ("OsM2", 2.618, [-1.33, -0.768, 1.06], [-2.66, -1.536, -1.06]),
            ("OsM2", 2.618, [-1.33, -0.768, 1.06], [0.0, -1.536, 3.18]),
            ("OsM2", 2.618, [-1.33, -0.768, 1.06], [-1.33, 0.768, 3.18]),
        ],
        "OsM2": [
            ("OsM2", 2.618, [1.33, -0.768, 1.06], [2.66, -1.536, 3.18]),
            ("CoM1", 2.618, [1.33, -0.768, 1.06], [1.33, 0.768, 3.18]),
            ("OsM2", 2.618, [1.33, -0.768, 1.06], [1.33, 0.768, -1.06]),
            ("OsM2", 2.618, [1.33, -0.768, 1.06], [0.0, -1.536, 3.18]),
            ("CoM1", 2.618, [1.33, -0.768, 1.06], [1.33, 0.768, -1.06]),
            ("CoM1", 2.618, [1.33, -0.768, 1.06], [2.66, -1.536, 3.18]),
        ],
    }

    assert remove_duplicate_connections(connections) == {
        "CoM1": [
            ("CoM1", 2.618, [-1.33, -0.768, 1.06], [-1.33, 0.768, -1.06]),
            ("OsM2", 2.618, [-1.33, -0.768, 1.06], [-2.66, -1.536, 3.18]),
            ("OsM2", 2.618, [-1.33, -0.768, 1.06], [-2.66, -1.536, -1.06]),
            ("OsM2", 2.618, [-1.33, -0.768, 1.06], [0.0, -1.536, 3.18]),
            ("OsM2", 2.618, [-1.33, -0.768, 1.06], [-1.33, 0.768, 3.18]),
        ],
        "OsM2": [
            ("OsM2", 2.618, [1.33, -0.768, 1.06], [2.66, -1.536, 3.18]),
            ("CoM1", 2.618, [1.33, -0.768, 1.06], [1.33, 0.768, 3.18]),
            ("OsM2", 2.618, [1.33, -0.768, 1.06], [1.33, 0.768, -1.06]),
            ("OsM2", 2.618, [1.33, -0.768, 1.06], [0.0, -1.536, 3.18]),
        ],
    }
