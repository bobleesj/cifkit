import numpy as np

from cifkit.preprocessors.supercell_util import _shift_points


def test_shifted_crystal_points():
    actual_points_shifted = _shift_points(1)
    # Shift +/- 1 in each direction, expected 3 by 3 by 3 supercell (27 unit cells)
    print(actual_points_shifted)
    assert len(actual_points_shifted) == 27
    assert actual_points_shifted == [
        [-1, -1, -1],
        [-1, -1, 0],
        [-1, -1, 1],
        [-1, 0, -1],
        [-1, 0, 0],
        [-1, 0, 1],
        [-1, 1, -1],
        [-1, 1, 0],
        [-1, 1, 1],
        [0, -1, -1],
        [0, -1, 0],
        [0, -1, 1],
        [0, 0, -1],
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, -1],
        [0, 1, 0],
        [0, 1, 1],
        [1, -1, -1],
        [1, -1, 0],
        [1, -1, 1],
        [1, 0, -1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, -1],
        [1, 1, 0],
        [1, 1, 1],
    ]
    actual_points_shifted = _shift_points(2)
    # Shift +/- 2 in each direction, expected 5 by 5 by 5 supercell (125 unit cells)
    assert len(actual_points_shifted) == 125
    print(actual_points_shifted)
