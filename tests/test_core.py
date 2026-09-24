import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from assessment_design_lab import core


class CoreTests(unittest.TestCase):
    def test_item_statistics(self):
        self.assertAlmostEqual(core.item_difficulty([1, 1, 0, 0]), 0.5)
        self.assertGreaterEqual(core.item_discrimination([1, 1, 0, 0], [4, 3, 2, 1]), 0)

    def test_reliability_and_validation(self):
        self.assertAlmostEqual(core.cronbach_alpha([[1, 1, 0], [1, 1, 1], [0, 0, 0], [0, 1, 0]]), 0.75)
        with self.assertRaises(ValueError):
            core.item_difficulty([])


if __name__ == "__main__":
    unittest.main()
