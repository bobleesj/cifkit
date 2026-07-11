# Installation

`cifkit` is published on [PyPI](https://pypi.org/project/cifkit/). It is
pure Python and supports Python 3.11 through 3.13 on macOS, Linux, and
Windows.

## pip

```bash
pip install cifkit
```

## From source

```bash
git clone https://github.com/bobleesj/cifkit.git
cd cifkit
pip install -e .
```

## Dependencies

`cifkit` pulls in a small scientific stack automatically:

- `gemmi` - CIF parsing and symmetry operations
- `numpy`, `scipy` - distance and geometry math
- `pandas`, `openpyxl` - the Excel-backed Oliynyk elemental database
- `matplotlib` - histograms
- `pyvista` - 3D polyhedron rendering

## Verify

```python
import cifkit
from cifkit import Cif, Example

print(cifkit.__version__)
cif = Cif(Example.GdSb_file_path)
print(cif.formula)
```

```text
1.2.1
GdSb
```

The packaged example CIFs mean the check above runs offline; nothing is
downloaded.
