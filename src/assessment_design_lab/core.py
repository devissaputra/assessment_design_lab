from collections.abc import Sequence


def _require_non_empty(values: Sequence[float], name: str) -> None:
    if not values:
        raise ValueError(f"{name} must not be empty")


def _sample_variance(values: Sequence[float]) -> float:
    if len(values) < 2:
        raise ValueError("sample variance requires at least two observations")
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def item_difficulty(responses: Sequence[int]) -> float:
    """Return the proportion of correct binary responses."""
    _require_non_empty(responses, "responses")
    if any(value not in (0, 1) for value in responses):
        raise ValueError("responses must contain only 0 and 1")
    return sum(responses) / len(responses)


def item_discrimination(responses: Sequence[int], totals: Sequence[float]) -> float:
    """Compare item success in the upper and lower thirds of total scores."""
    _require_non_empty(responses, "responses")
    if len(responses) != len(totals):
        raise ValueError("responses and totals must have equal length")
    if any(value not in (0, 1) for value in responses):
        raise ValueError("responses must contain only 0 and 1")

    pairs = sorted(zip(totals, responses), reverse=True)
    group_size = max(1, len(pairs) // 3)
    upper = [response for _, response in pairs[:group_size]]
    lower = [response for _, response in pairs[-group_size:]]
    return sum(upper) / len(upper) - sum(lower) / len(lower)


def cronbach_alpha(matrix: Sequence[Sequence[float]]) -> float:
    """Compute Cronbach alpha for a rectangular response matrix."""
    if len(matrix) < 2:
        raise ValueError("matrix must contain at least two respondents")
    item_count = len(matrix[0]) if matrix else 0
    if item_count < 2:
        raise ValueError("matrix must contain at least two items")
    if any(len(row) != item_count for row in matrix):
        raise ValueError("matrix rows must have equal length")

    columns = [[row[index] for row in matrix] for index in range(item_count)]
    item_variance = sum(_sample_variance(column) for column in columns)
    totals = [sum(row) for row in matrix]
    total_variance = _sample_variance(totals)
    if total_variance == 0:
        return 0.0
    return item_count / (item_count - 1) * (1 - item_variance / total_variance)
