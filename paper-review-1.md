## Review by @espottesmith

**Paper comments:**

> The summary is generally appropriate. From context, a non-expert might realize what *.cif files are (since crystal structures are mentioned in the second sentence), but this could be more explicitly stated in the first sentence.

Thank you for your suggestion. The summary begins with

```
`cifkit` provides higher-level functions and properties for coordination
geometry and atomic site analysis from .cif files, which are standard file
formats for storing crystallographic data such as atomic fractional coordinates,
symmetry operations, and unit cell dimensions.
```

> I come from a computational background, so I'm not the target audience, but I am unconvinced that the basic functionality (i.e., parsing CIF files and extracting information like structures and formulas) is easier in cifkit than in pymatgen/ASE. Similar numbers of lines of code would be required, at least comparing pymatgen and the example given in the cifkit paper (see https://pymatgen.org/usage.html#reading-and-writing-structuresmolecules). Considering higher-level features of cifkit, including filtering groups of CIFs and visualization, I think that cifkit distinguishes itself from other codes. In this area, the authors' argument is more convincing. Perhaps a slight reframing of the Statement of Need is appropriate?

This is a valid point. I have modified the "Statement of Need" and emphaszie the utility of higher-level functions by modifying as follow:

```
`cifkit` distinguishes itself from existing libraries by offering higher-level
functions and variables that allow solid-state synthesists to obtain intuitive,
yet physically impactful properties. It facilitates the visualization of
coordination geometry from each site using four coordination determination
methods and extracts physics-based features like volume and packing
efficiency—crucial for structural analysis in machine learning tasks. Moreover,
`cifkit` extracts atomic mixing information at the bond pair level, tasks that
would otherwise require extensive manual effort using GUI-based tools like
VESTA, Diamond, and CrystalMaker. These functions can be further developed
on-demand, as demonstrated by `cifkit`'s ability to extract coordination
geometry information based on four coordination number determination methods for
a newly discovered phase [@tyvanchuk_crystal_2024].
```

> Otherwise, the paper looks good!

Thank you!

**Code comments:**

> The folder "[occupacny"](https://github.com/bobleesj/cifkit/tree/main/src/cifkit/occupacny) should probably be "occupancy"

Modified. Thank you.

> I initially tried installing with Python 3.9 (as far as I can tell, the "pyproject.toml" and the docs don't specify a version). This caused problems, as cifkit is using type annotation syntax that is not supported in Python 3.9. I now see on PYPI that cifkit only supports Python 3.10, 3.11, and 3.12. Please make this more clear for users.

In `pyproject.toml`, I have added the following `requires-python = '>=3.10, <3.13` to support 3.10, 3.11, 3.12. Per your suggestion, I have included the supported Python badged in the documentation under the Getting Started page.

> In terms of code style, more extensive docstrings (for instance, explaining what the inputs and outputs should be) would be appreciated. It seems there are already some "TODO"s to this effect (see e.g., models/cif.py), so perhaps the authors are planning on making these changes soon. Function bodies are typically well commented (note that I have not read every file)

I have added numpy-style docstrings for the main classes `Cif` and `CifEnsemble` here: https://github.com/bobleesj/cifkit/pull/49. I've also identified some code methods that could be refactored, as noted here: https://github.com/bobleesj/cifkit/issues/53. My next step is to further refine these docstrings by consolidating them into reusable methods.

**Documentation comments:**

> Examples in the docs aren't the most consistent. For instance, some example lines of code use "ensemble" as the variable, and some use "ensemble_test". It may also be better if the commented outputs reflected the example folder ("Example.ErCoIn_big_folder_path") so users can more easily verify correctness. Finally, incorporating the visualization tools in the docs (currently they're demonstrated only in the README) would be appreciated.

Thank you for your suggestion. I have now maintained the isntance name `ensemble` consistently. The actual ouput using the Jupyter notebook has been used for all examples.

> The statement of need could be made more clear in the docs

I have added the statement of need in the beginning of the docs: https://bobleesj.github.io/cifkit/.

> Community guidelines basically amount to "submit a PR or talk to the lead author", but for a project at this scale, perhaps that's appropriate.

Thank you. I have created a PR template https://github.com/bobleesj/cifkit/blob/main/.github/pull_request_template.md and instructions on how to contribute here https://github.com/bobleesj/cifkit/blob/main/CONTRIBUTING.md.

**Overall comments:**

>  In terms of "substantial scholarly effort", this is a reasonably small, simple, and young project. That said, it is clearly already being used for scholarly research, and it is somewhat unique in terms of the features that it offers. As such, I think it should be considered substantial.

Thank you. For one of the projects mentioned, SAF (Structure/Composition Analyzer), which uses approximately 100 features generated using cifkit, we have a pre-print version available: https://chemrxiv.org/engage/chemrxiv/article-details/670aa269cec5d6c142f3b11a. I will continue to maintain the software for ongoing research efforts.

> The paper does not contain original data or results
Yes, .cif files must be provided for us to conduct analysis.

> The authors do not make significant performance claims

I have added information to the documentation stating that processing approximately 10,000 .cif files on a standard laptop (iMac with M1 chip) takes about 30 to 60 minutes. At this rate, we can process nearly all .cif files within 1–2 days. However, I've decided not to include performance metrics in the manuscript. Our code may evolve further—for instance, by using matrix multiplications to compute distances, as in ASE—and performance hasn't been a major bottleneck for our research.

> With some relatively small tweaks, I think this will make a good addition to JOSS.

Thank you for your review!