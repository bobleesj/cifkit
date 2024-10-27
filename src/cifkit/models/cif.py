import logging
import os

# Bond pair
from cifkit.coordination.bond_distance import get_shortest_distance_per_bond_pair
from cifkit.coordination.composition import (
    compute_avg_CN,
    get_bond_counts,
    get_bond_fractions,
    get_unique_CN_values,
)
from cifkit.coordination.connection import get_CN_connections_by_best_methods
from cifkit.coordination.filter import (
    find_best_polyhedron,
    get_CN_connections_by_min_dist_method,
)
from cifkit.coordination.geometry import get_polyhedron_coordinates_labels
from cifkit.coordination.method import compute_CN_max_gap_per_site

# Site info
from cifkit.coordination.site_distance import (
    get_shortest_distance,
    get_shortest_distance_per_site,
)

# Radius
from cifkit.data.radius_handler import (
    compute_radius_sum,
    get_is_radius_data_available,
    get_radius_values_per_element,
)
from cifkit.figures import polyhedron
from cifkit.occupancy.mixing import get_mixing_type_per_pair_dict, get_site_mixing_type
from cifkit.preprocessors.environment import get_site_connections

# Coordination number
from cifkit.preprocessors.environment_util import flat_site_connections

# Supercell generation
from cifkit.preprocessors.supercell import get_supercell_points
from cifkit.preprocessors.supercell_util import get_cell_atom_count
from cifkit.utils.bond_pair import get_bond_pairs, get_pairs_sorted_by_mendeleev

# Edit .cif file
from cifkit.utils.cif_editor import edit_cif_file_based_on_db

# Parser .cif file
from cifkit.utils.cif_parser import (
    get_cif_block,
    get_formula_structure_weight_s_group,
    get_loop_values,
    get_tag_from_third_line,
    get_unique_elements_from_loop,
    get_unique_site_labels,
    get_unitcell_angles_rad,
    get_unitcell_lengths,
    parse_atom_site_occupancy_info,
)

# Identify .cif database source
from cifkit.utils.cif_sourcer import get_cif_db_source
from cifkit.utils.log_messages import CifLog
from cifkit.utils.unit import round_dict_values


def ensure_connections(func):
    """For accessing lazy properties and methods, compute connections."""

    def wrapper(self, *args, **kwargs):
        if self.connections is None:
            self.compute_connections()
        return func(self, *args, **kwargs)

    return wrapper


# Global logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Cif:
    def __init__(
        self, file_path: str, is_formatted=False, logging_enabled=False
    ) -> None:
        """_summary_

        Parameters
        ----------
        file_path : str
            _description_
        is_formatted : bool, optional
            _description_, by default False
        logging_enabled : bool, optional
            _description_, by default False
        """

        self.file_path = file_path
        self.logging_enabled = logging_enabled

        """Initialize the Cif object with the file path."""
        self.file_name = os.path.basename(file_path)
        self.file_name_without_ext = os.path.splitext(self.file_name)[0]
        self.db_source = get_cif_db_source(self.file_path)
        self.connections = None  # Private attribute to store connections
        self._shortest_pair_distance = None

        # If it is not previously formatted
        if not is_formatted:
            self._preprocess()

        self._load_data()

    def _log_info(self, message):
        """Log a formatted message if logging is enabled."""
        if self.logging_enabled:
            formatted_message = message.format(
                file_path=self.file_path, file_name=self.file_name
            )
            logging.info(formatted_message)

    def _preprocess(self):
        """Preprocess each .cif file and check any error."""
        self._log_info(CifLog.PREPROCESSING.value)
        edit_cif_file_based_on_db(self.file_path)

    def _load_data(self):
        """Load data from the .cif file and process it."""
        self._log_info(CifLog.LOADING_DATA.value)
        self._block = get_cif_block(self.file_path)
        self._parse_cif_data()
        self._generate_supercell()

    def _parse_cif_data(self):
        """Parse the main CIF data from the block."""
        self._loop_values = get_loop_values(self._block)
        self.unitcell_lengths = get_unitcell_lengths(self._block)
        self.unitcell_angles = get_unitcell_angles_rad(self._block)
        self.site_labels = get_unique_site_labels(self._loop_values)
        self.unique_elements = get_unique_elements_from_loop(self._loop_values)
        (
            self.formula,
            self.structure,
            self.weight,
            self.space_group_number,
            self.space_group_name,
        ) = get_formula_structure_weight_s_group(self._block)
        self.atom_site_info = parse_atom_site_occupancy_info(self.file_path)
        self.composition_type = len(self.unique_elements)
        self.tag = get_tag_from_third_line(self.file_path, self.db_source)
        self.bond_pairs = get_bond_pairs(self.unique_elements)
        self.site_label_pairs = get_bond_pairs(self.site_labels)
        self.bond_pairs_sorted_by_mendeleev = get_pairs_sorted_by_mendeleev(
            self.unique_elements
        )
        self.site_label_pairs_sorted_by_mendeleev = (
            get_pairs_sorted_by_mendeleev(self.site_labels)
        )
        self.site_mixing_type = get_site_mixing_type(
            self.site_labels, self.atom_site_info
        )
        self.is_radius_data_available = get_is_radius_data_available(
            self.unique_elements
        )
        self.mixing_info_per_label_pair = get_mixing_type_per_pair_dict(
            self.site_labels, self.site_label_pairs, self.atom_site_info
        )
        self.mixing_info_per_label_pair_sorted_by_mendeleev = (
            get_mixing_type_per_pair_dict(
                self.site_labels,
                self.site_label_pairs_sorted_by_mendeleev,
                self.atom_site_info,
            )
        )

    def _generate_supercell(self) -> None:
        """Generate supercell information based on the unit cell data.

        This method calculates the supercell points and atom counts based
        on the unit cell data. It uses the `get_supercell_points` and
        `get_cell_atom_count` functions to perform the calculations.

        Returns:
            None
        """
        # Method implementation goes here
        self.unitcell_points = get_supercell_points(self._block, 1)
        self.supercell_points = get_supercell_points(self._block, 3)
        self.unitcell_atom_count = get_cell_atom_count(self.unitcell_points)
        self.supercell_atom_count = get_cell_atom_count(self.supercell_points)

    def compute_connections(self, cutoff_radius=10.0):
        """_summary_

        Args:
            cutoff_radius (float, optional): _description_. Defaults to 10.0.
        """
        self._log_info(CifLog.COMPUTE_CONNECTIONS.value)
        self.connections = get_site_connections(
            [
                self.site_labels,
                self.unitcell_lengths,
                self.unitcell_angles,
            ],
            self.unitcell_points,
            self.supercell_points,
            cutoff_radius=cutoff_radius,
        )

        # Flattened coordinations
        self._connections_flattened = flat_site_connections(self.connections)

        # Shortest distance
        self._shortest_distance = get_shortest_distance(self.connections)

        # Shortest distance per bond pair
        self._shortest_bond_pair_distance = (
            get_shortest_distance_per_bond_pair(self.connections_flattened)
        )

        # Shortest distance per site
        self._shortest_site_pair_distance = get_shortest_distance_per_site(
            self.connections
        )

        # Parse individual radii per element
        self._radius_values = round_dict_values(
            get_radius_values_per_element(
                self.unique_elements, self.shortest_bond_pair_distance
            )
        )
        self._radius_sum = compute_radius_sum(
            self.radius_values, self.is_radius_data_available
        )

        # CN max gap per site
        self._CN_max_gap_per_site = compute_CN_max_gap_per_site(
            self.radius_sum,
            self.connections,
            self.is_radius_data_available,
            self.site_mixing_type,
        )

        # Find the best methods
        self._CN_best_methods = find_best_polyhedron(
            self.CN_max_gap_per_site, self.connections
        )

        # Get CN connections by the best methods
        self._CN_connections_by_best_methods = (
            get_CN_connections_by_best_methods(
                self.CN_best_methods, self.connections
            )
        )

        # Get CN connections by the best methods
        self._CN_connections_by_min_dist_method = (
            get_CN_connections_by_min_dist_method(
                self.CN_max_gap_per_site, self.connections
            )
        )
        # Bond counts
        self._CN_bond_count_by_min_dist_method = get_bond_counts(
            self.unique_elements, self.CN_connections_by_min_dist_method
        )
        self._CN_bond_count_by_best_methods = get_bond_counts(
            self.unique_elements, self.CN_connections_by_best_methods
        )

        # Bond counts sorted by mendeleev
        self._CN_bond_count_by_min_dist_method_sorted_by_mendeleev = (
            get_bond_counts(
                self.unique_elements,
                self.CN_connections_by_min_dist_method,
                sorted_by_mendeleev=True,
            )
        )
        self._CN_bond_count_by_best_methods_sorted_by_mendeleev = (
            get_bond_counts(
                self.unique_elements,
                self.CN_connections_by_best_methods,
                sorted_by_mendeleev=True,
            )
        )

        # Bond fractions
        self._CN_bond_fractions_by_min_dist_method = get_bond_fractions(
            self.CN_bond_count_by_min_dist_method
        )
        self._CN_bond_fractions_by_best_methods = get_bond_fractions(
            self.CN_bond_count_by_best_methods
        )

        # Bond fractions sorted by Mendeleev
        self._CN_bond_fractions_by_min_dist_method_sorted_by_mendeleev = (
            get_bond_fractions(
                self.CN_bond_count_by_min_dist_method_sorted_by_mendeleev
            )
        )

        self._CN_bond_fractions_by_best_methods_sorted_by_mendeleev = (
            get_bond_fractions(
                self.CN_bond_count_by_best_methods_sorted_by_mendeleev
            )
        )

        # Unique CN
        self._CN_unique_values_by_min_dist_method = get_unique_CN_values(
            self.CN_connections_by_min_dist_method
        )
        self._CN_unique_values_by_best_methods = get_unique_CN_values(
            self.CN_connections_by_best_methods
        )

        # Avg CN
        self._CN_avg_by_min_dist_method = compute_avg_CN(
            self.CN_connections_by_min_dist_method
        )

        self._CN_avg_by_best_methods = compute_avg_CN(
            self.CN_connections_by_best_methods
        )

        # Max CN
        self._CN_max_by_min_dist_method = max(
            self.CN_unique_values_by_min_dist_method
        )
        self._CN_max_by_best_methods = max(
            self.CN_unique_values_by_best_methods
        )
        # Min CN
        self._CN_min_by_min_dist_method = min(
            self.CN_unique_values_by_min_dist_method
        )
        self._CN_min_by_best_methods = min(
            self.CN_unique_values_by_best_methods
        )

    @property
    @ensure_connections
    def shortest_distance(self):
        """Property that checks if connections are computed and computes."""
        return self._shortest_distance

    @property
    @ensure_connections
    def connections_flattened(self):
        """Property that combine site connections into a single array."""
        return self._connections_flattened

    @property
    @ensure_connections
    def shortest_bond_pair_distance(self):
        return self._shortest_bond_pair_distance

    @property
    @ensure_connections
    def shortest_site_pair_distance(self):
        return self._shortest_site_pair_distance

    @property
    @ensure_connections
    def radius_values(self):
        return self._radius_values

    @property
    @ensure_connections
    def radius_sum(self):
        return self._radius_sum

    @property
    @ensure_connections
    def CN_max_gap_per_site(self):
        return self._CN_max_gap_per_site

    @property
    @ensure_connections
    def CN_best_methods(self):
        return self._CN_best_methods

    @property
    @ensure_connections
    def CN_connections_by_best_methods(self):
        return self._CN_connections_by_best_methods

    @property
    @ensure_connections
    def CN_connections_by_min_dist_method(self):
        return self._CN_connections_by_min_dist_method

    """
    Compute avg, min, max, unique for best and min_dist method
    """

    # 1.1 Bond counts
    @property
    @ensure_connections
    def CN_bond_count_by_min_dist_method(self):
        return self._CN_bond_count_by_min_dist_method

    @property
    @ensure_connections
    def CN_bond_count_by_best_methods(self):
        return self._CN_bond_count_by_best_methods

    # 1.2 Bond counts sorted by mendeleev
    @property
    @ensure_connections
    def CN_bond_count_by_min_dist_method_sorted_by_mendeleev(self):
        return self._CN_bond_count_by_min_dist_method_sorted_by_mendeleev

    @property
    @ensure_connections
    def CN_bond_count_by_best_methods_sorted_by_mendeleev(self):
        return self._CN_bond_count_by_best_methods_sorted_by_mendeleev

    # 2.1 Bond fractions
    @property
    @ensure_connections
    def CN_bond_fractions_by_min_dist_method(self):
        return self._CN_bond_fractions_by_min_dist_method

    @property
    @ensure_connections
    def CN_bond_fractions_by_best_methods(self):
        return self._CN_bond_fractions_by_best_methods

    # 2.2. Bond fractions sorted by Mendeleev
    @property
    @ensure_connections
    def CN_bond_fractions_by_min_dist_method_sorted_by_mendeleev(self):
        return self._CN_bond_fractions_by_min_dist_method_sorted_by_mendeleev

    @property
    @ensure_connections
    def CN_bond_fractions_by_best_methods_sorted_by_mendeleev(self):
        return self._CN_bond_fractions_by_best_methods_sorted_by_mendeleev

    # Unique CN
    @property
    @ensure_connections
    def CN_unique_values_by_min_dist_method(self):
        return self._CN_unique_values_by_min_dist_method

    @property
    @ensure_connections
    def CN_unique_values_by_best_methods(self):
        return self._CN_unique_values_by_best_methods

    # Average CN
    @property
    @ensure_connections
    def CN_avg_by_min_dist_method(self):
        return self._CN_avg_by_min_dist_method

    @property
    @ensure_connections
    def CN_avg_by_best_methods(self):
        return self._CN_avg_by_best_methods

    @property
    @ensure_connections
    def CN_max_by_min_dist_method(self):
        return self._CN_max_by_min_dist_method

    @property
    @ensure_connections
    def CN_max_by_best_methods(self):
        return self._CN_max_by_best_methods

    @property
    @ensure_connections
    def CN_min_by_min_dist_method(self):
        return self._CN_min_by_min_dist_method

    @property
    @ensure_connections
    def CN_min_by_best_methods(self):
        return self._CN_min_by_best_methods

    @ensure_connections
    def get_polyhedron_labels_by_CN_min_dist_method(
        self, label: str
    ) -> tuple[list[list[float]], list[str]]:
        return get_polyhedron_coordinates_labels(
            self.CN_connections_by_min_dist_method, label
        )

    @ensure_connections
    def get_polyhedron_labels_by_CN_best_methods(
        self, label: str
    ) -> tuple[list[list[float]], list[str]]:
        return get_polyhedron_coordinates_labels(
            self.CN_connections_by_best_methods, label
        )

    @ensure_connections
    def plot_polyhedron(
        self, site_label, show_labels=True, is_displayed=False, output_dir=None
    ) -> None:
        """
        Plots a polyhedron structure and optionally saves it.

        Args:
            site_label (str): Central site label for the polyhedron.
            show_labels (bool, optional): Whether to display vertex labels. Defaults to True.
            is_displayed (bool, optional): Display plot interactively. Defaults to False.
            output_dir (str, optional): Directory to save the plot. Defaults to None.
        """
        coords, vertex_labels = get_polyhedron_coordinates_labels(
            self.CN_connections_by_best_methods, site_label
        )
        polyhedron.plot(
            coords,
            vertex_labels,
            self.file_path,
            self.formula,
            show_labels,
            is_displayed,
            output_dir,
        )
