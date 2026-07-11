# Formula

Parse a composition string into `(element, count)` pairs, normalize
indices, and sort/filter formulas. Used with OLED for ML feature vectors.

```python
from cifkit.parsers.formula import Formula

f = Formula("NdSi2")
f.formula                 # 'NdSi2'
f.elements                # ['Nd', 'Si']
f.parsed_formula          # [('Nd', 1.0), ('Si', 2.0)]  # use this for weights
f.indices                 # [1.0, 2.0]
f.element_count           # 2
f.get_normalized_formula()
```

With OLED: [quick reference — Formula → feature vector](quick-reference) ·
[OLED tutorial](../tutorials/oled) · [llms.txt](../llms.txt)

## Reference

```{eval-rst}
.. autoclass:: cifkit.parsers.formula.Formula
   :members:
   :show-inheritance:
```
