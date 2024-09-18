import unittest
from example_solution import contains_negative

class TestContainsNegative(unittest.TestCase):
    def test_all_positive_numbers(self):
        self.assertFalse(contains_negative([1, 2, 3, 4, 5]), "There should be no negative numbers in [1, 2, 3, 4, 5]")

    def test_mixed_positive_and_negative_numbers(self):
        self.assertTrue(contains_negative([1, 2, -3, 4, 5]), "There should be a negative number in [1, 2, -3, 4, 5]")

    def test_empty_list(self):
        self.assertFalse(contains_negative([]), "An empty list should not contain negative numbers")

if __name__ == '__main__': # pragma: no cover
    unittest.main()