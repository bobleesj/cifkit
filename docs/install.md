# Installation

cifkit is published on [PyPI](https://pypi.org/project/cifkit/). The
package itself is pure Python and supports **Python 3.12 through 3.14**
on macOS, Linux, and Windows.

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

`pip install cifkit` pulls a small scientific stack automatically
(`requirements/pip.txt`):

| Package | Role |
|---|---|
| **gemmi** | CIF parsing and symmetry operations |
| **numpy**, **scipy** | Distance and geometry math |
| **pandas**, **openpyxl** | Excel-backed Oliynyk elemental database (OLED) |
| **matplotlib** | Histograms (`CifEnsemble`) |
| **pyvista** | 3D polyhedron rendering |

No extra install step is required for ICSD / COD / PCD-style CIFs - those
are handled by cifkit's preprocess and `db_source` detection, not by
separate packages.

## Verify

```python
import cifkit
from cifkit import Cif, Example

print(cifkit.__version__)
cif = Cif(Example.GdSb_file_path)
print(cif.formula)
```

```text
1.2.2
GdSb
```

The packaged example CIFs mean the check above runs offline; nothing is
downloaded.
