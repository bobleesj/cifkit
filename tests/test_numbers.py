import pytest

from cifkit.numbers import calculate_basic_stats


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [1, 2, 3, 4, 5],
            {
                "max": 5.0,
                "min": 1.0,
                "mid": 3.0,
                "avg": 3.0,
                "std": pytest.approx(1.41421356, abs=1e-5),
                "var": pytest.approx(2.0, abs=1e-5),
            },
        ),
        (
            [42],
            {
                "max": 42.0,
                "min": 42.0,
                "mid": 42.0,
                "avg": 42.0,
                "std": 0.0,
                "var": 0.0,
            },
        ),
    ],
)
def test_calculate_basic_stats(data, expected):
    result = calculate_basic_stats(data)
    for key in expected:
        assert result[key] == expected[key]


def test_calculate_basic_stats_empty_input_error():
    with pytest.raises(ValueError):
        calculate_basic_stats([])
