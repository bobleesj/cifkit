import logging
import os

from bobleesj.utils.sources import radius

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
from cifkit.data.radius_handler import compute_radius_sum, get_radius_values_per_element
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

# Utility
from cifkit.utils.log_messages import CifLog


def ensure_connections(func):
    """For accessing lazy properties and methods, compute
    connections."""

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
        self,
        file_path: str,
        is_formatted=False,
        logging_enabled=False,
        supercell_size=3,
        compute_CN=False,
    ) -> None:
        """Initialize an object from a .cif file.

        Parameters
        ----------
        file_path : str
            Path to the .cif file.
        is_formatted : bool, default
            If False, preprocess the .cif file to ensure compatibility with the
            gemmi library.
        logging_enabled : bool, default False
            Enables detailed logging during initialization and for distance
            calculations.
        supercell_size : int, default 3
            Size of the supercell to be generated. Default is 3.
            Method 1 - No shifts
            Method 2 - ±1 shifts  (3x3x3 of the unit cell)
            Method 3 - ±2 shifts (5×5×5 of the unit cell)
        compute_CN : bool, default False
            Option to compute CN related metrics for each Cif object.

        Attributes
        ----------
        file_path : str
            Path to the CIF file from which data is loaded.
        logging_enabled : bool
            Enables detailed logging for initialization and distance
            alculations if set to True.
        file_name : str
            Base name of the CIF file, extracted from `file_path`.
        file_name_without_ext : str
            File name without its extension, useful for referencing or
            generating derivative files.
        db_source : str
            Source database (e.g., ICSD, MP, CCDC, PCD) from which the CIF file
            originates, determined at runtime.
        unitcell_lengths : list[float]
            List of unit cell lengths for the crystal structure, typically in
            Angstroms.
        unitcell_angles : list[float]
            List of unit cell angles in radians, ordered by alpha, beta, gamma.
        site_labels : list[str]
            Lists all unique atomic site labels.
        unique_elements : set[str]
            Set of unique chemical elements present in the CIF file.
        atom_site_info : dict[str, any]
            Dictionary containing detailed information about each atomic site
            including element, site occupancy,
            fractional coordinates, symmetry, and multiplicity.
        composition_type : int
            Number of unique elements present in the .cif file, e.g., 1 for
            unary, 2 for binary, etc.
        tag : str
            Additional tag associated with the CIF data, parsed from the third
            line of PCD .cif files.
        bond_pairs : set[tuple[str, str]]
            Set of tuples representing bonded pairs of elements.
        site_label_pairs : set[tuple[str, str]]
            Set of tuples representing pairs of atomic site labels.
        bond_pairs_sorted_by_mendeleev : set[tuple[str, str]]
            Set of bonded pairs sorted according to Mendeleev Numbers.
        site_label_pairs_sorted_by_mendeleev : set[tuple[str, str]]
            Set of site label pairs sorted by Mendeleev Numbers.
        site_mixing_type : str
            Descriptor of the mixing type, categorized into four types:
            Full occupancy is assigned when a single atomic site occupies
            the fractional coordinate with an occupancy value of 1.
            Full occupancy with mixing is assigned when multiple atomic sites
            collectively occupy the fractional coordinate to a sum of 1.
            Deficiency without mixing is assigned when a single atomic site occupying
            the fractional coordinate with a sum less than 1.
            Deficiency with atomic mixing is assigned when multiple atomic sites occupy
            the fractional coordinate with a sum less than 1.
        is_radius_data_available : bool
            Indicates whether Pauling and CIF atomic radii are available for
            all elements in the .cif file.
        mixing_info_per_label_pair : dict
            Dictionary mapping pairs of labels to their mixing information.
        mixing_info_per_label_pair_sorted_by_mendeleev : dict
            Same as `mixing_info_per_label_pair`, but sorted according to
            Mendeleev numbers.
        unitcell_points : list[list[tuple[float, float, float, str]]]
            List of points defining the unit cell; each point contains
            fractional coordinates and a site label.
        supercell_points : list[list[tuple[float, float, float, str]]]
            List of points defining the supercell of the cell For each .cif file,
            a unit cell is generated by applying the symmetry operations.
            A supercell is generated by applying ±1 shifts from the unit cell.
        unitcell_atom_count : int
            Total count of atoms within the unit cell.
        supercell_atom_count : int
            Total count of atoms within the generated supercell
            incorporating ±1, ±1, ±1 translations.
        connections : None or dict
            Initially None, intended to store connection data related to
            the crystal structure. Connections are computed lazily and are
            only calculated when first needed by a method or property requiring them.
        """

        self.file_path = file_path
        self.logging_enabled = logging_enabled
        # Initialize the Cif object with the file path.
        self.file_name = os.path.basename(file_path)
        self.file_name_without_ext = os.path.splitext(self.file_name)[0]
        self.db_source = get_cif_db_source(self.file_path)
        # Private attribute to store connections
        self.connections = None
        self._shortest_pair_distance = None
        # Pre-process if .cif has not been formatted
        if not is_formatted:
            self._preprocess()
        self._load_data(supercell_size)
        if compute_CN:
            self.compute_CN()

    def _log_info(self, message):
        """Log a formatted message if logging is enabled."""
        if self.logging_enabled:
            formatted_message = message.format(
                file_path=self.file_path, file_name=self.file_name
            )
            logging.info(formatted_message)

    def _preprocess(self):
        """Preprocess each .cif file before initializng and separate
        files with error."""
        self._log_info(CifLog.PREPROCESSING.value)
        edit_cif_file_based_on_db(self.file_path)

    def _load_data(self, supercell_size):
        """Load data from the .cif file and extract attributes."""
        self._log_info(CifLog.LOADING_DATA.value)
        self._block = get_cif_block(self.file_path)
        self._parse_cif_data()
        self._generate_supercell(supercell_size)

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
        self.site_label_pairs_sorted_by_mendeleev = get_pairs_sorted_by_mendeleev(
            self.site_labels
        )
        self.site_mixing_type = get_site_mixing_type(
            self.site_labels, self.atom_site_info
        )
        self.is_radius_data_available = radius.are_available(list(self.unique_elements))
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

    def _generate_supercell(self, supercell_size) -> None:
        """Generate supercell information based on the unit cell data.

        This method calculates the supercell points and atom counts based
        on the unit cell data. It uses the `get_supercell_points` and
        `get_cell_atom_count` functions to perform the calculations.
        """
        # Method implementation goes here
        self.unitcell_points = get_supercell_points(self._block, 1)
        self.supercell_points = get_supercell_points(self._block, supercell_size)
        self.unitcell_atom_count = get_cell_atom_count(self.unitcell_points)
        self.supercell_atom_count = get_cell_atom_count(self.supercell_points)

    def compute_connections(self, cutoff_radius=10.0) -> None:
        """Compute onnection network, shortest distances, bond counts,
        and coordination numbers (CN). These prperties are lazily loaded
        to avoid unnecessary computation during the initialization and
        pre-processing step.

        Parameters
        ----------
        cutoff_radius : float, default=10.0
            The distance threshold in Angstroms used to consider two atoms as connected.
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
        self._connections_flattened = flat_site_connections(self.connections)
        self._shortest_distance = get_shortest_distance(self.connections)
        # Shortest distance per bond pair
        self._shortest_bond_pair_distance = get_shortest_distance_per_bond_pair(
            self.connections_flattened
        )
        # Shortest distance per site
        self._shortest_site_pair_distance = get_shortest_distance_per_site(
            self.connections
        )
        # Parse individual radii per element
        self._radius_values = get_radius_values_per_element(
            list(self.unique_elements), self.shortest_bond_pair_distance
        )
        self._radius_sum = compute_radius_sum(
            self.radius_values, self.is_radius_data_available
        )

    def compute_CN(self) -> None:
        """Compute onnection network, shortest distances, bond counts,
        and coordination numbers (CN). These prperties are lazily loaded
        to avoid unnecessary computation during the initialization and
        pre-processing step.

        Parameters
        ----------
        cutoff_radius : float, default=10.0
            The distance threshold in Angstroms used to consider two atoms as connected.
        """

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
        self._CN_connections_by_best_methods = get_CN_connections_by_best_methods(
            self.CN_best_methods, self.connections
        )

        # Get CN connections by the best methods
        self._CN_connections_by_min_dist_method = get_CN_connections_by_min_dist_method(
            self.CN_max_gap_per_site, self.connections
        )
        # Bond counts
        self._CN_bond_count_by_min_dist_method = get_bond_counts(
            self.unique_elements, self.CN_connections_by_min_dist_method
        )
        self._CN_bond_count_by_best_methods = get_bond_counts(
            self.unique_elements, self.CN_connections_by_best_methods
        )

        # Bond counts sorted by mendeleev
        self._CN_bond_count_by_min_dist_method_sorted_by_mendeleev = get_bond_counts(
            self.unique_elements,
            self.CN_connections_by_min_dist_method,
            sorted_by_mendeleev=True,
        )
        self._CN_bond_count_by_best_methods_sorted_by_mendeleev = get_bond_counts(
            self.unique_elements,
            self.CN_connections_by_best_methods,
            sorted_by_mendeleev=True,
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
            get_bond_fractions(self.CN_bond_count_by_min_dist_method_sorted_by_mendeleev)
        )

        self._CN_bond_fractions_by_best_methods_sorted_by_mendeleev = get_bond_fractions(
            self.CN_bond_count_by_best_methods_sorted_by_mendeleev
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

        self._CN_avg_by_best_methods = compute_avg_CN(self.CN_connections_by_best_methods)

        # Max CN
        self._CN_max_by_min_dist_method = max(self.CN_unique_values_by_min_dist_method)
        self._CN_max_by_best_methods = max(self.CN_unique_values_by_best_methods)
        # Min CN
        self._CN_min_by_min_dist_method = min(self.CN_unique_values_by_min_dist_method)
        self._CN_min_by_best_methods = min(self.CN_unique_values_by_best_methods)

    @property
    @ensure_connections
    def shortest_distance(self):
        """Lazily retrieve the shortest atomic distance within the
        crystal structure. This property is lazily loaded and ensures
        all necessary connections are computed beforehand using the
        `@ensure_connections` decorator. The computation calculates the
        minimum distance between any pairs of atoms based on the
        connection data.

        Returns
        -------
        float
            The shortest distance between any two connected atoms in the
            crystal structure, in Angstroms.
        """
        return self._shortest_distance

    @property
    @ensure_connections
    def connections_flattened(self):
        """Transform site connections into a sorted list of tuples, each
        containing a pair of alphabetically sorted element symbols and
        the distance between them.

        Returns
        -------
        list[tuple[tuple[str, str], float]]
            A sorted list of tuples, each containing a pair of alphabetically
            sorted element symbols and the distance between them.

        Examples
        --------
        >>> cif = Cif("path/to/cif/file.cif"))
        >>> cif.connections_flattened
        [(("In", "Rh"), 2.697), (("In", "Rh"), 2.697)]
        """
        return self._connections_flattened

    @property
    @ensure_connections
    def shortest_bond_pair_distance(self):
        """Determine the minimum distance for all possible unique pair
        of elements. This property uses lazily loaded connections to
        compute the distance if they are not already available.

        Returns
        -------
        dict[tuple[str, str], float]
            Dictionary where each key is a tuple of element symbols and the float value
            is the distance between pair of elements in Angstroms.

        Examples
        --------
        >>> cif.shortest_bond_pair_distance
        {
            ("In", "In"): 3.244,
            ("In", "Rh"): 2.697,
            ("In", "U"): 3.21,
            ("Rh", "Rh"): 3.881,
            ("Rh", "U"): 2.983,
            ("U", "U"): 3.881,
        }
        """
        return self._shortest_bond_pair_distance

    @property
    @ensure_connections
    def shortest_site_pair_distance(self):
        """Retrieves the shortest distance from each unique atomic site
        in the crystal structure. This property uses lazily loaded
        connections to compute these distances if they are not already
        available.

        Returns
        -------
        dict[str, tuple[str, float]]
             dictionary where each key is an atomic label and the value is a
             tuple containing the label of the closest atomic site and the
             shortest distance to it in Angstroms

        Examples
        --------
        >>> cif.shortest_site_pair_distance
        {
            "In1": ("Rh2", 2.697),
            "Rh1": ("In1", 2.852),
            "Rh2": ("In1", 2.697),
            "U1": ("Rh1", 2.984),
        }
        """
        return self._shortest_site_pair_distance

    @property
    @ensure_connections
    def radius_values(self):
        """Retrieve CIF radius, CIF_refined radius, and Pauling C12
        radius for each element.

        This property uses lazy loading to compute or retrieve radius values only when
        needed, optimizing performance. The CIF radius and Pauling C12 radius are standard
        values sourced from `data/radius.py` for each element. In contrast, the
        CIF_refined radius is calculated based on bonding distances to ensure accuracy
        across different environments.

        - **CIF_radius**: The standard radius value commonly determined from
        elemental .cif files, the approximate size of an atom within a crystal structure.
        - **CIF_radius_refined**: An optimized radius calculated to ensure that, across
        all bonding pairs, the sum of the two radii in a bonded pair attempts to
        matches the shortest unique observed bond distances. This refinement is designed
        to improve packing efficiency within a coordination polyhedron.
        - **Pauling_radius_CN12**: The Pauling radius of the element, calculated with a
        coordination number (CN) of 12, providing a basis for comparison with other radius
        types.

        Returns
        -------
        dict[str, dict[str, float]]
            A dictionary where each key is an atomic label (e.g., "In", "Rh", "U"), and
            the corresponding value is a dictionary with radius information in Angstroms:

            - `CIF_radius` (float): The standard CIF radius.
            - `CIF_radius_refined` (float): The optimized radius based on CIF radius.
            - `Pauling_radius_CN12` (float): The Pauling radius with a coordination
            number of 12, parsed from literature.

        Examples
        --------
        >>> cif.radius_values
        {
            "In": {
                "CIF_radius": 1.624,
                "CIF_radius_refined": 1.328,
                "Pauling_radius_CN12": 1.66,
            },
            "Rh": {
                "CIF_radius": 1.345,
                "CIF_radius_refined": 1.369,
                "Pauling_radius_CN12": 1.342,
            },
            "U": {
                "CIF_radius": 1.377,
                "CIF_radius_refined": 1.614,
                "Pauling_radius_CN12": 1.516,
            },
        }
        """
        return self._radius_values

    @property
    @ensure_connections
    def radius_sum(self):
        """Retrieve the sum of CIF radius, CIF_refined radius, and
        Pauling C12 radius for the shortest bonding pairs of elements.

        Returns
        -------
        dict[str : dict[str:float]]
            Dictionary where each key is a radius type and the value is a dictionary
            with the key being a bond pair of elements and the value being the total
            radius in Angstroms.

        Examples
        --------
        >>> cif.radius_values
        >>>  {
            "CIF_radius_sum": {
                "In-In": 3.248,
                "In-Rh": 2.969,
                "In-U": 3.001,
                "Rh-Rh": 2.69,
                "Rh-U": 2.722,
                "U-U": 2.754,
            },
            "CIF_radius_refined_sum": {
                "In-In": 2.657,
                "In-Rh": 2.697,
                "In-U": 2.943,
                "Rh-Rh": 2.737,
                "Rh-U": 2.983,
                "U-U": 3.229,
            },
            "Pauling_radius_sum": {
                "In-In": 3.32,
                "In-Rh": 3.002,
                "In-U": 3.176,
                "Rh-Rh": 2.684,
                "Rh-U": 2.858,
                "U-U": 3.032,
            },
        }
        """

        return self._radius_sum

    @property
    def CN_max_gap_per_site(self):
        """Determines the maximum gap in coordination number (CN) for
        each atomic site.

        For each atomic site, considers the first 20 nearest neighbors. The distances
        to these neighbors are normalized based on four methods:

        - `dist_by_shortest_dist`: Normalization by the shortest distance from the site.
        - `dist_by_CIF_radius_sum`: Normalization by the sum of CIF radii.
        - `dist_by_CIF_radius_refined_sum`: Normalization by the sum of refined CIF radii.
        - `dist_by_Pauling_radius_sum`: Normalization by the sum of Pauling radii.

        The radius sums are calculated for each element pair involved. For each
        normalization method, the maximum gap is determined as the largest difference
        between consecutive normalized distances (i.e., the difference between the nth
        and (n-1)th neighbors).

        This CN gap provides insight into the bonding relevance for each site.

        Returns
        -------
        dict of dict of dict
            A dictionary where each key represents an atomic site, mapping to another
            dictionary with normalization methods as keys. Each normalization method
            contains a dictionary with:

            - `max_gap` (float): The maximum gap in the normalized distances.
            - `CN` (int): Coordination number based on the normalization method.

        Examples
        --------
        >>> cif.CN_max_gap_per_site
        {
            "In1": {
                "dist_by_shortest_dist": {"max_gap": 0.306, "CN": 14},
                "dist_by_CIF_radius_sum": {"max_gap": 0.39, "CN": 14},
                "dist_by_CIF_radius_refined_sum": {"max_gap": 0.341, "CN": 12},
                "dist_by_Pauling_radius_sum": {"max_gap": 0.398, "CN": 14},
            },
            "U1": {
                "dist_by_shortest_dist": {"max_gap": 0.197, "CN": 11},
                "dist_by_CIF_radius_sum": {"max_gap": 0.312, "CN": 11},
                "dist_by_CIF_radius_refined_sum": {"max_gap": 0.27, "CN": 17},
                "dist_by_Pauling_radius_sum": {"max_gap": 0.256, "CN": 17},
            },
            "Rh1": {
                "dist_by_shortest_dist": {"max_gap": 0.315, "CN": 9},
                "dist_by_CIF_radius_sum": {"max_gap": 0.347, "CN": 9},
                "dist_by_CIF_radius_refined_sum": {"max_gap": 0.418, "CN": 9},
                "dist_by_Pauling_radius_sum": {"max_gap": 0.402, "CN": 9},
            },
            "Rh2": {
                "dist_by_shortest_dist": {"max_gap": 0.31, "CN": 9},
                "dist_by_CIF_radius_sum": {"max_gap": 0.324, "CN": 9},
                "dist_by_CIF_radius_refined_sum": {"max_gap": 0.397, "CN": 9},
                "dist_by_Pauling_radius_sum": {"max_gap": 0.380, "CN": 9},
            },
        }
        """
        return self._CN_max_gap_per_site

    @property
    def CN_best_methods(self):
        """Determines the optimal coordination method for each atomic
        site.

        For each atomic site, the coordination polyhedron is generated for each method
        in `self.CN_max_gap_per_site`. The method with the smallest value of
        `polyhedron_metrics["distance_from_avg_point_to_center"]`, indicating the highest
        symmetry of the polyhedron, is selected as the "best method" among the four
        methods used to determine the CN gap in `self.CN_max_gap_per_site`.

        Returns
        -------
        dict[str, dict[str, float | int | str]]]
            Dictionary where each key represents an atomic site, and the corresponding
            value is a dictionary containing:

            - `volume_of_polyhedron` (float): The volume of the polyhedron surrounding
            the atomic site.
            - `distance_from_avg_point_to_center` (float): The average distance from
            the polyhedron's vertices  to its geometric center, used as a measure of
            symmetry.
            - `number_of_vertices` (int): The number of vertices in the coordination
            polyhedron.
            - `number_of_edges` (int): The number of edges connecting vertices in the
            polyhedron.
            - `number_of_faces` (int): The number of faces in the coordination polyhedron.
            - `shortest_distance_to_face` (float): The shortest distance between the
            atomic site and the nearest face.
            - `shortest_distance_to_edge` (float): The shortest distance between the
            atomic site and the nearest edge.
            - `volume_of_inscribed_sphere` (float): Volume of the largest sphere that can
            it inside the polyhedron.
            - `packing_efficiency` (float): A measure of how efficiently the polyhedron
            is packed around the atomic site.
            - `method_used` (str): The name of the chosen method
            (e.g., `dist_by_shortest_dist`) providing the  highest symmetry based on
            `distance_from_avg_point_to_center`.

        Examples
        --------
        >>> CN_best_methods = cif_URhIn.CN_best_methods
        >>> CN_best_methods["In1"]["number_of_vertices"] == 14
        >>> CN_best_methods["Rh2"]["number_of_vertices"] == 9
        >>> CN_best_methods["In1"]["method_used"] == "dist_by_shortest_dist"
        >>> CN_best_methods["Rh2"]["method_used"] == "dist_by_shortest_dist"
        """
        return self._CN_best_methods

    @property
    def CN_connections_by_best_methods(self):
        return self._CN_connections_by_best_methods

    @property
    def CN_connections_by_min_dist_method(self):
        return self._CN_connections_by_min_dist_method

    """
    Compute avg, min, max, unique for best and min_dist method
    """

    # 1.1 Bond counts
    @property
    def CN_bond_count_by_min_dist_method(self):
        return self._CN_bond_count_by_min_dist_method

    @property
    def CN_bond_count_by_best_methods(self):
        return self._CN_bond_count_by_best_methods

    # 1.2 Bond counts sorted by mendeleev
    @property
    def CN_bond_count_by_min_dist_method_sorted_by_mendeleev(self):
        return self._CN_bond_count_by_min_dist_method_sorted_by_mendeleev

    @property
    def CN_bond_count_by_best_methods_sorted_by_mendeleev(self):
        return self._CN_bond_count_by_best_methods_sorted_by_mendeleev

    # 2.1 Bond fractions
    @property
    def CN_bond_fractions_by_min_dist_method(self):
        return self._CN_bond_fractions_by_min_dist_method

    @property
    def CN_bond_fractions_by_best_methods(self):
        return self._CN_bond_fractions_by_best_methods

    # 2.2. Bond fractions sorted by Mendeleev
    @property
    def CN_bond_fractions_by_min_dist_method_sorted_by_mendeleev(self):
        return self._CN_bond_fractions_by_min_dist_method_sorted_by_mendeleev

    @property
    def CN_bond_fractions_by_best_methods_sorted_by_mendeleev(self):
        return self._CN_bond_fractions_by_best_methods_sorted_by_mendeleev

    # Unique CN
    @property
    def CN_unique_values_by_min_dist_method(self):
        return self._CN_unique_values_by_min_dist_method

    @property
    def CN_unique_values_by_best_methods(self):
        return self._CN_unique_values_by_best_methods

    # Average CN
    @property
    def CN_avg_by_min_dist_method(self):
        return self._CN_avg_by_min_dist_method

    @property
    def CN_avg_by_best_methods(self):
        return self._CN_avg_by_best_methods

    @property
    def CN_max_by_min_dist_method(self):
        return self._CN_max_by_min_dist_method

    @property
    def CN_max_by_best_methods(self):
        return self._CN_max_by_best_methods

    @property
    def CN_min_by_min_dist_method(self):
        return self._CN_min_by_min_dist_method

    @property
    def CN_min_by_best_methods(self):
        return self._CN_min_by_best_methods

    def get_polyhedron_labels_by_CN_min_dist_method(
        self, label: str
    ) -> tuple[list[list[float]], list[str]]:
        return get_polyhedron_coordinates_labels(
            self.CN_connections_by_min_dist_method, label
        )

    def get_polyhedron_labels_by_CN_best_methods(
        self, label: str
    ) -> tuple[list[list[float]], list[str]]:
        return get_polyhedron_coordinates_labels(
            self.CN_connections_by_best_methods, label
        )

    def plot_polyhedron(
        self,
        site_label: str,
        show_labels=True,
        is_displayed=False,
        output_dir=None,
    ) -> None:
        """Function to plot a polyhedron structure and optionally saves
        it.

        Parameters
        ----------
        site_label : str
            Central site label for the polyhedron
        show_labels : bool, optional
            Whether to display vertex labels, by default True
        is_displayed : bool, optional
            Display plot interactively, by default False
        output_dir : str, optional
            Directory to save the plot, by default None
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
