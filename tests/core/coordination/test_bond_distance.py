from cifkit.coordination.bond_distance import get_shortest_distance_per_bond_pair


def test_get_minimum_dist_per_bond_pair(
    flattened_connections_URhIn,
):
    # Call the function under test
    min_dist_per_element_pair = get_shortest_distance_per_bond_pair(
        flattened_connections_URhIn
    )

    # Assert that the actual minimum distances match the expected results
    assert min_dist_per_element_pair == {
        ("In", "In"): 3.244,
        ("In", "Rh"): 2.697,
        ("In", "U"): 3.21,
        ("Rh", "Rh"): 3.881,
        ("Rh", "U"): 2.983,
        ("U", "U"): 3.881,
    }
