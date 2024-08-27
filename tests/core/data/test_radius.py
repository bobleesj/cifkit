import pytest

from cifkit.data.radius import get_radius_data


@pytest.mark.fast
def test_get_radius_data():
    # Call the function to get the radii data
    radii_data = get_radius_data()
    test_elements = ["Si", "Fe", "Co", "U"]
    for element in test_elements:
        assert element in radii_data
        assert "CIF_radius" in radii_data[element]
        assert "Pauling_radius_CN12" in radii_data[element]
        assert isinstance(radii_data[element]["CIF_radius"], float)
        assert isinstance(radii_data[element]["Pauling_radius_CN12"], float)

    # Check specific values for one element to ensure data accuracy
    assert radii_data["Si"]["CIF_radius"] == 1.176
    assert radii_data["Si"]["Pauling_radius_CN12"] == 1.316
