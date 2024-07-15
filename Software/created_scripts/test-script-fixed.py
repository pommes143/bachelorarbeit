import unittest
from classes_to_test.contains_negative import contains_negative

class TestContainsNegative(unittest.TestCase):

    def test_contains_negative_with_negative_numbers(self):
        self.assertTrue(contains_negative([13, 324, 123, 87, -4545, 8878, 45]))

    def test_contains_negative_without_negative_numbers(self):
        self.assertFalse(contains_negative([2, 1123, 233]))

    def test_contains_negative_with_floats(self):
        self.assertTrue(contains_negative([13, 324, 123, 87, -45.45, 8878, 45]))

    def test_contains_negative_with_mixed_integers_and_floats(self):
        self.assertTrue(contains_negative([13, 324, 123, 87, -45.45, 8878, 45, -10]))

    def test_contains_negative_with_empty_list(self):
        self.assertFalse(contains_negative([]))

    def test_contains_negative_with_zero(self):
        self.assertFalse(contains_negative([0]))

    def test_contains_negative_with_negative_zero(self):
        self.assertTrue(contains_negative([-0.0]))  # Change it from [-0] to [-0.0]

    def test_contains_negative_with_negative_inf(self):
        self.assertTrue(contains_negative([-float('inf')]))

    def test_contains_negative_with_positive_inf(self):
        self.assertFalse(contains_negative([float('inf')]))

    def test_contains_negative_with_nan(self):
        self.assertFalse(contains_negative([float('nan')]))

if __name__ == '__main__':
    unittest.main()
