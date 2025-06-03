from cifkit import Cif
from cifkit.preprocessors.environment import get_site_connections


def test_cif_short_dist(cif_CUMNON_sb: Cif):
    cif_CUMNON_sb.compute_connections
    # There are 2 atoms in the unit cell
    assert cif_CUMNON_sb.unitcell_atom_count == 2
    # 5 by 5 by 5 by, (125 unit cells), expect 250
    assert cif_CUMNON_sb.supercell_atom_count == 250
