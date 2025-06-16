import numpy as np

from cifkit.utils import bond_pair
from cifkit.utils.string_parser import get_atom_type_from_label


def get_bond_counts(
    elements: list[str],
    connections: dict[str, list],
    sorted_by_mendeleev=False,
) -> dict[str, dict[tuple[str, str], int]]:
    """Return a dictionary containing bond pairs and counts per label
    site."""
    if sorted_by_mendeleev:
        bond_pairs = bond_pair.get_pairs_sorted_by_mendeleev(elements)
    else:
        bond_pairs = bond_pair.get_bond_pairs(elements)

    # Initialize the dictionary to hold bond pair counts for each label
    bond_counts: dict = {}

    # Iterate over each label and its connections
    for label, label_connections in connections.items():
        # Initialize the bond count for the current label
        bond_counts[label] = {}

        # Get the atom type for the reference label
        ref_element = get_atom_type_from_label(label)

        # Iterate over each connection for the current label
        for conn in label_connections:
            conn_label, _, _, _ = conn

            # Get the atom type for the connected label
            conn_element = get_atom_type_from_label(conn_label)

            # Create a tuple representing the bond pair, sorted
            pair = (ref_element, conn_element)
            sorted_bond_pair = None

            # Sort by Mendeeleve
            if sorted_by_mendeleev:
                sorted_bond_pair = bond_pair.order_tuple_pair_by_mendeleev(pair)
            else:
                sorted_bond_pair = tuple(sorted((ref_element, conn_element)))

            # Check if the bond pair is one of the valid pairs
            if sorted_bond_pair in bond_pairs:
                if sorted_bond_pair in bond_counts[label]:
                    bond_counts[label][sorted_bond_pair] += 1
                else:
                    bond_counts[label][sorted_bond_pair] = 1

    return bond_counts


def get_bond_fractions(bond_pair_data: dict) -> dict[tuple[str, str], float]:
    """Calculate the fraction of each bond type across all labels."""
    total_bond_counts: dict[tuple[str, str], float] = {}
    total_bonds = 0

    # Sum up bond counts for each bond type
    for bonds in bond_pair_data.values():
        for bond_type, count in bonds.items():
            if bond_type in total_bond_counts:
                total_bond_counts[bond_type] += count
            else:
                total_bond_counts[bond_type] = count
            total_bonds += count

    # Calculate fractions
    bond_fractions = {
        bond_type: round(count / total_bonds, 3)
        for bond_type, count in total_bond_counts.items()
    }

    return bond_fractions


def count_connections_per_site(connections: dict) -> dict[str, int]:
    """Calculate the coordination number for each atom site."""
    neighbor_count = {}
    for label, connection_data in connections.items():
        neighbor_count[label] = len(connection_data)

    return neighbor_count


def compute_avg_CN(connections: dict[str, int]) -> float:
    """Calculate the average coordination number across all sites."""
    coordination_numbers = count_connections_per_site(connections)
    total = 0
    for _, value in coordination_numbers.items():
        total += value
    return np.round(total / len(coordination_numbers), 3)


def get_unique_CN_values(connections: dict) -> set[int]:
    """Return unique coordination numbers from all sites."""
    coordination_numbers = count_connections_per_site(connections)
    unique_numbers = set(coordination_numbers.values())
    return unique_numbers
