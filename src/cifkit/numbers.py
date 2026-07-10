from numpy import max, mean, median, min, std, var


def calculate_basic_stats(values):
    return {
        "max": float(max(values)),
        "min": float(min(values)),
        "mid": float(median(values)),
        "avg": float(mean(values)),
        "std": float(std(values)),
        "var": float(var(values)),
    }
