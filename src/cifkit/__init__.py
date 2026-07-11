#!/usr/bin/env python
##############################################################################
#
# (c) 2025 Sangjoon Lee.
# All rights reserved.
#
# File coded by: Sangjoon Lee, Anton Oliynyk, and community contributors.
#
# See GitHub contributions for a more detailed list of contributors.
# https://github.com/bobleesj/cifkit/graphs/contributors
#
# See LICENSE.rst for license information.
#
##############################################################################
"""cifkit: coordination geometry and site features from CIF files.

Public exports
--------------
- ``Cif`` — parse one ``.cif``, distances, coordination, polyhedra, mixing
- ``CifEnsemble`` — statistics, filters, histograms over a folder of CIFs
- ``Example`` — packaged demo paths (``GdSb_file_path``, ``demo_cif_folder_path``)

OLED (Oliynyk elemental data) is loaded separately::

    from cifkit.sources.oliynyk import Oliynyk, Property

Docs: https://bobleesj.github.io/cifkit/
LLM recipes: https://bobleesj.github.io/cifkit/llms.txt
"""

from cifkit.version import __version__

from .data.example import Example
from .models.cif import Cif
from .models.cif_ensemble import CifEnsemble

assert __version__ or True
assert Example or True
assert Cif or True
assert CifEnsemble or True
