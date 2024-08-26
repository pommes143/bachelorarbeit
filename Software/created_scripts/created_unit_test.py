import unittest
from example_solution import contains_negative  # assuming you have this line in your file

class TestContainsNegative(unittest.TestCase):

    def test_no_negative_numbers(self):
        self.assertFalse(contains_negative([1, 2, 3, 4, 5]), "There is no negative numbers in [1, 2, 3, 4, 5]")

    def test_has_negative_number(self):
        self.assertTrue(contains_negative([1, 2, -3, 4, 5]), "There is a negative number in [1, 2, -3, 4, 5]")

    def test_empty_list(self):
        self.assertFalse(contains_negative([]), "An empty list should not contain negative numbers")

    def test_only_negative_number(self):
        self.assertTrue(contains_negative([-5]), "A list containing only a negative number should return True")

    def test_multiple_negative_numbers(self):
        self.assertTrue(contains_negative([1, -2, -3, 4, -5]), "Multiple negative numbers in the list should return True")

if __name__ == '__main__': # pragma: no cover
    unittest.main()