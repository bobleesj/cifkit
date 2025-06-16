import numpy as np


def get_radians_from_degrees(angles: list[float]) -> list[float]:
    """Convert angles from degrees to radians and round to 5 decimal
    places."""
    radians = [round(float(np.radians(angle)), 5) for angle in angles]
    return radians


def round_float(distance: float, precision: int = 3) -> float:
    """Round a distance value to a specified precision."""
    return round(distance, precision)


def fractional_to_cartesian(
    fractional_coords: list[float],
    cell_lengths: list[float],
    cell_angles_rad: list[float],
) -> list[float]:
    """Convert fractional coordinates to Cartesian coordinates using
    cell lengths and angles."""
    alpha, beta, gamma = cell_angles_rad

    # Calculate the components of the transformation matrix
    a, b, c = cell_lengths
    cos_alpha = np.cos(alpha)
    cos_beta = np.cos(beta)
    cos_gamma = np.cos(gamma)
    sin_gamma = np.sin(gamma)

    # The volume of the unit cell
    volume = (
        a
        * b
        * c
        * np.sqrt(
            1
            - cos_alpha**2
            - cos_beta**2
            - cos_gamma**2
            + 2 * cos_alpha * cos_beta * cos_gamma
        )
    )

    # Transformation matrix from fractional to Cartesian coordinates
    matrix = np.array(
        [
            [a, b * cos_gamma, c * cos_beta],
            [
                0,
                b * sin_gamma,
                c * (cos_alpha - cos_beta * cos_gamma) / sin_gamma,
            ],
            [0, 0, volume / (a * b * sin_gamma)],
        ]
    )

    cartesian_coords = np.dot(matrix, fractional_coords).flatten()

    return cartesian_coords


def round_dict_values(dict, precision=3):
    if dict is None:
        return None
    rounded_dict = {
        k: round(v, precision) if isinstance(v, float) else v for k, v in dict.items()
    }
    return rounded_dict
