import numpy as np


def get_cell_atom_count(supercell_points) -> int:
    """Count the number of atoms in the cell."""
    return len(supercell_points)


def _shift_xyz_plus_minus(size) -> list[int]:
    """Provide 1D array for all crystal directions.

    Please check the "test_supercell_utils.py to see examples. This
    function is important in order to shift crystal coordinates from the
    unit cell to the coordinates of the supercell that is created by
    shifting."
    """
    arrays = []
    dimensions = np.arange(-size, size + 1, 1)
    dimensions = dimensions.tolist()
    for h in dimensions:
        for j in dimensions:
            for k in dimensions:
                arrays.append([h, j, k])
    return arrays
