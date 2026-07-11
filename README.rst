cifkit
======

|PyPI| |PythonVersion| |PR|

|CI| |Tracking|

.. |CI| image:: https://github.com/bobleesj/cifkit/actions/workflows/matrix-on-merge-to-main.yml/badge.svg
        :target: https://github.com/bobleesj/cifkit/actions/workflows/matrix-on-merge-to-main.yml

.. |PR| image:: https://img.shields.io/badge/PR-Welcome-29ab47ff
        :target: https://github.com/bobleesj/cifkit/pulls

.. |PyPI| image:: https://img.shields.io/pypi/v/cifkit
        :target: https://pypi.org/project/cifkit/

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/cifkit
        :target: https://pypi.org/project/cifkit/

.. |Tracking| image:: https://img.shields.io/badge/issue_tracking-github-blue
        :target: https://github.com/bobleesj/cifkit/issues

**Docs:** https://bobleesj.github.io/cifkit/

**LLM / agent recipes (plain text):** https://bobleesj.github.io/cifkit/llms.txt
(also ``llms.txt`` in this repository)

``cifkit`` parses Crystallographic Information Files (``.cif``) for
coordination geometry and atomic-site features, and ships **OLED
(Oliynyk elemental data)** for composition featurization (ML).

Install::

   pip install cifkit

Common tasks
------------

1) Parse physical features from one ``.cif``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from cifkit import Cif, Example

   cif = Cif(Example.GdSb_file_path)  # or Cif("file.cif")
   print(cif.formula, cif.structure, cif.space_group_name, cif.site_labels)
   print(cif.shortest_distance, cif.shortest_bond_pair_distance)

   cif.compute_CN()
   print(cif.CN_best_methods)  # volume, packing_efficiency, CN, …
   print(cif.CN_bond_fractions_by_min_dist_method)

Tutorial: https://bobleesj.github.io/cifkit/tutorials/physical-features.html

2) Statistics over many ``.cif`` files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from cifkit import CifEnsemble, Example

   ensemble = CifEnsemble(Example.demo_cif_folder_path)  # or a folder path
   print(ensemble.file_count, ensemble.unique_formulas)
   paths = ensemble.filter_by_formulas(["GdSb"])

Tutorial: https://bobleesj.github.io/cifkit/tutorials/statistics-many-cifs.html

3) OLED — Oliynyk elemental data (composition / ML)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**OLED** is the Oliynyk elemental property table (22 properties × 76
elements). Load it with ``cifkit.sources.oliynyk.Oliynyk`` — not a
separate package.

.. code:: python

   from cifkit.sources.oliynyk import Oliynyk, Property
   from cifkit.parsers.formula import Formula

   oled = Oliynyk()
   print(len(oled.elements), "elements")
   for prop in Property:  # exact enum names — do not rename
       print(prop.name, prop.value)
   print(oled.db["Si"][Property.AW], oled.db["Si"][Property.PAULING_EN])
   oled.to_csv("oled.csv")

   # Formula → stoichiometry-weighted mean feature vector
   parsed = Formula("NdSi2").parsed_formula  # [('Nd', 1.0), ('Si', 2.0)]
   total = sum(c for _, c in parsed)
   features = {
       prop.value: sum(oled.db[el][prop] * c for el, c in parsed) / total
       for prop in Property
   }
   print(features["atomic_weight"], features["Pauling_EN"])

**Exact** ``Property`` members (use these names as written)::

   AW, ATOMIC_NUMBER, PERIOD, GROUP, MEND_NUM, VAL_TOTAL, UNPARIED_E,
   GILMAN, Z_EFF, ION_ENERGY, COORD_NUM, RATIO_CLOSEST, POLYHEDRON_DISTORT,
   CIF_RADIUS, PAULING_RADIUS_CN12, PAULING_EN, MARTYNOV_BATSANOV_EN,
   MELTING_POINT_K, DENSITY, SPECIFIC_HEAT, COHESIVE_ENERGY, BULK_MODULUS

Tutorial: https://bobleesj.github.io/cifkit/tutorials/oled.html

Features
--------

-  **Physical features from a ``.cif``** — distances, four coordination
   methods, polyhedron metrics (volume, packing efficiency), bond
   fractions, site mixing.
-  **Statistics over many CIFs** — filter, histogram, copy/move folders.
-  **OLED (Oliynyk elemental data)** — composition descriptors for ML;
   CSV export via ``Oliynyk().to_csv()``.

|Logo light mode| |Logo dark mode|

.. |Logo light mode| image:: docs/source/img/logo-black.png#gh-light-mode-only
.. |Logo dark mode| image:: docs/source/img/logo-color.png#gh-dark-mode-only

Documentation
-------------

-  `Official documentation (Jupyter Book) <https://bobleesj.github.io/cifkit>`_
-  `LLM recipes (llms.txt) <https://bobleesj.github.io/cifkit/llms.txt>`_
-  `Source <https://github.com/bobleesj/cifkit>`_

Publications
------------

Citation files: ``CITATION.cff`` (repo root) and
https://bobleesj.github.io/cifkit/_static/CITATION.txt

Consider citing if useful:

-  **cifkit** — Lee & Oliynyk, JOSS (2024).
   https://doi.org/10.21105/joss.07205
-  **OLED / Oliynyk elemental data** — Lee et al., Data in Brief (2024).
   https://doi.org/10.1016/j.dib.2024.110178

.. code:: text

   @article{Lee2024,
     author    = {Sangjoon Lee and Anton O. Oliynyk},
     title     = {cifkit: A Python package for coordination geometry and atomic site analysis},
     journal   = {Journal of Open Source Software},
     year      = {2024},
     volume    = {9},
     number    = {103},
     pages     = {7205},
     doi       = {10.21105/joss.07205}
   }

How to contribute
-----------------

-  Issues: https://github.com/bobleesj/cifkit/issues
-  PRs welcome; run ``pytest`` and keep one theme per branch.

Acknowledgements
----------------

Developed with ``scikit-package``
(https://scikit-package.github.io/scikit-package/). Maintained by
Sangjoon Bob Lee.
