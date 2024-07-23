import unittest
import numpy as np
from example_solution import apply_mask

class TestApplyMaskFunction(unittest.TestCase):
    def test_correct_mask_inversion(self):
        original_array = np.array([1, 2, 3, 4, 5])
        mask = np.array([True, False, True, False, True])
        
        result = apply_mask(original_array, mask)
        expected_result = np.array([2, 4])
        
        self.assertTrue(np.array_equal(result, expected_result))
    
    def test_mask_size_mismatch(self):
        original_array = np.array([1, 2, 3, 4, 5])
        mask = np.array([True, False, True])
        
        result = apply_mask(original_array, mask)
        
        self.assertIsNone(result)
    
    def test_no_elements_selected(self):
        original_array = np.array([1, 2, 3, 4, 5])
        mask = np.array([True, True, True, True, True])
        
        result = apply_mask(original_array, mask)
        
        self.assertTrue(np.array_equal(result, np.array([])))

    def test_some_elements_selected(self):
        original_array = np.array([1, 2, 3, 4, 5])
        mask = np.array([False, True, False, True, False])
        
        result = apply_mask(original_array, mask)
        expected_result = np.array([1, 3, 5])
        
        self.assertTrue(np.array_equal(result, expected_result))

if __name__ == '__main__':
    unittest.main()