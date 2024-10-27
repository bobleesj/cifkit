---
title: "cifkit: A user-friendly Python package for high-throughput CIF analysis"
tags:
  - Python
  - CIF
  - crystallography
  - materials science
  - solid state chemistry
  - crystal structure
  - machine learning

authors:
  - name: Sangjoon Lee
    orcid: 0000-0002-2367-3932
    corresponding: true
    affiliation: 1
  - name: Anton O. Oliynyk
  - orcid: 0000-0003-0732-7340
    affiliation: "2, 3"
affiliations:
  - name:
      Department of Applied Physics and Applied Mathematics, Columbia
      University, New York, NY 10027, USA
    index: 1
  - name:
      Department of Chemistry, Hunter College, City University of New York, New
      York, NY 10065, USA
    index: 2
  - name:
      Ph.D. Program in Chemistry, The Graduate Center of the City University of
      New York, New York, NY 10016, USA
    index: 3
date: 29 August 2024
bibliography: paper.bib
---

# Summary

`cifkit` provides higher-level utility functions and variables from .cif files,
which are standard file formats for storing crystallographic data such as atomic
fractional coordinates, symmetry operations, and unit cell dimensions. `cifkit`
serves as an engine for building Python applications that automate crystal
structure analysis, enabling the extraction of physics-based information crucial
for understanding geometric configurations and identifying irregularities.
`cifkit` also offers various tools for determining coordination numbers,
plotting coordination geometry-based polyhedron from each site, calculating bond
fractions, moving and copying .cif files based on a set of attributes, and
determining atomic mixing information.

# Statement of need

In solid state chemistry and materials science, the Crystallographic Information
File (CIF) [@hall_crystallographic_1991] is the predominant file format used to
store and distribute crystal structure information. There are open-source Python
packages that read, edit, and create CIF files. Python Materials Genomics
(pymatgen) [@ong_python_2013] offers functionalities beyond the aforementioned
features, such as generating electronic structure properties and phase diagrams.
Similarly, the Atomic Simulation Environment (ASE) [@larsen_atomic_2017]
provides a suite of powerful tools for generating and running atomistic
simulations.

`cifkit` distinguishes itself from existing libraries by offering higher-level
functions and variables that enable users to perform complex tasks efficiently
with a few lines of code. `cifkit` not only facilitates the visualization of
coordination geometry from each site but also extracts physics-based features
like volume and packing efficiency, crucial for structural analysis in ML tasks.
Additionally, it extracts atomic mixing information at the bond pair level—tasks
that would otherwise require extensive manual effort using GUI-based tools like
VESTA, Diamond, and CrystalMaker, due to the lack of readily available
higher-level functions.

Further enhancing its utility, cifkit excels in sorting, preprocessing, and
understanding the distribution of underlying CIF files. Common issues in CIF
files from databases, such as incorrect loop values and missing fractional
coordinates, are systematically addressed as cifkit standardizes and filters out
ill-formatted files. It also preprocesses atomic site labels, transforming
labels such as 'M1' to 'Fe1' in files with atomic mixing. Beyond error
correction, cifkit provides functionalities to copy, move, and sort files based
on attributes like coordination numbers, space groups, unit cells, and shortest
distances. It also excels in visualizing and cataloging CIF files, organizing
them based on supercell size, tags, coordination numbers, elements, and atomic
mixing, among other parameters.

# Examples

cifkit is designed to minmize the reliance on API documentation for useres with
limtied programming experience. By simplifying user interactions while
maintaining robust functionality, cifkit enables a broader range of scientists
to leverage computational tools for complex tasks such as extracting descriptors
for geometry-based polyhedra from each atomic site. The full installation
process can be executed via a Jupyter notebook, which is distributed through the
Google Colab URL provided in the official documentation.

```python
from cifkit import Cif, Example

# Initalize with the .cif file path
cif = Cif(Example.Er10Co9In20_file_path)
cif.formula
```

To extract information from a set of .cif files:

```python
from cifkit import CifEnsemble, Example

# Initalize with the folder path containing .cif files
ensemble = CifEnsemble(Example.ErCoIn_big_folder_path)
ensemble.unique_formulas
ensemble.unique_structures
ensemble.unique_elements

# Determine shortest pair distance per .cif file
ensemble.minimum_distances

# Filter .cif by formula
ensemble.filter_by_formulas(["LaRu2Ge2"])

# Filter .cif by space group name
ensemble.filter_by_space_group_names("Im-3m")
```

# Applications 

`cifkit` serves as a core package for building applications used by academic and
national laboratories for crystal structural analysis and machine learning
studies. CIF Bond Analyzer (CBA) utilizes `cifkit` to extract coordination
geometry information for newly a discovered phase [@tyvanchuk_crystal_2024]. The
Structure Analysis/Featurizer (SAF) employs `cifkit` to construct and extract
physics-based geometric features for binary and ternary compounds. Furthermore,
geometric features generated with `cifkit` are being incorporated into a
follow-up study on thermoelectric materials [@barua_interpretable_2024],
building upon the compositional properties explored in [@lee_machine_2024].

# Testing and documentation

97 percent of the code is covered according to Codecov. The documentation is
provided at https://bobleesj.github.io/cifkit.

# Acknowledgement

We acknowledge the initial testing done by Nishant Yadav, Siddha Sankalpa Sethi,
and Arnab Dutta from the Indian Institute of Technology, Kharagpur. We also
thank Emil Jaffal, Danila Shiryaev, and Alex Vtorov from CUNY Hunter College for
testing. We acknowledge Fabian Zills for his recommendations on Python tooling.

# References
