from example_solution import my_arrays as my_arrays
import numpy as np
#!cut_imports!#
def test_my_arrays():
    # Test case 1: Check if the function correctly creates arrays for a positive n
    n1 = 5
    zeros_array1, ones_array1, fives_array1 = my_arrays(n1)
    expected_zeros1 = np.zeros(n1)
    expected_ones1 = np.ones(n1)
    expected_fives1 = np.full(n1, 5)
    
    assert np.array_equal(zeros_array1, expected_zeros1), "Error in creation of the array of zeros"
    assert np.array_equal(ones_array1, expected_ones1), "Error in creation of the array of ones"
    assert np.array_equal(fives_array1, expected_fives1), "Error in creation of the array of fives"

    # Test case 2: Check if the function handles n <= 0 by returning None
    n2 = -3
    result2 = my_arrays(n2)
    assert result2 is None, "The function does not return None for negative integers. Please account for this case!"


