# cifkit

[![CI](https://github.com/bobleesj/cifkit/actions/workflows/tests-on-pr.yml/badge.svg?branch=main)](https://github.com/bobleesj/cifkit/actions/workflows/tests-on-pr.yml)
![Python - Version](https://img.shields.io/pypi/pyversions/cifkit)
[![PyPi version](https://img.shields.io/pypi/v/cifkit.svg)](https://pypi.python.org/pypi/cifkit)

<a href="https://joss.theoj.org/papers/9016ae27b8c6fddffaae5aeb8be18d19"><img src="https://joss.theoj.org/papers/9016ae27b8c6fddffaae5aeb8be18d19/status.svg"></a>

![Logo light mode](doc/source/img/logo-black.png#gh-light-mode-only "cifkit logo light")
![Logo dark mode](doc/source/img/logo-color.png#gh-dark-mode-only "cifkit logo dark")

`cifkit` is designed to provide a set of fully-tested utility functions and
variables for handling large datasets, on the order of tens of thousands, of
`.cif` files.

## Features:

`cifkit` provides higher-level functions in just a few lines of code.

- **Coordination geometry** - `cifkit` provides functions for visualing
  coordination geometry from each site and extracts physics-based features like
  volume and packing efficiency in each polyhedron.
- **Atomic mixing** - `cifkit` extracts atomic mixing information at the bond
  pair level—tasks that would otherwise require extensive manual effort using
  GUI-based tools like VESTA, Diamond, and CrystalMaker.
- **Filter** - `cifkit` offers features for preprocessing. It systematically
  addresses common issues in CIF files from databases, such as incorrect loop
  values and missing fractional coordinates, by standardizing and filtering out
  ill-formatted files. It also preprocesses atomic site labels, transforming
  labels such as 'M1' to 'Fe1' in files with atomic mixing.
- **Sort** - `cifkit` allows you to copy, move, and sort `.cif` files based on
  attributes such as coordination numbers, space groups, unit cells, shortest
  distances, elements, and more.

### Example usage 1 - coordination geometry

The example below uses `cifkit` to visualize the polyhedron generated from each
atomic site based on the coordination number geometry.

```python
from cifkit import Cif

cif = Cif("your_cif_file_path")
site_labels = cif.site_labels

# Loop through each site label
for label in site_labels:
    # Dipslay each polyhedron, .png saved for each label
    cif.plot_polyhedron(label, is_displayed=True)
```

![Polyhedron generation](doc/source/img/ErCoIn-polyhedron.png)

### Example Usage 2 - sort

The following example generates a distribution of structure.

```python
from cifkit import CifEnsemble

ensemble = CifEnsemble("your_folder_path_containing_cif_files")
ensemble.generate_structure_histogram()
```

![structure distribution](doc/source/img/histogram-structure.png)

Basde on your visual histogram above, you can copy and move .cif files based on
specific attributes:

```python
# Return file paths matching structures either Co1.75Ge or CoIn2
ensemble.filter_by_structures(["Co1.75Ge", "CoIn2"])

# Return file path matching CeAl2Ga2
ensemble.filter_by_structures("CeAl2Ga2")
```

To learn more, please read the official documentation here:
https://bobleesj.github.io/cifkit.

## Quotes

Here is a quote illustrating how `cifkit` addresses one of the challenges
mentioned above.

> "I am building an X-Ray diffraction analysis (XRD) pattern visualization
> script for my lab using `pymatgen`. I feel like `cifkit` integrated really
> well into my existing stable of libraries, while surpassing some alternatives
> in preprocessing and parsing. For example, it was often unclear at what stage
> an error occurred—whether during pre-processing with `CifParser`, or XRD plot
> generation with `diffraction.core` in `pymatgen`. The pre-processing logic in
> `cifkit` was communicated clearly, both in documentation and in actual
> outputs, allowing me to catch errors in my data before it was used in my
> visualizations. I now use `cifkit` by default for processing CIFs before they
> pass through the rest of my pipeline." - Alex Vtorov `

## Documentation

- [Official documentation](https://bobleesj.github.io/cifkit)
- [Contribution guide](https://github.com/bobleesj/cifkit/blob/main/CONTRIBUTING.md)
- [MIT license](https://github.com/bobleesj/cifkit/blob/main/LICENSE)

## Citation

If you use `cifkit` in your publication, please cite the following:

```text
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
```

## How to contribute

Here is how you can contribute to the `cifkit` project if you found it helpful:

- Star the repository on GitHub and recommend it to your colleagues who might
  find `cifkit` helpful as well.
  [![Star GitHub repository](https://img.shields.io/github/stars/bobleesj/cifkit.svg?style=social)](https://github.com/bobleesj/cifkit/stargazers)
- Create a new issue for any bugs or feature requests
  [here](https://github.com/bobleesj/cifkit/issues)
- Fork the repository and consider contributing changes via a pull request.
  [![Fork GitHub repository](https://img.shields.io/github/forks/bobleesj/cifkit?style=social)](https://github.com/bobleesj/cifkit/fork).
  Check out
  [CONTRIBUTING.md](https://github.com/bobleesj/cifkit/blob/main/CONTRIBUTING.md)
  for instructions.
- If you have any suggestions or need further clarification on how to use
  `cifkit`, please reach out to Bob Lee
  ([@bobleesj](https://github.com/bobleesj)).

## Acknowledgements

`cifkit` is maintained and developed with the help of `scikit-package` (https://scikit-package.github.io/scikit-package/).
