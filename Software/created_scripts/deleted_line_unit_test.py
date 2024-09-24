import numpy as np
import unittest
from example_solution import apply_mask

class TestApplyMaskFunction(unittest.TestCase):
    def test_correct_mask_inversion(self):
        original_array = np.array([1, 2, 3, 4, 5])
        mask = np.array([True, False, True, False, True])
        result = apply_mask(original_array, mask)
        expected_result = np.array([2, 4])
        self.assertTrue(np.array_equal(result, expected_result))

    def test_empty_input(self):
        original_array = np.array([])
        mask = np.array([])
        result = apply_mask(original_array, mask)
        expected_result = np.array([])
        self.assertTrue(np.array_equal(result, expected_result))

if __name__ == '__main__': # pragma: no cover # pragma: no cover
    unittest.main()