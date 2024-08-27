import pytest

from cifkit.utils.cif_type import get_cif_file_source


@pytest.mark.now
def test_check_for_icsd_code():
    # Example usage
    ICSD_file_path = "tests/data/ICSD/icsd_001385.cif"
    assert get_cif_file_source(ICSD_file_path) == "ICSD"
    PCD_file_path = "tests/data/cif/URhIn.cif"
    assert get_cif_file_source(PCD_file_path) == "PCD"
