from importlib.metadata import version

from .data.example import Example
from .models.cif import Cif
from .models.cif_ensemble import CifEnsemble

__version__ = version("cifkit")
__all__ = ["Cif", "CifEnsemble", "Example"]
