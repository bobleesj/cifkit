from scipy.spatial import ConvexHull

from cifkit.coordination.geometry import compute_polyhedron_metrics


def find_best_polyhedron(max_gaps_per_label, connections):
    """Find the best polyhedron for each label based on the minimum
    distance between the reference atom to the average position of
    connected atoms."""
    best_polyhedrons = {}

    for label, CN_data_per_method in max_gaps_per_label.items():
        # Initialize variables to track the best polyhedron
        min_distance_to_center = float("inf")
        best_polyhedron_metrics = None
        best_method_used = None

        for method, CN_data in CN_data_per_method.items():
            # Take only the top-N connections as determined by CN
            connection_data = connections[label][: CN_data["CN"]]
            if len(connection_data) < 4:
                continue

            # Extract neighbor coords and central atom
            neighbor_points = [c[3] for c in connection_data]
            central_point = connection_data[0][2]

            # Compute hull on neighbor points only
            try:
                hull = ConvexHull(neighbor_points, qhull_options="QJ")
            except Exception:
                print(
                    f"Error in polyhedron calculation for"
                    f"{label} using {method} - Skip"
                )
                continue

            # Prepare full point set for metrics (neighbors + central)
            points_for_metrics = neighbor_points + [central_point]

            # Compute metrics
            metrics = compute_polyhedron_metrics(points_for_metrics, hull)
            if metrics is None:
                continue

            dist = metrics["distance_from_avg_point_to_center"]
            if dist < min_distance_to_center:
                min_distance_to_center = dist
                best_polyhedron_metrics = metrics
                best_method_used = method

        if best_polyhedron_metrics:
            best_polyhedron_metrics["method_used"] = best_method_used
            best_polyhedrons[label] = best_polyhedron_metrics

    return best_polyhedrons


def get_CN_connections_by_min_dist_method(max_gaps_per_label, connections):
    CN_by_shortest_dist = {}
    for label, methods_info in max_gaps_per_label.items():
        # Access the 'dist_by_shortest_dist' method and get the 'CN' value
        CN_by_shortest_dist[label] = methods_info["dist_by_shortest_dist"]["CN"]

    CN_connections: dict = {}
    # Iterate through each label and number of connections
    for label, CN_value in CN_by_shortest_dist.items():
        if label in connections:
            CN_connections[label] = connections[label][:CN_value]

    return CN_connections
