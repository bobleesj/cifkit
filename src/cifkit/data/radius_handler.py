import numpy as np
from bobleesj.utils.sources import radius

from cifkit.data.radius_optimization import get_refined_CIF_radius
from cifkit.utils.unit import round_dict_values


def get_CIF_pauling_radius(elements: list[str]) -> dict:
    """Return CIF and Pualing data for a list of elements."""
    data = radius.data()
    radii = {}
    for atom in elements:
        radii[atom] = {
            "CIF_radius": data[atom]["CIF"],
            "Pauling_radius_CN12": data[atom]["Pauling_CN12"],
        }
    return radii


def get_radius_values_per_element(
    elements: list[str], shortest_bond_distances
) -> dict[str : dict[str:float]]:
    """Merge CIF and Pauling radius data with CIF refined radius
    data."""
    is_radius_data_available = radius.are_available(elements)
    if not is_radius_data_available:
        return None
    CIF_pauling_rad = get_CIF_pauling_radius(elements)
    CIF_refined_rad, _ = get_refined_CIF_radius(elements, shortest_bond_distances)
    combined_radii = {}
    for element in elements:
        combined_radii[element] = {
            "CIF_radius": CIF_pauling_rad[element]["CIF_radius"],
            "CIF_radius_refined": float(np.round(CIF_refined_rad.get(element), 3)),
            "Pauling_radius_CN12": CIF_pauling_rad[element]["Pauling_radius_CN12"],
        }
    return round_dict_values(combined_radii)


def compute_radius_sum(
    radius_values: dict[str : dict[str:float]], is_radius_data_available: bool
) -> dict[str : dict[str:float]]:
    """Compute the sum of two radii."""
    if not is_radius_data_available:
        return None

    elements = sorted(radius_values.keys())
    pair_distances: dict[str : dict[str, float]] = {
        "CIF_radius_sum": {},
        "CIF_radius_refined_sum": {},
        "Pauling_radius_sum": {},
    }
    # Calculate pair sums for each unique combination of elements
    for i, elem_i in enumerate(elements):
        for j in range(i, len(elements)):
            elem_j = elements[j]
            # Element pair label, e.g., A-B or A-A
            pair_label = f"{elem_i}-{elem_j}" if i != j else f"{elem_i}-{elem_i}"

            # Sum radii for each radius type
            pair_distances["CIF_radius_sum"][pair_label] = round(
                radius_values[elem_i]["CIF_radius"] + radius_values[elem_j]["CIF_radius"],
                3,
            )
            pair_distances["CIF_radius_refined_sum"][pair_label] = round(
                radius_values[elem_i]["CIF_radius_refined"]
                + radius_values[elem_j]["CIF_radius_refined"],
                3,
            )
            pair_distances["Pauling_radius_sum"][pair_label] = round(
                radius_values[elem_i]["Pauling_radius_CN12"]
                + radius_values[elem_j]["Pauling_radius_CN12"],
                3,
            )
    return pair_distances
