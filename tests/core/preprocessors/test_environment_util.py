import pytest

from cifkit.preprocessors.environment_util import flat_site_connections


@pytest.mark.fast
def test_flat_site_connections(connections_URhIn):
    flattened_connections = flat_site_connections(connections_URhIn)

    assert isinstance(flattened_connections, list)

    for connection in flattened_connections:
        assert (
            isinstance(connection, tuple) and len(connection) == 2
        ), "Each item should be a tuple with two elements."
        assert (
            isinstance(connection[0], tuple) and len(connection[0]) == 2
        ), "First element of each item should be a tuple of two strings."
        assert isinstance(
            connection[1], float
        ), "Second element of each item should be a float."
        assert all(
            isinstance(label, str) for label in connection[0]
        ), "Both elements in the label tuple should be strings."

    assert flattened_connections[0] == (("In", "Rh"), 2.697)
    assert flattened_connections[1] == (("In", "Rh"), 2.697)
