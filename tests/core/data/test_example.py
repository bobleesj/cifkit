import pytest

from cifkit import Cif, CifEnsemble, Example


@pytest.mark.fast
def test_ErCoIn_folder_path():
    assert CifEnsemble(Example.ErCoIn_folder_path).file_count == 3
    assert CifEnsemble(Example.ErCoIn_big_folder_path).file_count == 16
    assert Cif(Example.Er10Co9In20_file_path).file_name == "Er10Co9In20.cif"
    assert Cif(Example.ErCoIn5_file_path).file_name == "ErCoIn5.cif"
