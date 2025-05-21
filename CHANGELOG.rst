=============
Release Notes
=============

.. current developments

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
