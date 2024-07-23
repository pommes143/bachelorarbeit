import numpy as np

def apply_mask(input_array, mask):
    # Check if the dimensions match
    if input_array.shape[0] != mask.shape[0]:
        return None
    # Handle empty arrays
    if input_array.size == 0 or mask.size == 0:
        return np.array([])  # Return empty array for empty inputs
    return input_array[mask]  # Apply the mask
