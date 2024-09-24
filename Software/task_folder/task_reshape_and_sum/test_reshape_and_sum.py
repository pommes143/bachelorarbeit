from example_solution import reshape_and_sum as reshape_and_sum
import numpy as np
#!cut_imports!#
def test_reshape_and_sum():
    # Test case 1: Check if the function correctly reshapes and calculates sums
    input_array1 = np.array([1, 2, 3, 4, 5, 6])
    num_rows1 = 2
    num_columns1 = 3
    row_sums1, column_sums1 = reshape_and_sum(input_array1, num_rows1, num_columns1)
    expected_row_sums1 = np.array([6, 15])
    expected_column_sums1 = np.array([5, 7, 9])
    assert np.array_equal(row_sums1, expected_row_sums1), "The row sums are not calculated correctly."
    assert np.array_equal(column_sums1, expected_column_sums1), "The column sums are not calculated correctly."

    # Test case 2: Check if the function handles incompatible dimensions
    input_array2 = np.array([1, 2, 3, 4, 5, 6, 7])
    num_rows2 = 2
    num_columns2 = 3
    result2 = reshape_and_sum(input_array2, num_rows2, num_columns2)
    assert result2 is None, "It seems that there is no check whether the array can be reshaped."