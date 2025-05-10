import random


def generate_random_numbers(
    count: int, low: int | float, high: int | float, is_float=True
):
    random.seed(42)
    """Generate a list of random numbers (floating-point or integer)."""
    if is_float:
        return [random.uniform(low, high) for _ in range(count)]
    else:
        return [random.randint(int(low), int(high)) for _ in range(count)]
