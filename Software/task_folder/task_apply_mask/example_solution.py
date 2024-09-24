#!function!#
import numpy as np 
def apply_mask(input_array, mask):
#!prefix!#
    if input_array.shape != mask.shape:
        return None  # Return None for mismatched shapes
    
    # Invert the input mask
    inverted_mask = ~mask

    # Use the inverted mask to select elements from the input array
    result_array = input_array[inverted_mask]

    return result_array
