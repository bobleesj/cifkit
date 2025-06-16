import gemmi
import numpy as np
from gemmi.cif import Block

from cifkit.preprocessors import supercell_util
from cifkit.utils import cif_parser


def get_supercell_points(
    block,
    supercell_size: int,
) -> list[tuple[float, float, float, str]]:
    """Return supercell points."""
    supercell_points = []
    loop_values = cif_parser.get_loop_values(block)
    all_coords_list = get_unitcell_coords_for_all_labels(block)

    # Get the total number of atoms in the unit cell
    for i, all_coords in enumerate(all_coords_list):
        points = flatten_original_coordinates(all_coords)
        atom_site_label = loop_values[0][i]

        supercell_points.extend(
            shift_and_append_points(
                points,
                atom_site_label,
                supercell_size,
            )
        )

    return list(set(supercell_points))


def get_unitcell_coords_for_all_labels(
    block: Block,
) -> list[list[tuple[float, float, float, str]]]:
    """Compute the new coordinates after applying symmetry operations to
    the initial coordinates."""

    loop_values = cif_parser.get_loop_values(block)
    loop_length = len(loop_values[0])
    coords_list = []
    for i in range(loop_length):
        (
            site_label,
            _,
            coordinates,
        ) = cif_parser.get_label_occupancy_coordinates(loop_values, i)

        coords_after_symmetry_operations = (
            get_unitcell_coords_after_sym_operations_per_label(
                block,
                coordinates,
                site_label,
            )
        )
        coords_list.append(coords_after_symmetry_operations)
    return coords_list


# Function to find and return the appropriate loop for symmetry operations
def find_symmetry_operations(block):
    # Try to find _space_group_symop_operation_xyz

    if block.find_loop("_space_group_symop_operation_xyz"):
        return block.find_loop("_space_group_symop_operation_xyz")
    elif block.find_loop("_symmetry_equiv_pos_as_xyz"):
        return block.find_loop("_symmetry_equiv_pos_as_xyz")
    else:
        raise ValueError("No symmetry operations found in the CIF file.")


def get_unitcell_coords_after_sym_operations_per_label(
    block: Block,
    atom_site_fracs: tuple[float, float, float],
    atom_site_label: str,
) -> list[tuple[float, float, float, str]]:
    """Generate a list of coordinates for each atom site after applying
    symmetry operations."""

    symmetry_operations = find_symmetry_operations(block)
    if symmetry_operations is not None:
        all_coords = set()
        for operation in symmetry_operations:
            operation = operation.replace("'", "")
            try:
                op = gemmi.Op(operation)
                new_x, new_y, new_z = op.apply_to_xyz(
                    [
                        atom_site_fracs[0],
                        atom_site_fracs[1],
                        atom_site_fracs[2],
                    ]
                )

                all_coords.add(
                    (
                        round(new_x, 5),
                        round(new_y, 5),
                        round(new_z, 5),
                        atom_site_label,
                    )
                )

            except RuntimeError as e:
                print(f"Skipping operation '{operation}': {str(e)}")

        return list(all_coords)


def flatten_original_coordinates(
    all_coords: list[tuple[float, float, float, str]],
):
    points = np.array([list(map(float, coord[:-1])) for coord in all_coords])
    return points


def shift_and_append_points(
    points,
    atom_site_label: str,
    supercell_generation_method: int,
):
    """Shift the unit cell's array of coordinates in the crystal frame
    to form the array containing the coordinates of the supercell.

    # Method 1 - No sfhits
    # Method 2 - +-1 +-1 +-1 shifts (This rarely used)
    # Method 3 - +-2 +-2 +-2 shifts (5*5*5 of the unit cell)
    """
    if supercell_generation_method == 1:
        shifts = np.array([[0, 0, 0]])
        shifted_points = points[:, None, :] + shifts
        all_points = []
        for point_group in shifted_points:
            for point in point_group:
                new_point = (*np.round(point, 5), atom_site_label)
                all_points.append(new_point)
        return all_points

    if supercell_generation_method == 2:
        shift_array = supercell_util._shift_xyz_plus_minus(1)
        shift_array = np.array(shift_array)
        shifted_points = points[:, None, :] + shift_array
        all_points = []
        for point_group in shifted_points:
            for point in point_group:
                new_point = (*np.round(point, 5), atom_site_label)
                all_points.append(new_point)
        return all_points

    if supercell_generation_method == 3:
        shift_array = supercell_util._shift_xyz_plus_minus(2)
        shift_array = np.array(shift_array)
        shifted_points = points[:, None, :] + shift_array
        all_points = []
        for point_group in shifted_points:
            for point in point_group:
                new_point = (*np.round(point, 5), atom_site_label)
                all_points.append(new_point)
        return all_points
