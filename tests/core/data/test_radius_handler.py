import pytest
from bobleesj.utils.sources import radius

from cifkit.data.radius_handler import compute_radius_sum, get_CIF_pauling_radius


@pytest.mark.fast
def test_get_CIF_pauling_radii():
    test_elements = ["Si", "Fe"]
    expected = {
        "Fe": {"CIF_radius": 1.242, "Pauling_radius_CN12": 1.26},
        "Si": {"CIF_radius": 1.176, "Pauling_radius_CN12": 1.316},
    }
    assert get_CIF_pauling_radius(test_elements) == expected

    test_elements = ["In", "Rh", "U"]
    expected = {
        "In": {"CIF_radius": 1.624, "Pauling_radius_CN12": 1.66},
        "Rh": {"CIF_radius": 1.345, "Pauling_radius_CN12": 1.342},
        "U": {"CIF_radius": 1.377, "Pauling_radius_CN12": 1.516},
    }
    assert get_CIF_pauling_radius(test_elements) == expected


@pytest.mark.fast
def test_compute_radius_sum(radius_data_URhIn, radius_sum_data_URhIn):
    combined_radii = compute_radius_sum(radius_data_URhIn, True)
    expected = radius_sum_data_URhIn

    # Assert each element and sub-element individually
    for element, radii in expected.items():
        for key, value in radii.items():
            assert combined_radii[element][key] == pytest.approx(value, abs=0.001)


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["H", "Li"], False),
        (["H", "He"], False),
        (["U", "Rh", "In"], True),
        (["Er", "Co", "In"], True),
    ],
)
def test_check_radius_data_available(elements, expected):
    assert radius.are_available(elements) == expected
