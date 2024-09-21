import pytest

import cifkit


@pytest.mark.now
def test_version():
    assert cifkit.__version__
    assert cifkit.__version__ != "0.0.0"
