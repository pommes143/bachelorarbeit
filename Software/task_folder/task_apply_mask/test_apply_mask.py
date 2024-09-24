from example_solution import apply_mask as apply_mask
import numpy as np
#!cut_imports!#
def test_apply_mask():
    # Test case 1: Check if the inverted mask selects elements in the original array
    original_array = np.array([1, 2, 3, 4, 5])
    mask = np.array([True, False, True, False, True])
    result = apply_mask(original_array, mask)
    
    expected_result = np.array([2, 4])
    assert np.array_equal(result, expected_result), "There is something wrong with the main function. Did you invert the mask?"

    # Test case 2: Check if the function returns None for mismatched shapes
    original_array = np.array([1, 2, 3, 4, 5])
    mask = np.array([True, False, True])
    result = apply_mask(original_array, mask)
    assert result is None, "The case for the mismatch in sizes of the array and the mask is not accounted for."

    # Test case 3: Check if the inverted mask selects all elements in the original array
    original_array = np.array([1, 2, 3, 4, 5])
    mask = np.array([False, False, False, False, False])
    result = apply_mask(original_array, mask)
    expected_result = original_array
    assert np.array_equal(result, expected_result), "The case for the mismatch in sizes of the array and the mask is not accounted for."

    original_matrix = np.array([[1, 2], [3, 4], [5, 6]])
    mask4 = np.array([[True, False], [False, True], [True, False]])
    result4 = apply_mask(original_matrix, mask4)
    expected_result4 = np.array([2, 3, 6])
    assert np.array_equal(result4, expected_result4), "It seems that your program does not work properly for higher dimensions (matrices)."
