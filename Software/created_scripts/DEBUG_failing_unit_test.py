import unittest
from classes_to_test.contains_negative import contains_negative

class TestContainsNegative(unittest.TestCase):
    
    def test_negative_numbers_exist(self):
        self.assertTrue(contains_negative([-3, 5, 2, -8]))
        self.assertTrue(contains_negative([0, -1, 7, 4]))
    
    def test_no_negative_numbers(self):
        self.assertFalse(contains_negative([10, 20, 30]))
        self.assertFalse(contains_negative([0, 1, 2, 3]))
    
    def test_float_numbers(self):
        self.assertTrue(contains_negative([3.5, -2.5, 1.1]))
        self.assertFalse(contains_negative([5.6, 8.9, 4.3]))
    
    def test_empty_list(self):
        self.assertFalse(contains_negative([]))
    
    def test_edge_cases(self):
        self.assertTrue(contains_negative([-1]))
        self.assertFalse(contains_negative([0]))
        self.assertTrue(contains_negative([-0.5, 0.1, 0.9]))
        self.assertTrue(contains_negative([-0.0, 1.0]))

if __name__ == '__main__':
    unittest.main()
