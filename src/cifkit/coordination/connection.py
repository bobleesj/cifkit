def get_CN_connections_by_best_methods(best_methods, connections: dict) -> dict:
    """Retrieve connections limited by the number of vertices (CN) for
    each label."""
    CN_connections = {}

    for label, data in best_methods.items():
        CN_value = data[
            "number_of_vertices"
        ]  # Extract the limit for the number of vertices
        # Limit the connections for this label using CN_value
        CN_connections[label] = connections[label][:CN_value]

    return CN_connections
