from cifkit.preprocessors.supercell_util import get_cell_atom_count


def test_get_cell_atom_count_no_shift(unitcell_points_URhIn):
    assert get_cell_atom_count(unitcell_points_URhIn) == 22


def test_get_cell_atom_count_full_shift(supercell_points_URhIn):
    assert get_cell_atom_count(supercell_points_URhIn) == 336
