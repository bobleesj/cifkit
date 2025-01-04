from cifkit.utils.error_messages import OccupancyError


def frac_coordinates(atom_site_info: dict, label: str) -> tuple[str, str, str]:
    """Return a tuple of fractional coordinates."""
    x_frac = atom_site_info[label]["x_frac_coord"]
    y_frac = atom_site_info[label]["y_frac_coord"]
    z_frac = atom_site_info[label]["z_frac_coord"]
    return (x_frac, y_frac, z_frac)


def compute_coord_occupancy_sum(
    site_labels: list[str], atom_site_info: dict
) -> dict[tuple[str, str, str], float]:
    """Compute sum of occupancy per each coordinate."""
    coord_occupancy_sum: dict[tuple[str, str, str], float] = {}
    for label in site_labels:
        occupancy = round(
            atom_site_info[label]["site_occupancy"], 6
        )  # Round occupancy to 6 decimal places
        coordinates = frac_coordinates(atom_site_info, label)
        # Calculate the sum and round it
        current_sum = coord_occupancy_sum.get(coordinates, 0) + occupancy
        coord_occupancy_sum[coordinates] = round(current_sum, 6)

    return coord_occupancy_sum


def get_site_mixing_type(site_labels: list[str], atom_site_info: dict) -> str:
    """Get file-level atomic site mixing info."""

    is_full_occupancy = True
    coord_occupancy_sum = compute_coord_occupancy_sum(site_labels, atom_site_info)

    # Now check summed occupancies
    for _, occupancy_sum in coord_occupancy_sum.items():
        if occupancy_sum != 1:
            is_full_occupancy = False

    # Check for atomic mixing
    num_atom_labels = len(site_labels)
    is_atomic_mixing = len(coord_occupancy_sum) != num_atom_labels

    if is_atomic_mixing and not is_full_occupancy:
        return "deficiency_atomic_mixing"

    elif is_atomic_mixing and is_full_occupancy:
        return "full_occupancy_atomic_mixing"

    elif not is_atomic_mixing and not is_full_occupancy:
        return "deficiency_without_atomic_mixing"

    elif is_full_occupancy:
        return "full_occupancy"
    else:
        raise ValueError(OccupancyError.INVALID_MIXING_TYPE.value)


def get_mixing_type_per_pair_dict(
    site_labels: list[str], label_pairs: list[str], atom_site_info: dict
):
    """Return a dictionary, alphabetically sorted pair."""
    coord_occupancy_sum = compute_coord_occupancy_sum(site_labels, atom_site_info)

    # Store categorizy per pair
    atom_site_pair_dict = {}
    for pair in label_pairs:
        first_label = pair[0]
        second_label = pair[1]
        first_label_coord = frac_coordinates(atom_site_info, first_label)
        second_label_coord = frac_coordinates(atom_site_info, second_label)
        first_label_occ = atom_site_info[first_label]["site_occupancy"]
        second_label_occ = atom_site_info[second_label]["site_occupancy"]
        # Step 1. "full_occupancy"
        if first_label_occ == 1 and second_label_occ == 1:
            atom_site_pair_dict[pair] = "full_occupancy"
            continue

        # Step 2. Check deficiecny at the pair level
        is_first_label_site_deficient = None
        is_second_label_deficient = None

        if first_label_occ < 1 or second_label_occ < 1:
            if coord_occupancy_sum[first_label_coord] < 1:
                is_first_label_site_deficient = True
            else:
                is_first_label_site_deficient = False

            if coord_occupancy_sum[second_label_coord] < 1:
                is_second_label_deficient = True

            else:
                is_second_label_deficient = False

        # Step 3. Check mixing at the pair level
        # Subtract current label coordinates occupancy from the sum
        # If is zero, then no atomic mixing

        is_first_label_atomic_mixed = None
        is_second_label_atomic_mixed = None

        if (coord_occupancy_sum[first_label_coord] - first_label_occ) == 0.0:
            is_first_label_atomic_mixed = False
        else:
            is_first_label_atomic_mixed = True

        if (coord_occupancy_sum[second_label_coord] - second_label_occ) == 0.0:
            is_second_label_atomic_mixed = False
        else:
            is_second_label_atomic_mixed = True

        # Step 4. Assign category for each label pair
        # Check 1. One of the labels is deficient
        # Check 2. Both labels are not atomic mixed
        if (is_first_label_site_deficient or is_second_label_deficient) and (
            not is_first_label_atomic_mixed and not is_second_label_atomic_mixed
        ):
            atom_site_pair_dict[pair] = "deficiency_without_atomic_mixing"

        # Check 1. Both labels are not deficient
        # Check 2. At least one label is atomic mixed
        # Assign "2" for "full_occupancy_atomic_mixing"
        if (not is_first_label_site_deficient and not is_second_label_deficient) and (
            is_first_label_atomic_mixed or is_second_label_atomic_mixed
        ):
            atom_site_pair_dict[pair] = "full_occupancy_atomic_mixing"

        # Assign "1" for "deficiency_with_atomic_mixing"
        # Check 1. At least one label is deficient
        # Check 2. At least one label mixed
        if (is_first_label_site_deficient or is_second_label_deficient) and (
            is_first_label_atomic_mixed or is_second_label_atomic_mixed
        ):
            atom_site_pair_dict[pair] = "deficiency_with_atomic_mixing"

    return atom_site_pair_dict
