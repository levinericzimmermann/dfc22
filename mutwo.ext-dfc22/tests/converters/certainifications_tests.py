import unittest

from mutwo import dfc22_converters
from mutwo import dfc22_generators


class SymmetricalSpecifyUncertainRangeTest(unittest.TestCase):
    def test_convert_equal(self):
        uncertain_range = dfc22_generators.UncertainRange(1, 2)
        specify_symmetrical_range = dfc22_converters.SymmetricalSpecifyUncertainRange(0)
        self.assertEqual(
            specify_symmetrical_range.convert(uncertain_range, 2),
            (
                dfc22_generators.UncertainRange(1, 1.5),
                dfc22_generators.UncertainRange(1.5, 2),
            ),
        )
        self.assertEqual(
            specify_symmetrical_range.convert(uncertain_range, 4),
            (
                dfc22_generators.UncertainRange(1, 1.25),
                dfc22_generators.UncertainRange(1.25, 1.5),
                dfc22_generators.UncertainRange(1.5, 1.75),
                dfc22_generators.UncertainRange(1.75, 2),
            ),
        )

    def test_convert_with_gap(self):
        uncertain_range = dfc22_generators.UncertainRange(1, 4)
        specify_symmetrical_range = dfc22_converters.SymmetricalSpecifyUncertainRange(-1)
        self.assertEqual(
            specify_symmetrical_range.convert(uncertain_range, 2),
            (
                dfc22_generators.UncertainRange(1, 2),
                dfc22_generators.UncertainRange(3, 4),
            ),
        )
        uncertain_range = dfc22_generators.UncertainRange(2, 7)
        self.assertEqual(
            specify_symmetrical_range.convert(uncertain_range, 3),
            (
                dfc22_generators.UncertainRange(2, 3),
                dfc22_generators.UncertainRange(4, 5),
                dfc22_generators.UncertainRange(6, 7),
            ),
        )

    def test_convert_with_overlap(self):
        uncertain_range = dfc22_generators.UncertainRange(1, 4)
        specify_symmetrical_range = dfc22_converters.SymmetricalSpecifyUncertainRange(1)
        self.assertEqual(
            specify_symmetrical_range.convert(uncertain_range, 2),
            (
                dfc22_generators.UncertainRange(1, 3),
                dfc22_generators.UncertainRange(2, 4),
            ),
        )
        uncertain_range = dfc22_generators.UncertainRange(2, 7)
        self.assertEqual(
            specify_symmetrical_range.convert(uncertain_range, 3),
            (
                dfc22_generators.UncertainRange(2, 4),
                dfc22_generators.UncertainRange(3, 6),
                dfc22_generators.UncertainRange(5, 7),
            ),
        )


if __name__ == "__main__":
    unittest.main()
