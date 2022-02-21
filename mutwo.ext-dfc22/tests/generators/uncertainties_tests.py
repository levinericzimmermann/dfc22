import collections
import unittest

from mutwo import dfc22_generators


class UncertainSetTest(unittest.TestCase):
    def test_resolve(self):
        number_list = [1, 2, 3]
        uncertain_set = dfc22_generators.UncertainSet(number_list)
        self.assertTrue(uncertain_set.resolve() in number_list)
        counter = collections.Counter()
        for _ in range(1000):
            counter.update({uncertain_set.resolve(): 1})

        for number in number_list:
            self.assertTrue(number in counter)


if __name__ == "__main__":
    unittest.main()
