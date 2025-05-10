=============
Release Notes
=============

.. current developments

1.0.8
=====

**Added:**

* Standarlize `cifkit` using `scikit-package` v0.1.0 including `docformatter`, `prettier`, and `codespell` for code formatting and linting.
* Relocate PCD .cif files that have no atomic site/label while preprocessing each .cif file.


1.0.6
=====

**Added:**

* cifkit accepted to JOSS


1.0.5
=====

**Added:**

* pre-commit hook for each pull request
* automated PyPI
* Core docstrings to Cif and CifEnsembleo classes
* CifEnsemble support for ICSD, COD, MP files
* Support CCDC CIF files
* Use GitHub Actions to deploy to PyPI and update CHANGELOG.rst

**Fixed:**

* Simpler issue templates used in Billinge Group
* Preprocess .cif files in CifEnsemble before initializing into CIF objects

**Removed:**

* Support for click module



1.0.4
=====

**Fixed:**

* do not print atom site info during Cif init

1.0.3
=====

**Added:**

* support .cif file formats of PCD, COD, Materials Studio, ICSD

**Fixed:**

* update `U` Pauling CN12 value from 1.51 to 1.516


1.0.2
=====

**Added:**

* initializing progress statement for `CifEnsemble` to enhance user experience (https://github.com/bobleesj/cifkit/issues/12)
* print option for `compute_connections` in CifEnsemble (https://github.com/bobleesj/cifkit/issues/13)
* preprocessing option for `CifEnsemble` to handle input data more flexibly (https://github.com/bobleesj/cifkit/issues/15)

**Fixed:**

* error computing polyhedron metrics: index 4 is out of bounds for axis 0 with size 4 (https://github.com/bobleesj/cifkit/issues/10)
* warning for using categorical units to plot a list of strings for histogram generation (https://github.com/bobleesj/cifkit/issues/11)
* misclassification issue during preprocessing: do not move to 'others' folder if elements do not belong to Mendeleev table (https://github.com/bobleesj/cifkit/issues/14)


1.0.1
=====

**Fixed:**

* error computing polyhedron metrics: index 4 is out of bounds (https://github.com/bobleesj/cifkit/issues/10)


1.0.0
=====

**Added:**

* issue and pull request templates.

### Fixed

* duplicate connected points in connections with atomic mixing (https://github.com/bobleesj/cifkit/issues/7)
