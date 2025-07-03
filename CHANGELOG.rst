=============
Release Notes
=============

.. current developments

1.1.1
=====

**Fixed:**

* Bump verison 1.1.0 to 1.1.1 sincedone.1.1.0 was already uploaded before to PyPI.


1.1.0
=====

**Added:**

* Use tests.txt, modify folder name from doc to docs.
* Add Bala to contributor's list in index.rst.

**Fixed:**

* Use vectorization for computing connections.


1.0.9
=====

**Added:**

* Add unit tests for refined CIF radius for binary and ternary.
* Add ``bobleesj.utils`` to the ``pip.txt`` and ``conda.txt`` requirement files.
* Add ``deepdiff`` to ``test.txt``.
* Use bobleesj.utils to source CIF radius for all elements.
* Relocate PCD .cif files that have no atomic site/label while preprocessing each .cif file.
* Standarlize `cifkit` using `scikit-package` v0.1.0 including `docformatter`, `prettier`, and `codespell` for code formatting and linting.
* Include an option to compute coordination metrics when CIF and CifEnsemble are initialized.
* Implement compute_CN to separate computing CN related metrics, separated from computing connections.
* Return objective function value after finding refined CIF radius.

**Changed:**

* Source Mendeleeve values from bobleesj.utils.

**Fixed:**

* Catch error for the polyhedron when the volume cannot be calculated due to flat surface.
* Fix all local unit tests to pass with compute_CN() method.
* Generate 5 by 5 by 5 supercell by default in instead of 3 by 3 by 3 to handle the case where a bigger supercell is required to accurate to determine the correct shortest distances from each site.
* Fix Jupyter CIF doc rendering problem with PCD demo file.
* Set line-length max to 90 instead of 79.
* Fix error in polyhedron volume calculation for CN=5 and other polyhedrons with central atom on the same plane with equatorial atoms.

**Removed:**

* Remove hard coded data for CIF and Pauling CN12 radius values. Retrieve them from bobleesj.utils.


1.0.6
=====

**Added:**

* Publish ``cikift`` to Journal of Open Source Software (JOSS) with DOI: `10.21105/joss.05923 <https://doi.org/10.21105/joss.07205>`_.

1.0.5
=====

**Added:**

* Add docstrings to ``Cif`` and ``CifEnsembleo`` classes.
* Add support for ICSD, COD, MP, CCDC files.
* Use GitHub Actions to deploy to PyPI and update ``CHANGELOG.rst``.

1.0.3
=====

**Added:**

* Support .cif file formats of PCD, COD, Materials Studio, ICSD.

**Fixed:**

* Update `U` Pauling CN12 value from 1.51 to 1.516.

1.0.2
=====

**Added:**

* Initializing progress statement for `CifEnsemble` to enhance user experience.
* Print option for `compute_connections` in CifEnsemble.
* Preprocessing option for `CifEnsemble` to handle input data more flexibly.

**Fixed:**

* Error computing polyhedron metrics: index 4 is out of bounds for axis 0 with size 4.
* Warning for using categorical units to plot a list of strings for histogram generation.
* Misclassification issue during preprocessing: do not move to 'others' folder if elements do not belong to Mendeleev table.
