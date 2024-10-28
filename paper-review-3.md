## Response to @ml-evs

> While this package clearly has some useful tools (particularly the nice polyhedron visualisation), I fail to see how this tool is easier to use than pymatgen/ASE as a selling point. If it is targeted at people with limited programming/Python experience, then much more care must be taken in guiding them through the installation process (with virtual environments etc).

This is a valid comment considering most users end up using the packages that are built on top of `cifkit` rather than building. I've also provided `conda install cifkit_env -n cifkit` option in the package to help manage dependencies easily. This installation and the Getting Started sections were tested by undergraduate and PhD students of Dr. Anton Oliynyk.

> Whilst "high throughput" is mentioned throughout the docs and paper, I see little in the way of e.g., assistance with parallelisation or batch processing (e.g., if I have 1m structures can I stream data without going via a file all the time?), nor any advanced error handling that could allow this package to be used in a highly automated way -- perhaps the authors could clarify what they mean with regards to high throughput in this case?

Repeating my comment above regarding the comment "the order of tens of thousands" by @lancekavalsky,

Based on reviewer feedback and internal discussions, we concluded that our package's strength lies not in high-throughput processing (ASE and pymatgen excel at this), but in its specific features for "coordination geometry" and "atomic site analysis." These features are crucial for experimental research and are often tediously acquired from GUI-based software. Consequently, I've modified the manuscript title to "cifkit: A Python package for coordination geometry and atomic site analysis" and removed "high-throughput."

To clarify, our current implementation doesn't include batch processing. We process each .cif file individually. With approximately 1,000 atoms in the supercell, processing takes about 0.3 seconds for one file and 3,000 atoms—less than 3 seconds total. I've added to the documentation that processing roughly 10,000 .cif files on a standard laptop (iMac with M1 chip) takes about 30 to 60 minutes. At this rate, we can process nearly all .cif files within 1–2 days. However, we've decided not to include performance metrics in the manuscript. Our code may evolve further—perhaps using matrix multiplications to compute distances, as in ASE—and performance hasn't been a major bottleneck for our research.


Regarding error handling, we've processed tens of thousands of binary and ternary .cif files, primarily from PCD and thousands from ICSD. We've aimed to identify the most common errors to ensure we can use as many .cif files from the database as possible. Of course, there are some cases where .cif files lack space group operations or fractional coordinates. In such instances, we move those files into separate folders before initializing them into objects. We've also tested with COD, CCSD, and other datasets to encounter more diverse errors, which users can report later for me to address.

> I do not think it is appropriate to mention test coverage explicitly in the paper; although the package does appear to be well-tested with good CI, pinned dependencies and lots of test cases, this metric can be a red herring.

Thank you for your suggestion. All dependency pinnings have been removed, and CI now supports Python 3.10, 3.11, and 3.12. Additionally, the mention of Codecov has been removed.

> There are a few glaring omissions in the references that could help provide useful background to readers:

Based on your feedback, cifkit now supports CIF files directly downloaded from ICSD, COD, PCD, CCDC, and those created with Materials Studio. I have retained the `hall_crystallographic_1991` citation as it introduces the original CIF format. On demand, I will modify our code to support the new version if databases begin to export .cif in v2.

> The CIF framework itself is not appropriately cited (see https://www.iucr.org/resources/cif/cif2) -- the paper/documentation should also discuss which versions of the CIF standard are supported (it is a growing standard) with changes between v1 and v2. Gemmi, the library used for the underlying CIF parsing, published in JOSS already https://joss.theoj.org/papers/10.21105/joss.04200 Other potential but not mandatory references:

This is greatly appreciated. The Gemmi has been cited, along with PyVista, another JOSS paper. Additionally, citations for NumPy, SciPy, and Matplotlib have been included.

>  chemenv, used under the hood by pymatgen for coordination analysis https://journals.iucr.org/b/issues/2020/04/00/lo5066 (and subsequently much of the pre-existing literature for determining coordination environments).

Thank you. Added in the manuscript.

> Other dedicated CIF parsing projects supported by IUCr: PyCIFRw and COD's CIF parser (with pycodcif Python package) https://journals.iucr.org/j/issues/2016/01/00/po5052/index.html There are many others listed at https://www.iucr.org/resources/cif/software

Since Gemmi provided sufficient parsing capabilities for our tasks with minor fixes done by cifkit such as such as adding “#” to the first line to ICSD .cif files, we have not incorporated additional CIF parsers.

> I feel this submission is borderline on the "Substantial scholarly effort" front, given the guidelines at https://joss.readthedocs.io/en/latest/submitting.html#substantial-scholarly-effort I am not convinced by the text that the library was crucial in the three examples listed by the authors in the applications section; perhaps this could be expanded? Perhaps even the functionality from the other related packages by the author listed in the paper (SAF and CBA) could be exposed in the cifcheck namespace as (effectively) one package?

Yes, cikfit and its applications are actively used by approximately 4-5 research groups. The SAF and CBA modules each have their own descriptions in respective journal publications, making it challenging to consolidate them under a broad `cifkit' umbrella. We would prefer to serve as an 'engine' that provides advanced functionality. Therefore, we do not want to combine packages into one. However, features will continue to be developed on demand, primarily for experimental groups led by Prof. Oliynyk, both within his group and through his active collaborations.
