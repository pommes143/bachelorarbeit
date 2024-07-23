import unittest
from example_solution import contains_negative

class TestContainsNegative(unittest.TestCase):

    def test_contains_negative_with_negatives(self):
        numbers = [1, 2, -3, 4, 5]
        self.assertTrue(contains_negative(numbers))

    def test_contains_negative_without_negatives(self):
        numbers = [1, 2, 3, 4, 5]
        self.assertFalse(contains_negative(numbers))

    def test_contains_negative_empty_list(self):
        numbers = []
        self.assertFalse(contains_negative(numbers))

    def test_contains_negative_with_only_negatives(self):
        numbers = [-1, -2, -3]
        self.assertTrue(contains_negative(numbers))

if __name__ == '__main__':
    unittest.main()
