import unittest
import numpy as np
from example_solution import apply_mask

class TestApplyMaskFunction(unittest.TestCase):

    def test_apply_mask_valid(self):
        input_array = np.array([1, 2, 3, 4, 5])
        mask_array = np.array([False, True, False, True, False])
        expected_output = np.array([1, 3, 5])
        
        result = apply_mask(input_array, mask_array)
        
        self.assertTrue(np.array_equal(result, expected_output))

    def test_apply_mask_invalid(self):
        input_array = np.array([1, 2, 3, 4, 5])
        mask_array = np.array([False, True, False, True])
        
        result = apply_mask(input_array, mask_array)
        
        self.assertIsNone(result)

    def test_apply_mask_empty_mask(self):
        input_array = np.array([1, 2, 3, 4, 5])
        mask_array = np.array([])
        
        result = apply_mask(input_array, mask_array)
        
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
