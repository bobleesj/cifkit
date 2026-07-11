# OLED — Oliynyk elemental data

**OLED** = **O**liynyk **E**lemental **D**ata (22 properties × **76
elements**) for composition featurization and ML.

**Load with** `from cifkit.sources.oliynyk import Oliynyk, Property` —
not a separate package; not related to OLED displays.

## Get the data (+ how to credit it)

| Asset | Link |
|---|---|
| **Full table (CSV)** | [oled.csv](../_static/oled.csv) |
| **Citation file (BibTeX + text)** | [CITATION.txt](../_static/CITATION.txt) |
| **Agent recipes** | [llms.txt](../llms.txt) |

If the OLED table was useful in a paper or product, consider citing the
**dataset** paper (and cifkit if you also used CIF geometry):

- **OLED dataset** — Lee, Chen, Garcia & Oliynyk, *Data in Brief* **53**,
  110178 (2024).
  DOI: [10.1016/j.dib.2024.110178](https://doi.org/10.1016/j.dib.2024.110178)
- **cifkit software** — Lee & Oliynyk, *JOSS* **9**, 7205 (2024).
  DOI: [10.21105/joss.07205](https://doi.org/10.21105/joss.07205)
- **Related — AB-stacking prototype structures** — Selvaratnam, Jaffal,
  Shiryaev & Oliynyk, *Data in Brief* **63**, 112138 (2025).
  DOI: [10.1016/j.dib.2025.112138](https://doi.org/10.1016/j.dib.2025.112138)
  · [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2352340925008595)

```bibtex
@article{Lee2024OLED,
  author  = {Lee, Sangjoon and Chen, C. and Garcia, G. and Oliynyk, Anton},
  title   = {Machine learning descriptors in materials chemistry used in
             multiple experimentally validated studies: Oliynyk elemental
             property dataset},
  journal = {Data in Brief},
  year    = {2024},
  volume  = {53},
  pages   = {110178},
  doi     = {10.1016/j.dib.2024.110178}
}
```

## Full table

All 76 elements × 22 properties (+ symbol). Scroll sideways for every
column; search only filters this list (clear the box to show all rows).

```{raw} html
:file: ../_static/oled_table.html
```

Column header abbreviations (hover a header for the full key):

| Header | Property key |
|---|---|
| El | symbol |
| AW | atomic_weight |
| Z | atomic_number |
| Per / Grp | period / group |
| Mend# | Mendeleev_number |
| Val e / Unp e | valencee_total / unpaired_electrons |
| IE | ionization_energy |
| CN | coordination_number |
| CIF r / Pauling r | CIF_radius / Pauling_radius_CN12 |
| Pauling EN / MB EN | Pauling_EN / Martynov_Batsanov_EN |
| Tm (K) | melting_point_K |
| dens / Cp / Ecoh / B | density / specific_heat / cohesive_energy / bulk_modulus |

## What each property means

cifkit ships a **22-column subset** of the larger Oliynyk elemental table
(98 features in the dataset paper). Meanings below follow that paper’s
**Table 1** (property · origin · ML use) and the data-description text
([Data in Brief 10.1016/j.dib.2024.110178](https://doi.org/10.1016/j.dib.2024.110178)).
Use these columns as **elemental descriptors** for composition-based
features (weighted averages, min/max over elements in a formula, etc.).

| `Property` enum | Column key | What it is | Why it shows up in ML / materials work |
|---|---|---|---|
| `AW` | `atomic_weight` | Weighted arithmetic mean of relative isotopic masses | Mass-weighted composition; used in hardness / superhard-materials models |
| `ATOMIC_NUMBER` | `atomic_number` | Proton count *Z*; periodic-table position | Sums / averages of *Z* used in structure classification |
| `PERIOD` | `period` | Period (row) in the periodic table | Coarse electronic-shell / size trend |
| `GROUP` | `group` | Group (column) in the periodic table | Chemical-family encoding |
| `MEND_NUM` | `Mendeleev_number` | Alternative element order so similar elements sit near each other | Averages used for hardness-type predictions |
| `VAL_TOTAL` | `valencee_total` | Total valence-electron count (column spelling as shipped) | Electron-count features for Heusler / AB compounds |
| `UNPARIED_E` | `unpaired_electrons` | Number of unpaired valence electrons | Open-shell / magnetism-related electron bookkeeping |
| `GILMAN` | `Gilman` | Gilman valence-electron count (group number, with *d*-block exceptions) | Valence trends in mechanical / strength-related models |
| `Z_EFF` | `Z_eff` | Effective nuclear charge on outer electrons (shielding included) | Combines well with valence-electron counts |
| `ION_ENERGY` | `ionization_energy` | First ionization energy (remove one electron) | Electronic reactivity / bonding tendency |
| `COORD_NUM` | `coordination_number` | Characteristic coordination number stored for the element in this table | Local-packing / size context in solid-state featurization |
| `RATIO_CLOSEST` | `ratio_closest` | Size / packing ratio feature from the curated solid-state set | Geometry-related size descriptor for intermetallics |
| `POLYHEDRON_DISTORT` | `polyhedron_distortion` | Local packing distortion metric in the curated set | Distortion-sensitive structure features |
| `CIF_RADIUS` | `CIF_radius` | Element radius used with CIF-radius distance normalization (Å) | Size scale aligned with CIF geometry analysis in cifkit |
| `PAULING_RADIUS_CN12` | `Pauling_radius_CN12` | Pauling metallic radius for CN = 12 | Metallic size scale for structure / packing models |
| `PAULING_EN` | `Pauling_EN` | Pauling electronegativity | EN differences place bonds on the covalent–ionic spectrum |
| `MARTYNOV_BATSANOV_EN` | `Martynov_Batsanov_EN` | Martynov–Batsanov electronegativity | Alternate EN scale for composition features |
| `MELTING_POINT_K` | `melting_point_K` | Elemental melting point (K) | Thermodynamic / cohesion-related bulk trend |
| `DENSITY` | `density` | Elemental bulk density | Mass/volume bulk property |
| `SPECIFIC_HEAT` | `specific_heat` | Specific heat capacity | Thermal bulk property |
| `COHESIVE_ENERGY` | `cohesive_energy` | Energy to separate solid into free atoms | Often strong when data are consistently sourced |
| `BULK_MODULUS` | `bulk_modulus` | Resistance to uniform compression | Mechanical bulk property; frequently useful with cohesive energy |

The **full 98-feature Excel** (more EN scales, radii, DFT, nuclear, HHI
cost, …) is described in the same paper and hosted on Mendeley Data:
[10.17632/bt6gv5z6yv](https://data.mendeley.com/datasets/bt6gv5z6yv).
cifkit’s OLED table is the portable 22-column subset used for day-to-day
composition featurization in this package.

## Load in Python

```bash
pip install cifkit
```

```python
from cifkit.sources.oliynyk import Oliynyk, Property

oled = Oliynyk()  # OLED = Oliynyk elemental data
print(len(oled.elements), "elements")
print(oled.elements)

# Exact Property enum → column key (use these names as written)
for prop in Property:
    print(f"{prop.name:22} {prop.value}")

print(oled.db["Si"][Property.AW], oled.db["Si"][Property.PAULING_EN])
for prop in Property:
    print(prop.value, oled.db["Si"][prop])
```

```text
76 elements
['Li', 'Be', 'B', …, 'Th', 'U']

AW                     atomic_weight
ATOMIC_NUMBER          atomic_number
PERIOD                 period
GROUP                  group
MEND_NUM               Mendeleev_number
VAL_TOTAL              valencee_total
UNPARIED_E             unpaired_electrons
GILMAN                 Gilman
Z_EFF                  Z_eff
ION_ENERGY             ionization_energy
COORD_NUM              coordination_number
RATIO_CLOSEST          ratio_closest
POLYHEDRON_DISTORT     polyhedron_distortion
CIF_RADIUS             CIF_radius
PAULING_RADIUS_CN12    Pauling_radius_CN12
PAULING_EN             Pauling_EN
MARTYNOV_BATSANOV_EN   Martynov_Batsanov_EN
MELTING_POINT_K        melting_point_K
DENSITY                density
SPECIFIC_HEAT          specific_heat
COHESIVE_ENERGY        cohesive_energy
BULK_MODULUS           bulk_modulus

28.0855 1.9
atomic_weight 28.0855
…
bulk_modulus 98.0
```

**Canonical `Property` list (exact names):** `AW`, `ATOMIC_NUMBER`,
`PERIOD`, `GROUP`, `MEND_NUM`, `VAL_TOTAL`, `UNPARIED_E`, `GILMAN`,
`Z_EFF`, `ION_ENERGY`, `COORD_NUM`, `RATIO_CLOSEST`,
`POLYHEDRON_DISTORT`, `CIF_RADIUS`, `PAULING_RADIUS_CN12`, `PAULING_EN`,
`MARTYNOV_BATSANOV_EN`, `MELTING_POINT_K`, `DENSITY`, `SPECIFIC_HEAT`,
`COHESIVE_ENERGY`, `BULK_MODULUS`. Prefer `Property.AW` over free-form
strings. Note `UNPARIED_E` and column `valencee_total` are spelled as in
the package.

Export (pair the CSV with a citation note in your repo/paper):

```python
from cifkit.sources.oliynyk import Oliynyk

Oliynyk().to_csv("oled.csv")
df = Oliynyk().to_dataframe()  # (76, 23)
# When sharing oled.csv, also keep the dataset DOI:
# https://doi.org/10.1016/j.dib.2024.110178  (Lee et al., Data in Brief 2024)
# Software that loads it: https://doi.org/10.21105/joss.07205  (cifkit JOSS)
```

### Formula → feature vector (ML)

Stoichiometry-weighted mean of every OLED property for a composition:

```python
from cifkit.parsers.formula import Formula
from cifkit.sources.oliynyk import Oliynyk, Property

oled = Oliynyk()
parsed = Formula("NdSi2").parsed_formula  # [('Nd', 1.0), ('Si', 2.0)]
total = sum(c for _, c in parsed)
features = {
    prop.value: sum(oled.db[el][prop] * c for el, c in parsed) / total
    for prop in Property
}
print(features["atomic_weight"], features["Pauling_EN"])
```

```text
66.80433333333333 1.6466666666666665
```

### Per-formula helpers

```python
from cifkit.sources.oliynyk import Oliynyk, Property

oled = Oliynyk()
print(oled.get_property_data_for_formula("NdSi2", Property.AW))
print(oled.is_formula_supported("LiFePO4"))
supported, unsupported = oled.get_supported_formulas(["FeH", "NdSi2", "UO2"])
print(supported, unsupported)
```

```text
{'Nd': 144.242, 'Si': 28.0855}
True
['NdSi2', 'UO2'] ['FeH']
```

API: [Oliynyk / Property](../api/oliynyk) · [llms.txt](../llms.txt)

## Publications

Same references as at the top of this page (dataset + software). Full
BibTeX for both: [CITATION.txt](../_static/CITATION.txt).

## Research that used OLED

- Copper Gallium Aluminum mixed metal oxides as alternative catalyst
  candidates for efficient conversion of carbon dioxide to methanol and
  dimethyl ether
  ([ACS Catal.](https://pubs.acs.org/doi/10.1021/acscatal.5c03876))
- Design and implementation of sintered NdFeB performance prediction
  system based on machine learning
  ([ISRIMT 2024](https://doi.org/10.1109/ISRIMT63979.2024.10875235))
- Multi-objective optimization of material properties for enhanced
  battery performance using artificial intelligence
  ([Expert Syst. Appl.](https://doi.org/10.1016/j.eswa.2025.128179))
- Machine learning based investigation of atomic packing effects:
  chemical pressures at the extremes of intermetallic complexity
  ([JACS](https://pubs.acs.org/doi/10.1021/jacs.4c10479))
- Machine learning predictions of thermopower for thermoelectric
  material screening
  ([ACS Appl. Energy Mater.](https://doi.org/10.1021/acsaem.5c02609))
- CALPHAD-based Bayesian optimization to accelerate alloy discovery for
  high-temperature applications
  ([J. Mater. Res.](https://doi.org/10.1557/s43578-024-01489-0))
- Machine learning assisted discovery of Cr³⁺-based near-infrared
  phosphors
  ([Chem. Mater.](https://doi.org/10.1021/acs.chemmater.5c01208))
- Thermoelectric material performance (zT) predictions with machine
  learning
  ([ACS Appl. Mater. Interfaces](https://pubs.acs.org/doi/10.1021/acsami.4c19149))
- Explainable recommendation engines to predict complex intermetallics:
  synthesis and characterization of Gd₁₀RuCd₃, a neutron absorption
  material
  ([JACS](https://pubs.acs.org/doi/10.1021/jacs.5c11646))
- A physics-regularized machine learning approach for predicting
  time-temperature-transformation curves in alloys: application to
  uranium-based alloys
  ([Research Square](https://doi.org/10.21203/rs.3.rs-9272503/v1))
