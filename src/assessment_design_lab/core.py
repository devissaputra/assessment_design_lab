# Calculation reading guide: ../CALCULATIONS.md (repository root).
# Alpha = k/(k-1) × (1 - sum(item variances)/variance(total score)).
# Difficulty is proportion correct, so larger values mean easier items. Discrimination uses rest scores to avoid part-whole inflation. Alpha is not dimensionality or validity; zero total variance makes it undefined.

import math
from collections.abc import Sequence
from numbers import Real


def _require_non_empty(values: Sequence[object], name: str) -> None:
    if not values:
        raise ValueError(f"{name} must not be empty")


def _validate_numeric(values: Sequence[Real], name: str) -> None:
    for value in values:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must contain only numeric values")
        if not math.isfinite(float(value)):
            raise ValueError(f"{name} must contain only finite values")


def _validate_binary(values: Sequence[int], name: str) -> None:
    if any(value not in (0, 1) or isinstance(value, bool) for value in values):
        raise ValueError(f"{name} must contain only binary 0/1 values")


def _validate_matrix(
    matrix: Sequence[Sequence[Real]],
    *,
    binary: bool = False,
) -> tuple[int, int]:
    if len(matrix) < 2:
        raise ValueError("matrix must contain at least two respondents")

    item_count = len(matrix[0]) if matrix else 0
    if item_count < 2:
        raise ValueError("matrix must contain at least two items")

    if any(len(row) != item_count for row in matrix):
        raise ValueError("matrix rows must have equal length")

    for row_index, row in enumerate(matrix):
        _validate_numeric(row, f"matrix row {row_index}")
        if binary:
            _validate_binary(row, f"matrix row {row_index}")

    return len(matrix), item_count


def _sample_variance(values: Sequence[Real]) -> float:
    if len(values) < 2:
        raise ValueError("sample variance requires at least two observations")
    _validate_numeric(values, "values")
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def item_difficulty(responses: Sequence[int]) -> float:
    """Return the proportion correct for a binary-scored item."""
    _require_non_empty(responses, "responses")
    _validate_binary(responses, "responses")
    return sum(responses) / len(responses)


def rest_scores(
    matrix: Sequence[Sequence[int]],
    item_index: int,
) -> list[int]:
    """Return each respondent's total score excluding the focal item."""
    _, item_count = _validate_matrix(matrix, binary=True)
    if not 0 <= item_index < item_count:
        raise IndexError("item_index is outside the response matrix")

    return [
        sum(row[:item_index]) + sum(row[item_index + 1 :])
        for row in matrix
    ]


def _extreme_groups(
    criterion_scores: Sequence[Real],
    *,
    group_fraction: float,
    min_group_size: int,
) -> tuple[list[int], list[int]] | None:
    if not 0 < group_fraction <= 0.5:
        raise ValueError("group_fraction must be greater than 0 and at most 0.5")
    if min_group_size < 1:
        raise ValueError("min_group_size must be at least 1")

    _require_non_empty(criterion_scores, "criterion_scores")
    _validate_numeric(criterion_scores, "criterion_scores")

    respondent_count = len(criterion_scores)
    target_size = max(min_group_size, int(respondent_count * group_fraction))

    if 2 * target_size > respondent_count:
        return None

    ranked = sorted(
        range(respondent_count),
        key=lambda index: criterion_scores[index],
        reverse=True,
    )

    upper_cutoff = criterion_scores[ranked[target_size - 1]]
    lower_cutoff = criterion_scores[ranked[-target_size]]

    upper = [
        index
        for index, score in enumerate(criterion_scores)
        if score >= upper_cutoff
    ]
    lower = [
        index
        for index, score in enumerate(criterion_scores)
        if score <= lower_cutoff
    ]

    # If a broad score tie causes the extreme groups to overlap, there is no
    # defensible separation for this simple upper/lower-group statistic.
    if set(upper) & set(lower):
        return None

    return upper, lower


def item_discrimination(
    responses: Sequence[int],
    criterion_scores: Sequence[Real],
    *,
    group_fraction: float = 1 / 3,
    min_group_size: int = 2,
) -> float | None:
    """Return upper-minus-lower proportion correct using tie-safe score groups.

    The caller should normally provide rest scores rather than totals that
    include the focal item. None means the extreme groups cannot be separated
    defensibly for the supplied sample and settings.
    """
    _require_non_empty(responses, "responses")
    if len(responses) != len(criterion_scores):
        raise ValueError("responses and criterion_scores must have equal length")

    _validate_binary(responses, "responses")
    groups = _extreme_groups(
        criterion_scores,
        group_fraction=group_fraction,
        min_group_size=min_group_size,
    )
    if groups is None:
        return None

    upper, lower = groups
    upper_p = sum(responses[index] for index in upper) / len(upper)
    lower_p = sum(responses[index] for index in lower) / len(lower)
    return upper_p - lower_p


def cronbach_alpha(
    matrix: Sequence[Sequence[Real]],
) -> float | None:
    """Compute Cronbach alpha for a rectangular numeric response matrix.

    None means alpha is not estimable because total scores have zero variance.
    """
    _, item_count = _validate_matrix(matrix)

    columns = [
        [row[index] for row in matrix]
        for index in range(item_count)
    ]
    item_variance = sum(_sample_variance(column) for column in columns)
    totals = [sum(row) for row in matrix]
    total_variance = _sample_variance(totals)

    if math.isclose(total_variance, 0.0, abs_tol=1e-12):
        return None

    return (
        item_count
        / (item_count - 1)
        * (1 - item_variance / total_variance)
    )


def item_review_flags(
    difficulty: float,
    discrimination: float | None,
    *,
    difficult_cutoff: float = 0.20,
    easy_cutoff: float = 0.90,
    low_discrimination_cutoff: float = 0.20,
) -> list[str]:
    """Return transparent review prompts using configurable descriptive cutoffs."""
    if not 0 <= difficulty <= 1:
        raise ValueError("difficulty must be between 0 and 1")
    if not 0 <= difficult_cutoff < easy_cutoff <= 1:
        raise ValueError("difficulty cutoffs must satisfy 0 <= low < high <= 1")
    if not -1 <= low_discrimination_cutoff <= 1:
        raise ValueError("low_discrimination_cutoff must be between -1 and 1")

    flags: list[str] = []

    if difficulty <= difficult_cutoff:
        flags.append("low_proportion_correct")
    elif difficulty >= easy_cutoff:
        flags.append("high_proportion_correct")

    if discrimination is None:
        flags.append("discrimination_not_estimable")
    elif discrimination < 0:
        flags.append("negative_discrimination")
    elif discrimination < low_discrimination_cutoff:
        flags.append("low_discrimination")

    return flags


def analyze_assessment(
    matrix: Sequence[Sequence[int]],
    *,
    group_fraction: float = 1 / 3,
    min_group_size: int = 2,
) -> dict[str, object]:
    """Analyze a binary response matrix with item-level review signals."""
    respondent_count, item_count = _validate_matrix(matrix, binary=True)
    alpha = cronbach_alpha(matrix)

    items = []
    for item_index in range(item_count):
        responses = [row[item_index] for row in matrix]
        criterion = rest_scores(matrix, item_index)
        difficulty = item_difficulty(responses)
        discrimination = item_discrimination(
            responses,
            criterion,
            group_fraction=group_fraction,
            min_group_size=min_group_size,
        )
        flags = item_review_flags(difficulty, discrimination)

        items.append(
            {
                "item_index": item_index,
                "difficulty": difficulty,
                "discrimination": discrimination,
                "review_flags": flags,
            }
        )

    flagged_items = sum(bool(item["review_flags"]) for item in items)

    return {
        "respondent_count": respondent_count,
        "item_count": item_count,
        "cronbach_alpha": alpha,
        "discrimination_method": "upper_lower_groups_using_rest_scores",
        "group_fraction": group_fraction,
        "min_group_size": min_group_size,
        "flagged_item_count": flagged_items,
        "items": items,
    }
