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
"""Python package for doing science."""

# package version
from cifkit.version import __version__

from .data.example import Example
from .models.cif import Cif
from .models.cif_ensemble import CifEnsemble

# silence the pyflakes syntax checker
assert __version__ or True
assert Example or True
assert Cif or True
assert CifEnsemble or True

# End of file
