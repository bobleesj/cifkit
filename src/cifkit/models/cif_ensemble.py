import logging
from collections import Counter

from cifkit import Cif
from cifkit.figures.histogram import plot_histogram
from cifkit.preprocessors.error import move_files_based_on_errors
from cifkit.utils.cif_editor import edit_cif_file_based_on_db
from cifkit.utils.folder import copy_files, get_file_paths, move_files
from cifkit.utils.log_messages import CifEnsembleLog


class CifEnsemble:
    def __init__(
        self,
        cif_dir_path: str,
        add_nested_files=False,
        preprocess=True,
        logging_enabled=False,
        supercell_size=3,
        compute_CN=False,
    ) -> None:
        """Initialize a CifEnsemble object, containing a collection of
        Cif objects.

        Parameters
        ----------
        cif_dir_path : str
            Path to the folder path containing .cif file(s).
        add_nested_files : bool, optional
            Option to include .cif files contained in sub-directories within cif_dir_path
            , by default False
        preprocess : bool, optional
            Option to edit .cif files before initializing each into a Cif object,
            by default True. Preprocess modifies atomic site labels in
            atom_site_label. Some site labels may contain a comma or a symbol like M
            due to atomic mixing. It reformats each atom_site_label so it can be
            parsed into an element type matching atom_site_type_symbol. For PCD
            databases, addresses in publ_author_address often have an incorrect
            format requiring manual modifications. It also relocates any ill-formatted
            files, such as those with duplicate labels in atom_site_label, missing
            fractional coordinates, or files requiring supercell generation.
        compute_CN : bool, optional
            Option to compute coordination numbers for each Cif object.
        logging_enabled : bool, optional
            Option to log while pre-processing Cif objects, by default False

        Attributes
        ----------
        dir_path: str
            The path to the folder containing .cif files
        file_paths: list[str]
            The pist of file paths to .cif files
        cifs: list[Cif]
            The list of Cif objects
        file_count: int
            The number of .cif files in the folder
        logging_enabled: bool
            The option to log while pre-processing Cif objects
        """

        # Process each file, handling exceptions that may occur
        self.logging_enabled = logging_enabled
        file_paths = get_file_paths(cif_dir_path, add_nested_files=add_nested_files)
        self.dir_path = cif_dir_path

        if preprocess:
            self._log_info(CifEnsembleLog.PREPROCESSING.value)
            for file_path in file_paths:
                edit_cif_file_based_on_db(file_path)
            # Move ill-formatted files after pre-processing
            move_files_based_on_errors(cif_dir_path, file_paths)

        # Initialize new files after ill-formatted files are moved
        self.file_paths = get_file_paths(cif_dir_path, add_nested_files=add_nested_files)
        self.file_count = len(self.file_paths)
        print(f"Initializing {self.file_count} Cif objects...")

        if logging_enabled:
            self.cifs = [
                Cif(
                    file_path,
                    is_formatted=True,
                    logging_enabled=True,
                    supercell_size=supercell_size,
                    compute_CN=compute_CN,
                )
                for file_path in self.file_paths
            ]
        else:
            self.cifs = [
                Cif(
                    file_path,
                    is_formatted=True,
                    supercell_size=supercell_size,
                    compute_CN=compute_CN,
                )
                for file_path in self.file_paths
            ]
        print("Finished initialization!")

    def _log_info(self, message):
        """Log a formatted message if logging is enabled."""
        if self.logging_enabled:
            formatted_message = message.format(dir_path=self.dir_path)
            logging.info(formatted_message)

    def _get_unique_property_values(self, property_name: str):
        """Return unique values for a given property from cifs."""
        return set(
            getattr(cif, property_name)
            for cif in self.cifs
            if hasattr(cif, property_name)
        )

    @property
    def unique_formulas(self) -> set[str]:
        """Get unique formulas from all .cif files in the folder.

        Returns
        -------
        set[str]
            unique formulas

        Examples
        --------
        >>> cif_ensemble.unique_formulas
        {"EuIr2Ge2", "CeRu2Ge2", "LaRu2Ge2", "Mo"}
        """
        return self._get_unique_property_values("formula")

    @property
    def unique_structures(self) -> set[str]:
        """Get unique structures from all .cif files in the folder.

        Examples
        --------
        >>> cif_ensemble.unique_structures
        {"CeAl2Ga2", "W"}
        """
        return self._get_unique_property_values("structure")

    @property
    def unique_tags(self) -> set[str]:
        """Get unique formulas from all .cif files in the folder.

        Examples
        --------
        >>> cif_ensemble.unique_tags
        {"hex", "rt", "rt_hex", ""}
        """
        return self._get_unique_property_values("tag")

    @property
    def unique_space_group_names(self) -> set[str]:
        """Get unique space groups from all .cif files in the folder.

        Examples
        --------
        >>> cif_ensemble.unique_space_group_names
        {"I4/mmm", "Im-3m"}
        """
        return self._get_unique_property_values("space_group_name")

    @property
    def unique_space_group_numbers(self) -> set[str]:
        """Get unique space groups from all .cif files in the folder.

        Examples
        --------
        >>> cif_ensemble.unique_space_group_numbers
        {139, 229}
        """
        return self._get_unique_property_values("space_group_number")

    @property
    def unique_site_mixing_types(self) -> set[int]:
        """Get unique site mixing types from all .cif files in the
        folder.

        Examples
        --------
        >>> cif_ensemble.unique_site_mixing_types
        {"deficiency_without_atomic_mixing", "full_occupancy"}
        """
        return self._get_unique_property_values("site_mixing_type")

    @property
    def unique_composition_types(self) -> set[int]:
        """Get unique composition types from all .cif files in the
        folder.

        Examples
        --------
        >>> cif_ensemble.unique_composition_types
        {1, 3}
        """
        return self._get_unique_property_values("composition_type")

    def _get_unique_property_values_from_set(self, property_name: str):
        unique_values = set()
        for cif in self.cifs:
            unique_values.update(getattr(cif, property_name))
        return unique_values

    @property
    def unique_elements(self) -> set[str]:
        """Get unique elements from all .cif files in the folder.

        Examples
        --------
        >>> cif_ensemble.unique_elements_stats
        {
            "Ce": 1,
            "Eu": 1,
            "Ge": 3,
            "Ir": 1,
            "La": 1,
            "Mo": 3,
            "Ru": 2,
        }
        """

        return self._get_unique_property_values_from_set("unique_elements")

    @property
    def CN_unique_values_by_min_dist_method(self) -> set[str]:
        """

        Returns
        -------
        set[str]
            Unique coordination number values by minimum distance method from all .cif
            files.
        """
        return self._get_unique_property_values_from_set(
            "CN_unique_values_by_min_dist_method"
        )

    @property
    def CN_unique_values_by_best_methods(self) -> set[str]:
        """

        Returns
        -------
        set[str]
            Unique coordination number by best methods from all .cif files.
        """
        return self._get_unique_property_values_from_set(
            "CN_unique_values_by_best_methods"
        )

    def _attribute_stats(self, attribute_name, transform=None):
        """Helper method to compute the count of each unique value of a
        given attribute across all Cif objects."""
        values = [
            (
                transform(getattr(cif, attribute_name))
                if transform
                else getattr(cif, attribute_name)
            )
            for cif in self.cifs
            if hasattr(cif, attribute_name)
        ]
        # Flatten the list if the attribute is a set of elements
        if isinstance(values[0], set):
            values = [elem for sublist in values for elem in sublist]
        return dict(Counter(values))

    @property
    def structure_stats(self) -> dict[str, int]:
        return self._attribute_stats("structure")

    @property
    def formula_stats(self) -> dict[str, int]:
        return self._attribute_stats("formula")

    @property
    def tag_stats(self) -> dict[str, int]:
        return self._attribute_stats("tag")

    @property
    def space_group_number_stats(self) -> dict[str, int]:
        return self._attribute_stats("space_group_number")

    @property
    def space_group_name_stats(self) -> dict[str, int]:
        return self._attribute_stats("space_group_name")

    @property
    def composition_type_stats(self) -> dict[str, int]:
        return self._attribute_stats("composition_type")

    @property
    def unique_elements_stats(self) -> dict[str, int]:
        return self._attribute_stats("unique_elements")

    @property
    def site_mixing_type_stats(self) -> dict[str, int]:
        return self._attribute_stats("site_mixing_type")

    @property
    def supercell_size_stats(self) -> dict[int, int]:
        return self._attribute_stats("supercell_points", len)

    @property
    def unique_CN_values_by_min_dist_method_stat(
        self,
    ) -> dict[float, int]:
        return self._attribute_stats("CN_unique_values_by_min_dist_method")

    @property
    def unique_CN_values_by_method_methods_stat(
        self,
    ) -> dict[float, int]:
        return self._attribute_stats("CN_unique_values_by_best_methods")

    def _collect_cif_data(self, attribute, transform=None):
        """Generic method to collect data from CIF files based on an
        attribute."""
        collected_data = []
        for cif in self.cifs:
            attr_value = getattr(cif, attribute, None)
            if attr_value is not None:
                if transform:
                    value = transform(attr_value)
                else:
                    value = attr_value
                collected_data.append((cif.file_path, value))
            else:
                print(f"No valid {attribute} for {cif.file_path}")
        return collected_data

    @property
    def minimum_distances(self) -> list[tuple[str, float]]:
        return self._collect_cif_data("shortest_distance")

    @property
    def supercell_atom_counts(self) -> list[tuple[str, int]]:
        return self._collect_cif_data("supercell_atom_count")

    def _filter_by_single_value(self, property_name: str, values: list):
        cif_file_paths = set()
        for cif in self.cifs:
            property_value = getattr(cif, property_name, None)
            if property_value in values:
                cif_file_paths.add(cif.file_path)

        return cif_file_paths

    # With sets
    def _filter_contains_any(self, property_name: str, values: list) -> set[str]:
        cif_file_paths = set()
        for cif in self.cifs:
            property_value: str = getattr(cif, property_name)
            cif.compute_CN()
            if any(val in property_value for val in values):
                cif_file_paths.add(cif.file_path)
        return cif_file_paths

    def _filter_exact_match(self, property_name: str, values: list) -> set[str]:
        cif_file_paths = set()
        for cif in self.cifs:
            property_value: str = getattr(cif, property_name)
            cif.compute_CN()
            if property_value == set(values):
                cif_file_paths.add(cif.file_path)
        return cif_file_paths

    def filter_by_formulas(self, values: list[str]) -> set[str]:
        return self._filter_by_single_value("formula", values)

    def filter_by_structures(self, values: list[str]) -> set[str]:
        return self._filter_by_single_value("structure", values)

    def filter_by_space_group_names(self, values: list[str]) -> set[str]:
        return self._filter_by_single_value("space_group_name", values)

    def filter_by_space_group_numbers(self, values: list[int]) -> set[str]:
        return self._filter_by_single_value("space_group_number", values)

    def filter_by_site_mixing_types(self, values: list[str]) -> set[str]:
        return self._filter_by_single_value("site_mixing_type", values)

    def filter_by_tags(self, values: list[str]) -> set[str]:
        return self._filter_by_single_value("tag", values)

    def filter_by_composition_types(self, values: list[int]) -> set[str]:
        return self._filter_by_single_value("composition_type", values)

    # Filter with setsz
    def filter_by_elements_containing(self, values: list[str]) -> set[str]:
        return self._filter_contains_any("unique_elements", values)

    def filter_by_elements_exact_matching(self, values: list[str]) -> set[str]:
        return self._filter_exact_match("unique_elements", values)

    """
    Filter by CN
    """

    def filter_by_CN_min_dist_method_containing(self, values: list[int]) -> set[str]:
        return self._filter_contains_any("CN_unique_values_by_min_dist_method", values)

    def filter_by_CN_min_dist_method_exact_matching(self, values: list[int]) -> set[str]:
        return self._filter_exact_match("CN_unique_values_by_min_dist_method", values)

    def filter_by_CN_best_methods_containing(self, values: list[int]) -> set[str]:
        return self._filter_contains_any("CN_unique_values_by_best_methods", values)

    def filter_by_CN_best_methods_exact_matching(self, values: list[int]) -> set[str]:
        return self._filter_exact_match("CN_unique_values_by_best_methods", values)

    def _filter_by_range(
        self, property: str, min: float | int, max: float | int
    ) -> set[str]:
        cif_file_paths = set()
        for cif in self.cifs:
            property_value = getattr(cif, property, None)
            if property_value is None:
                continue
            if property_value < min or property_value > max:
                continue
            cif_file_paths.add(cif.file_path)
        return cif_file_paths

    def filter_by_min_distance(
        self, min_distance: float, max_distance: float
    ) -> set[str]:
        return self._filter_by_range("shortest_distance", min_distance, max_distance)

    def filter_by_supercell_count(self, min_count: int, max_count: int) -> set[str]:
        return self._filter_by_range(
            "supercell_atom_count",
            min_count,
            max_count,
        )

    def move_cif_files(self, file_paths: set[str], to_directory_path: str) -> None:
        """Move a set of CIF files to a destination directory.

        Parameters
        ----------
        file_paths : set[str]
            Set of file paths to CIF files.
        to_directory_path : str
            Destination directory path.

        Examples
        --------
        >>> file_paths = {
            "tests/data/cif/ensemble_test/300169.cif",
            "tests/data/cif/ensemble_test/300170.cif",
        }
        >>> dest_dir_path = "tests/data/cif/ensemble_new_dir"
        >>> cif_ensemble_test.move_cif_files(file_paths, dest_dir_path)
        """
        move_files(to_directory_path, list(file_paths))

    def copy_cif_files(self, file_paths: set[str], to_directory_path: str) -> None:
        """Copy a set of CIF files to a destination directory.

        Parameters
        ----------
        file_paths : set[str]
            Set of file paths to CIF files.
        to_directory_path : str
            Destination directory path.

        Examples
        --------
        >>> file_paths = {
            "tests/data/cif/ensemble_test/300169.cif",
            "tests/data/cif/ensemble_test/300170.cif",
        }
        >>> dest_dir_path = "tests/data/cif/ensemble_new_dir"
        >>> cif_ensemble_test.copy_cif_files(file_paths, dest_dir_path)
        """
        copy_files(to_directory_path, list(file_paths))

    # FIXME: refactor this section to maintain DRY principle

    def generate_structure_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'structure' property from CIF
        files.

        This method creates a histogram based on the 'structure' statistics of the CIF
        files. If 'output_dir' is specified, the histogram image (.png) will be saved to
        that directory. If 'output_dir' is not specified, the image will be saved to the
        directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "structure",
            self.structure_stats,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_formula_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'formula' property from CIF
        files.

        This method creates a histogram based on the 'formula' statistics of the CIF
        files. If 'output_dir' is specified, the histogram image (.png) will be saved to
        that directory. If 'output_dir' is not specified, the image will be saved to the
        directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "formula",
            self.formula_stats,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_tag_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'tag' property from CIF files.

        This method creates a histogram based on the 'tag' statistics of the CIF
        files. If 'output_dir' is specified, the histogram image (.png) will be saved to
        that directory. If 'output_dir' is not specified, the image will be saved to the
        directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "tag",
            self.tag_stats,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_space_group_number_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'space_group_number' property
        from CIF files.

        This method creates a histogram based on the 'space_group_number' statistics of
        the CIF files. If 'output_dir' is specified, the histogram image (.png) will be
        saved to that directory. If 'output_dir' is not specified, the image will be saved
        to the directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "space_group_number",
            self.space_group_number_stats,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_space_group_name_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'space_group_name' property from
        CIF files.

        This method creates a histogram based on the 'space_group_name' statistics of
        the CIF files. If 'output_dir' is specified, the histogram image (.png) will be
        saved to that directory. If 'output_dir' is not specified, the image will be saved
        to the directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "space_group_name",
            self.space_group_name_stats,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_supercell_size_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'supercell_count' property from
        CIF files.

        This method creates a histogram based on the 'supercell_count' statistics of
        the CIF files. If 'output_dir' is specified, the histogram image (.png) will be
        saved to that directory. If 'output_dir' is not specified, the image will be saved
        to the directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "supercell_size",
            self.supercell_size_stats,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_elements_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'unique_elements' property from
        CIF files.

        This method creates a histogram based on the 'unique_elements' statistics of
        the CIF files. If 'output_dir' is specified, the histogram image (.png) will be
        saved to that directory. If 'output_dir' is not specified, the image will be saved
        to the directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "elements",
            self.unique_elements_stats,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_CN_by_min_dist_method_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'CN_by_min' property from CIF
        files.

        This method creates a histogram based on the 'CN_by_min' statistics of
        the CIF files. If 'output_dir' is specified, the histogram image (.png) will be
        saved to that directory. If 'output_dir' is not specified, the image will be saved
        to the directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "CN_by_min_dist_method",
            self.unique_CN_values_by_min_dist_method_stat,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_CN_by_best_methods_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'CN_by_best_methods' property
        from CIF files.

        This method creates a histogram based on the 'CN_by_best_methods' statistics of
        the CIF files. If 'output_dir' is specified, the histogram image (.png) will be
        saved to that directory. If 'output_dir' is not specified, the image will be saved
        to the directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "CN_by_best_methods",
            self.unique_CN_values_by_method_methods_stat,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_composition_type_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'composition_type' property from
        CIF files.

        This method creates a histogram based on the 'composition_type' statistics of
        the CIF files. If 'output_dir' is specified, the histogram image (.png) will be
        saved to that directory. If 'output_dir' is not specified, the image will be saved
        to the directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "composition_type",
            self.composition_type_stats,
            self.dir_path,
            display,
            output_dir,
        )

    def generate_site_mixing_type_histogram(self, display=False, output_dir=None):
        """Generate a histogram of the 'site_mixing_type' property from
        CIF files.

        This method creates a histogram based on the 'site_mixing_type' statistics of
        the CIF files. If 'output_dir' is specified, the histogram image (.png) will be
        saved to that directory. If 'output_dir' is not specified, the image will be saved
        to the directory specified by 'self.dir_path'.

        Parameters
        ----------
        display : bool, optional
            If True, the plot is displayed using plt.show(). Default is False.
        output_dir : str, optional
            The directory path where the histogram should be saved. If None,
            the histogram is saved in the directory defined by 'self.dir_path'.
        """
        plot_histogram(
            "site_mixing_type",
            self.site_mixing_type_stats,
            self.dir_path,
            display,
            output_dir,
        )
