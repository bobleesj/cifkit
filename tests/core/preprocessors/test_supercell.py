from cifkit import Cif
from cifkit.preprocessors.supercell import get_supercell_points


def test_cif_short_dist(cif_CUMNON_sb: Cif):
    # There are 2 atoms in the unit cell
    assert cif_CUMNON_sb.unitcell_atom_count == 2
    # 5 by 5 by 5 by, (125 unit cells), expect 250
    assert cif_CUMNON_sb.supercell_atom_count == 250


def test_get_supercell_points_full_shift(cif_block_URhIn):
    # +-2 +-2 +-2 shifts
    supercell_points = get_supercell_points(cif_block_URhIn, 3)
    assert len(supercell_points) == 1370
    # +-1 +-1 +-1 shifts
    supercell_points = get_supercell_points(cif_block_URhIn, 2)
    assert len(supercell_points) == 336
