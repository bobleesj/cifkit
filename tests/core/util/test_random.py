from cifkit.utils.random import generate_random_numbers


def test_generate_random_numbers():
    count = 10
    low = 20
    high = 30
    float_results = generate_random_numbers(count, low, high)
    int_results = generate_random_numbers(count, low, high, is_float=False)
    # Test bound
    assert all(low <= x <= high for x in float_results)
    assert all(low <= x <= high for x in int_results)

    # Test type and lengths
    assert all(isinstance(x, int) for x in int_results) and len(int_results) == 10
    assert all(isinstance(x, float) for x in float_results) and len(float_results) == 10
