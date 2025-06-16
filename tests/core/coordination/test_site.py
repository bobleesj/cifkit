from cifkit.coordination.site import get_min_distance_pair


def test_get_min_distance_pair(connections_URhIn):
    """Return the shortest distance."""
    min_dist_tuple = get_min_distance_pair(connections_URhIn)
    assert min_dist_tuple == (("In", "Rh"), 2.697)
