"""Unit tests for __version__.py."""

import cifkit


def test_package_version():
    """Ensure the package version is defined and not set to the initial
    placeholder."""
    assert hasattr(cifkit, "__version__")
    assert cifkit.__version__ != "0.0.0"
