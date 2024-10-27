import numpy as np


def calc_dist_two_cart_points(
    point1: list[float],
    point2: list[float],
) -> float:
    """Calculate the Euclidean distance between two points in Cartesian
    coordinates."""
    diff = np.array(point2) - np.array(point1)
    distance = float(np.linalg.norm(diff))

    return distance
