import unittest
from example_solution import contains_negative

class TestContainsNegative(unittest.TestCase):
    
    def test_positive_numbers(self):
        self.assertFalse(contains_negative([1, 2, 3, 4, 5]))

    def test_mixed_numbers(self):
        self.assertTrue(contains_negative([1, -2, 3, -4, 5]))

    def test_all_negative_numbers(self):
        self.assertTrue(contains_negative([-1, -2, -3, -4, -5]))

if __name__ == '__main__': # pragma: no cover
    unittest.main()