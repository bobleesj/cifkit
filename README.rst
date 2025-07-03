cifkit
======

|PyPI| |Forge| |PythonVersion| |PR|

|CI| |Codecov| |Tracking|

.. |CI| image:: https://github.com/bobleesj/cifkit/actions/workflows/matrix-and-codecov-on-merge-to-main.yml/badge.svg
        :target: https://github.com/bobleesj/cifkit/actions/workflows/matrix-and-codecov-on-merge-to-main.yml

.. |Codecov| image:: https://codecov.io/gh/bobleesj/cifkit/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/bobleesj/cifkit

.. |Forge| image:: https://img.shields.io/conda/vn/conda-forge/cifkit
        :target: https://anaconda.org/conda-forge/cifkit

.. |PR| image:: https://img.shields.io/badge/PR-Welcome-29ab47ff
        :target: https://github.com/bobleesj/cifkit/pulls

.. |PyPI| image:: https://img.shields.io/pypi/v/cifkit
        :target: https://pypi.org/project/cifkit/

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/cifkit
        :target: https://pypi.org/project/cifkit/

.. |Tracking| image:: https://img.shields.io/badge/issue_tracking-github-blue
        :target: https://github.com/bobleesj/cifkit/issues

|Logo light mode| |Logo dark mode|

.. |Logo light mode| image:: docs/source/img/logo-black.png#gh-light-mode-only
.. |Logo dark mode| image:: docs/source/img/logo-color.png#gh-dark-mode-only

``cifkit`` is designed to provide a set of fully-tested utility
functions and variables for handling large datasets, on the order of
tens of thousands, of ``.cif`` files.

Features:
---------

``cifkit`` provides higher-level functions in just a few lines of code.

-  **Coordination geometry** - ``cifkit`` provides functions for
   visualing coordination geometry from each site and extracts
   physics-based features like volume and packing efficiency in each
   polyhedron.
-  **Atomic mixing** - ``cifkit`` extracts atomic mixing information at
   the bond pair level—tasks that would otherwise require extensive
   manual effort using GUI-based tools like VESTA, Diamond, and
   CrystalMaker.
-  **Filter** - ``cifkit`` offers features for preprocessing. It
   systematically addresses common issues in CIF files from databases,
   such as incorrect loop values and missing fractional coordinates, by
   standardizing and filtering out ill-formatted files. It also
   preprocesses atomic site labels, transforming labels such as ‘M1’ to
   ‘Fe1’ in files with atomic mixing.
-  **Sort** - ``cifkit`` allows you to copy, move, and sort ``.cif``
   files based on attributes such as coordination numbers, space groups,
   unit cells, shortest distances, elements, and more.

Example usage 1 - coordination geometry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example below uses ``cifkit`` to visualize the polyhedron generated
from each atomic site based on the coordination number geometry.

.. code:: python

   from cifkit import Cif

   cif = Cif("your_cif_file_path")
   site_labels = cif.site_labels

   # Loop through each site label
   for label in site_labels:
       # Dipslay each polyhedron, .png saved for each label
       cif.plot_polyhedron(label, is_displayed=True)

.. figure:: docs/source/img/ErCoIn-polyhedron.png
   :alt: Polyhedron generation

   Polyhedron generation

Example Usage 2 - sort
~~~~~~~~~~~~~~~~~~~~~~

The following example generates a distribution of structure.

.. code:: python

   from cifkit import CifEnsemble

   ensemble = CifEnsemble("your_folder_path_containing_cif_files")
   ensemble.generate_structure_histogram()

.. figure:: docs/source/img/histogram-structure.png
   :alt: structure distribution

   structure distribution

Basde on your visual histogram above, you can copy and move .cif files
based on specific attributes:

.. code:: python

   # Return file paths matching structures either Co1.75Ge or CoIn2
   ensemble.filter_by_structures(["Co1.75Ge", "CoIn2"])

   # Return file path matching CeAl2Ga2
   ensemble.filter_by_structures("CeAl2Ga2")

To learn more, please read the official documentation here:
https://bobleesj.github.io/cifkit.

Quotes
------

Here is a quote illustrating how ``cifkit`` addresses one of the
challenges mentioned above.

   “I am building an X-Ray diffraction analysis (XRD) pattern
   visualization script for my lab using ``pymatgen``. I feel like
   ``cifkit`` integrated really well into my existing stable of
   libraries, while surpassing some alternatives in preprocessing and
   parsing. For example, it was often unclear at what stage an error
   occurred—whether during pre-processing with ``CifParser``, or XRD
   plot generation with ``diffraction.core`` in ``pymatgen``. The
   pre-processing logic in ``cifkit`` was communicated clearly, both in
   documentation and in actual outputs, allowing me to catch errors in
   my data before it was used in my visualizations. I now use ``cifkit``
   by default for processing CIFs before they pass through the rest of
   my pipeline.” - Alex Vtorov \`

Documentation
-------------

-  `Official documentation <https://bobleesj.github.io/cifkit>`_
-  `MIT license <https://github.com/bobleesj/cifkit/blob/main/LICENSE>`_

Citation
--------

If you use ``cifkit`` in your publication, please cite the following:

.. code:: text

   @article{Lee2024,
     author    = {Sangjoon Lee and Anton O. Oliynyk},
     title     = {cifkit: A Python package for coordination geometry and atomic site analysis},
     journal   = {Journal of Open Source Software},
     year      = {2024},
     volume    = {9},
     number    = {103},
     pages     = {7205},
     publisher = {The Open Journal},
     doi       = {10.21105/joss.07205},
     url       = {https://doi.org/10.21105/joss.07205}
   }

How to contribute
-----------------

Here is how you can contribute to the ``cifkit`` project if you found it
helpful:

-  Star the repository on GitHub and recommend it to your colleagues who
   might find ``cifkit`` helpful as well. |Star GitHub repository|
-  Create a new issue for any bugs or feature requests
   `here <https://github.com/bobleesj/cifkit/issues>`_
-  Fork the repository and consider contributing changes via a pull
   request. |Fork GitHub repository|.
-  If you have any suggestions or need further clarification on how to
   use ``cifkit``, please reach out to Bob Lee
   (`@bobleesj <https://github.com/bobleesj>`_).

Acknowledgements
----------------

``cifkit`` is maintained and developed with the help of
``scikit-package`` (https://scikit-package.github.io/scikit-package/).

