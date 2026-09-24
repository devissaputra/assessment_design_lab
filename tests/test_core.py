import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from assessment_design_lab import core


MATRIX = [
    [1, 1, 1, 1],
    [1, 1, 1, 0],
    [1, 1, 0, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
]


class CoreTests(unittest.TestCase):
    def test_item_difficulty(self):
        self.assertAlmostEqual(core.item_difficulty([1, 1, 0, 0]), 0.5)

    def test_item_difficulty_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            core.item_difficulty([])

    def test_item_difficulty_rejects_non_binary_values(self):
        with self.assertRaises(ValueError):
            core.item_difficulty([1, 0, 2])

    def test_item_difficulty_rejects_boolean_values(self):
        with self.assertRaises(ValueError):
            core.item_difficulty([1, True, 0])

    def test_rest_scores_exclude_focal_item(self):
        matrix = [[1, 1, 0], [0, 1, 1]]
        self.assertEqual(core.rest_scores(matrix, 1), [1, 1])

    def test_rest_scores_validate_item_index(self):
        with self.assertRaises(IndexError):
            core.rest_scores([[1, 0], [0, 1]], 2)

    def test_discrimination_uses_score_only_for_ranking(self):
        responses = [1, 0, 1, 0, 1, 0]
        scores = [3, 3, 2, 2, 1, 1]
        result = core.item_discrimination(
            responses,
            scores,
            group_fraction=1 / 3,
            min_group_size=2,
        )
        self.assertAlmostEqual(result, 0.0)

    def test_discrimination_returns_none_when_groups_overlap_on_ties(self):
        result = core.item_discrimination(
            [1, 0, 1, 0],
            [2, 2, 2, 2],
            group_fraction=0.5,
            min_group_size=1,
        )
        self.assertIsNone(result)

    def test_discrimination_rejects_mismatched_lengths(self):
        with self.assertRaises(ValueError):
            core.item_discrimination([1, 0], [2])

    def test_discrimination_rejects_invalid_fraction(self):
        with self.assertRaises(ValueError):
            core.item_discrimination([1, 0, 1, 0], [3, 2, 1, 0], group_fraction=0)

    def test_cronbach_alpha_matches_reference_example(self):
        alpha = core.cronbach_alpha(
            [[1, 1, 0], [1, 1, 1], [0, 0, 0], [0, 1, 0]]
        )
        self.assertAlmostEqual(alpha, 0.75)

    def test_cronbach_alpha_returns_none_for_zero_total_variance(self):
        self.assertIsNone(core.cronbach_alpha([[1, 0], [1, 0], [1, 0]]))

    def test_cronbach_alpha_rejects_ragged_matrix(self):
        with self.assertRaises(ValueError):
            core.cronbach_alpha([[1, 0], [1]])

    def test_cronbach_alpha_rejects_non_finite_values(self):
        with self.assertRaises(ValueError):
            core.cronbach_alpha([[1.0, math.nan], [0.0, 1.0]])

    def test_item_review_flags_are_transparent(self):
        self.assertEqual(
            core.item_review_flags(0.95, -0.10),
            ["high_proportion_correct", "negative_discrimination"],
        )

    def test_item_review_flags_handle_unestimable_discrimination(self):
        self.assertIn(
            "discrimination_not_estimable",
            core.item_review_flags(0.5, None),
        )

    def test_analyze_assessment_uses_rest_score_discrimination(self):
        result = core.analyze_assessment(MATRIX)
        self.assertEqual(result["respondent_count"], 9)
        self.assertEqual(result["item_count"], 4)
        self.assertEqual(
            result["discrimination_method"],
            "upper_lower_groups_using_rest_scores",
        )
        self.assertEqual(len(result["items"]), 4)
        self.assertAlmostEqual(result["items"][0]["difficulty"], 5 / 9)
        self.assertAlmostEqual(result["items"][0]["discrimination"], 0.55)

    def test_analyze_assessment_flags_low_discrimination(self):
        result = core.analyze_assessment(MATRIX)
        flags = result["items"][2]["review_flags"]
        self.assertIn("low_discrimination", flags)

    def test_analyze_assessment_rejects_non_binary_matrix(self):
        with self.assertRaises(ValueError):
            core.analyze_assessment([[1, 0], [0, 2]])


if __name__ == "__main__":
    unittest.main()
