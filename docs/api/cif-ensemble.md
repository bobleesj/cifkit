# CifEnsemble

Folder of `.cif` files: unique attributes, count stats, path filters,
copy/move, and matplotlib histograms.

```python
from cifkit import CifEnsemble, Example

ensemble = CifEnsemble(Example.demo_cif_folder_path)  # or any folder path
print(ensemble.file_count, ensemble.unique_formulas)
paths = ensemble.filter_by_formulas(["GdSb"])
ensemble.copy_cif_files(paths, "out")
ensemble.generate_structure_histogram(output_dir="histograms")
```

**Filter methods (exact names):**
`filter_by_formulas`, `filter_by_structures`,
`filter_by_space_group_names`, `filter_by_space_group_numbers`,
`filter_by_elements_containing`, `filter_by_elements_exact_matching`,
`filter_by_tags`, `filter_by_composition_types`,
`filter_by_site_mixing_types`, `filter_by_min_distance`,
`filter_by_supercell_count`,
`filter_by_CN_min_dist_method_containing`,
`filter_by_CN_min_dist_method_exact_matching`,
`filter_by_CN_best_methods_containing`,
`filter_by_CN_best_methods_exact_matching`.

**Histograms:** `generate_structure_histogram`,
`generate_formula_histogram`, `generate_tag_histogram`,
`generate_space_group_name_histogram`,
`generate_space_group_number_histogram`,
`generate_elements_histogram`, `generate_supercell_size_histogram`,
`generate_composition_type_histogram`,
`generate_site_mixing_type_histogram`,
`generate_CN_by_min_dist_method_histogram`,
`generate_CN_by_best_methods_histogram`.

**Calibrated tables:** [API quick reference](quick-reference).  
**Tutorial:** [Statistics over many CIFs](../tutorials/statistics-many-cifs).  
**LLM recipes:** [llms.txt](../llms.txt).

## Full autodoc

```{eval-rst}
.. autoclass:: cifkit.models.cif_ensemble.CifEnsemble
   :members:
   :undoc-members:
   :show-inheritance:
```
