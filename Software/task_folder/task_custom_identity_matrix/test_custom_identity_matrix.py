from example_solution import custom_identity_matrix as custom_identity_matrix
import numpy as np
#!cut_imports!#
def test_custom_identity_matrix():
    # Test is arbitrary, but you should use assert.
    n = 3
    custom_value = 2
    result = custom_identity_matrix(n, custom_value)
    expected_result = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
    assert np.array_equal(result, expected_result), "Test case 1 (3x3 matrix, value 2) failed"

    # Test case 2: Check if a custom identity matrix with value 5 is generated for n = 2
    n = 2
    custom_value = 5
    result = custom_identity_matrix(n, custom_value)
    expected_result = np.array([[5, 0], [0, 5]])
    assert np.array_equal(result, expected_result), "Test case 2 (2x2 matrix, value 5) failed"

    # Test case 3: Check if None is returned for n = 0
    n = 0
    custom_value = 3
    result = custom_identity_matrix(n, custom_value)
    assert result is None, "Test case 3 (impossible matrix) failed"