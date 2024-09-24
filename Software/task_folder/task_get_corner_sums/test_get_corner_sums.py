from example_solution import get_corner_sums as get_corner_sums
import numpy as np
#!cut_imports!#

def test_get_corner_sums():
    # Test case 1: Check if the function correctly computes corner sums
    array1 = np.array([[1, 2, 3],
                       [4, 5, 6]])

    array2 = np.array([[7, 8, 9],
                       [10, 11, 12]])

    result = get_corner_sums(array1, array2)
    expected_result = (14, 12)
    assert result == expected_result, "It seems that the sum is not calculated correctly."

    # Test case 2: Check if the function handles arrays with different shapes
    array3 = np.array([[1, 2, 3],
                       [4, 5, 6]])

    array4 = np.array([[7, 8, 9, 10],
                       [11, 12, 13, 14]])

    result2 = get_corner_sums(array3, array4)
    expected_result2 = (15, 13)
    assert result2 == expected_result2, "It seems that the case of matrices of different sizes is not accounted for."