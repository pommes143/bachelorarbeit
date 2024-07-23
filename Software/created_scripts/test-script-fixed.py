import numpy as np

def apply_mask(original_array, mask):
    if len(original_array) != len(mask):
        return None
    masked_array = original_array[mask]
    return masked_array

# Unit Test
def test_apply_mask():
    original_array = np.array([1, 2, 3, 4, 5])
    mask = np.array([True, False, True, False, True])
    expected_result = np.array([2, 4])
    result = apply_mask(original_array, mask)
    assert np.array_equal(result, expected_result)

    original_array = np.array([1, 2, 3, 4, 5])
    mask = np.array([True, False, True])
    result = apply_mask(original_array, mask)
    assert result is None

    original_array = np.array([10, 20, 30, 40, 50])
    mask = np.array([False, True, False, True, False])
    expected_result = np.array([20, 40])
    result = apply_mask(original_array, mask)
    assert np.array_equal(result, expected_result)

    original_array = np.array([100, 200, 300, 400, 500])
    mask = np.array([False, False, False, False, False])
    expected_result = np.array([])
    result = apply_mask(original_array, mask)
    assert np.array_equal(result, expected_result)

test_apply_mask()
