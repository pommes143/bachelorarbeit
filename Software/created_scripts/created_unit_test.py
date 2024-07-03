import unittest
from classes_to_test.contains_negative import contains_negative

class TestContainsNegative(unittest.TestCase):

    def test_contains_negative_with_negative_numbers(self):
        self.assertTrue(contains_negative([13, 324, 123, 87, -4545, 8878, 45]))

    def test_contains_negative_without_negative_numbers(self):
        self.assertFalse(contains_negative([2, 1123, 233]))

    def test_contains_negative_with_empty_list(self):
        self.assertFalse(contains_negative([]))

    def test_contains_negative_with_positive_float_numbers(self):
        self.assertFalse(contains_negative([1.234, 5.67, 0.0, 12.34]))

    def test_contains_negative_with_negative_float_numbers(self):
        self.assertTrue(contains_negative([1.234, -5.67, 0.0, -12.34]))

    def test_contains_negative_with_mixed_integers_and_floats(self):
        self.assertTrue(contains_negative([1, 2.2, 3, -4.4, 5]))

if __name__ == '__main__':
    unittest.main()
