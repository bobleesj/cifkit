from cifkit.data import radius_optimization

def test_generate_adjacent_pairs():
    actual = radius_optimization.generate_adjacent_pairs(["A", "B", "C"])
    expected =  [('A', 'B'), ('B', 'C')]
    assert actual == expected

def test_generated_adjacent_pairs_not_sorted():
    actual = radius_optimization.generate_adjacent_pairs(["C", "A", "B"])
    expected =  [('C', 'A'), ('A', 'B')]
    assert actual == expected

