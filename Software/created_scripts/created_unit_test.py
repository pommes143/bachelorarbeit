import unittest
from classes_to_test.contains_negative import contains_negative

class TestContainsNegative(unittest.TestCase):
    
    def test_contains_negative_with_negative_numbers(self):
        self.assertTrue(contains_negative([13, 324, 123, 87, -4545, 8878, 45]))
        
    def test_contains_negative_without_negative_numbers(self):
        self.assertFalse(contains_negative([2, 1123, 233]))
        
    def test_contains_negative_with_empty_list(self):
        self.assertFalse(contains_negative([]))
        
    def test_contains_negative_with_negative_float_numbers(self):
        self.assertTrue(contains_negative([1.5, -2.4, 3.0, 5.7]))
        
    def test_contains_negative_with_only_one_negative_number(self):
        self.assertTrue(contains_negative([-1]))
        
    def test_contains_negative_with_only_positive_float_numbers(self):
        self.assertFalse(contains_negative([0.2, 5.9, 3.3]))
        
    def test_contains_negative_with_mixed_integer_and_float_numbers(self):
        self.assertTrue(contains_negative([1, 2, -3.5, 4]))
        
    def test_contains_negative_with_large_numbers(self):
        self.assertFalse(contains_negative([999999999999999, 888888888888, 777777777777, 66666666666]))
        
if __name__ == '__main__':
    unittest.main()
