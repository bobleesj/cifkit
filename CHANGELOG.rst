=============
Release Notes
=============

.. current developments

1.0.18
=====

**Added:**

* 1

**Changed:**

* 2

**Deprecated:**

* 3


1.0.17
=====

**Added:**

* 1

**Changed:**

* 2


1.0.16
=====

**Added:**

* 2
* 1


1.0.15
=====

**Added:**

* 2
* 1


1.0.14
=====

**Added:**

* 1

**Changed:**

* 2

**Removed:**

* 4


1.0.13
=====

**Added:**

* 1

**Changed:**

* 2

**Deprecated:**

* 3


1.0.12
=====

**Added:**

* 1

**Changed:**

* 2


refs/tags/1.0.11
=====

**Added:**

* Test
* addeed 1

**Changed:**

* Test3
* changed 1
* changed 2


1.0.8
=====

**Added:**

* Test 1

**Fixed:**

* News CI bug with existing news *rst files

**Removed:**

* mypy.ini file


1.0.7
=====

**Added:**

* Test 1

**Fixed:**

* News CI bug with existing news *rst files

**Removed:**

* mypy.ini file



## [1.0.4] - 2024-09-03

### Fixed

- do not print atom site info during Cif init

## [1.0.3] - 2024-09-03

### Added

- support .cif file formats of PCD, COD, Materials Studio, ICSD

### Fixed

- update `U` Pauling CN12 value from 1.51 to 1.516

## [1.0.2] - 2024-07-09

### Added

- initializing progress statement for `CifEnsemble` to enhance user experience (https://github.com/bobleesj/cifkit/issues/12)
- print option for `compute_connections` in CifEnsemble (https://github.com/bobleesj/cifkit/issues/13)
- preprocessing option for `CifEnsemble` to handle input data more flexibly (https://github.com/bobleesj/cifkit/issues/15)

### Fixed

- error computing polyhedron metrics: index 4 is out of bounds for axis 0 with size 4 (https://github.com/bobleesj/cifkit/issues/10)
- warning for using categorical units to plot a list of strings for histogram generation (https://github.com/bobleesj/cifkit/issues/11)
- misclassification issue during preprocessing: do not move to 'others' folder if elements do not belong to Mendeleev table (https://github.com/bobleesj/cifkit/issues/14)

## [1.0.1] - 2024-07-05

### Fixed

- error computing polyhedron metrics: index 4 is out of bounds (https://github.com/bobleesj/cifkit/issues/10)

## [1.0.0] - 2024-07-04

### Added

- issue and pull request templates.

### Fixed

- duplicate connected points in connections with atomic mixing (https://github.com/bobleesj/cifkit/issues/7)
