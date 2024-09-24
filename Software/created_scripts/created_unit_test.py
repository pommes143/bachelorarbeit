import unittest
from example_solution import contains_negative

class TestContainsNegative(unittest.TestCase):

    def test_no_negative_numbers(self):
        self.assertEqual(contains_negative([1, 2, 3, 4, 5]), False, "There are no negative numbers in [1, 2, 3, 4, 5]")

    def test_contains_negative_numbers(self):
        self.assertEqual(contains_negative([1, 2, -3, 4, 5]), True, "There is a negative number in [1, 2, -3, 4, 5]")

    def test_empty_list(self):
        self.assertEqual(contains_negative([]), False, "Empty list should return False")

if __name__ == '__main__': # pragma: no cover
    unittest.main()