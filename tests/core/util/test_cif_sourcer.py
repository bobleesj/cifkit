import pytest

from cifkit.utils.cif_sourcer import get_cif_db_source


@pytest.mark.fast
def test_check_cif_file_known_databases():
    COD_file_1 = "tests/data/cif/sources/COD/1010581.cif"
    COD_file_2 = "tests/data/cif/sources/COD/1523923.cif"
    assert get_cif_db_source(COD_file_1) == "COD"
    assert get_cif_db_source(COD_file_2) == "COD"

    ICSD_file = "tests/data/cif/sources/ICSD/EntryWithCollCode43054.cif"
    assert get_cif_db_source(ICSD_file) == "ICSD"

    MS_file = "tests/data/cif/sources/MS/U13Rh4.cif"
    assert get_cif_db_source(MS_file) == "MS"

    PCD_file = "tests/data/cif/sources/PCD/250117.cif"
    assert get_cif_db_source(PCD_file) == "PCD"
