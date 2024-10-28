## Response to @ml-evs

> While this package clearly has some useful tools (particularly the nice polyhedron visualisation), I fail to see how this tool is easier to use than pymatgen/ASE as a selling point. If it is targeted at people with limited programming/Python experience, then much more care must be taken in guiding them through the installation process (with virtual environments etc).

This is a valid comment considering most users end up using the packages that are built on top of `cifkit` rather than building. I've also provided `conda install cifkit_env cifkit` option in the package to help manage dependencies easily.

> Whilst "high throughput" is mentioned throughout the docs and paper, I see little in the way of e.g., assistance with parallelisation or batch processing (e.g., if I have 1m structures can I stream data without going via a file all the time?), nor any advanced error handling that could allow this package to be used in a highly automated way -- perhaps the authors could clarify what they mean with regards to high throughput in this case?

Please see my comment addressed above in response to "In the summary it mentions that this package is designed to process datasets on "the order of tens of thousands" by @lancekavalsky.

> I do not think it is appropriate to mention test coverage explicitly in the paper; although the package does appear to be well-tested with good CI, pinned dependencies and lots of test cases, this metric can be a red herring.

Thank you for your suggestion. All dependency pinnings have been removed, and CI now supports Python 3.10, 3.11, and 3.12. Additionally, the mention of Codecov has been removed.

> There are a few glaring omissions in the references that could help provide useful background to readers:

Based on your feedback, cifkit now supports CIF files directly downloaded from ICSD, COD, PCD, CCDC, and those created with Materials Studio. I have retained the `hall_crystallographic_1991` citation as it introduces the original CIF format. Please let me know if this is incorrect.

> The CIF framework itself is not appropriately cited (see https://www.iucr.org/resources/cif/cif2) -- the paper/documentation should also discuss which versions of the CIF standard are supported (it is a growing standard) with changes between v1 and v2. Gemmi, the library used for the underlying CIF parsing, published in JOSS already https://joss.theoj.org/papers/10.21105/joss.04200 Other potential but not mandatory references:

This is greatly appreciated. The Gemmi has been cited, along with PyVista, another JOSS paper. Additionally, citations for NumPy, SciPy, and Matplotlib have been included.

>  chemenv, used under the hood by pymatgen for coordination analysis https://journals.iucr.org/b/issues/2020/04/00/lo5066 (and subsequently much of the pre-existing literature for determining coordination environments).

Thank you. Added in the manuscript.

> Other dedicated CIF parsing projects supported by IUCr: PyCIFRw and COD's CIF parser (with pycodcif Python package) https://journals.iucr.org/j/issues/2016/01/00/po5052/index.html There are many others listed at https://www.iucr.org/resources/cif/software

Since Gemmi provided sufficient parsing capabilities for our tasks, we have not incorporated additional CIF parsers.

> I feel this submission is borderline on the "Substantial scholarly effort" front, given the guidelines at https://joss.readthedocs.io/en/latest/submitting.html#substantial-scholarly-effort I am not convinced by the text that the library was crucial in the three examples listed by the authors in the applications section; perhaps this could be expanded? Perhaps even the functionality from the other related packages by the author listed in the paper (SAF and CBA) could be exposed in the cifcheck namespace as (effectively) one package?

Yes, cikfit and its applications are actively used by approximately 4-5 research groups. The SAF and CBA modules each have their own descriptions in respective journal publications, making it challenging to consolidate them under a broad `cifkit' umbrella. We would prefer to serve as an 'engine' that provides advanced functionality. However, features will continue to be developed on demand, primarily for experimental groups led by Prof. Oliynyk, both within his group and through his active collaborations.
