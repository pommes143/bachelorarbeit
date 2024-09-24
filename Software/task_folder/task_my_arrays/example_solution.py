#!function!#
import numpy as np 
def my_arrays(n):
#!prefix!#
    if n <= 0:
        return None  # Return None for invalid input
    
    # Create an array of zeros of size n
    zeros_array = np.zeros(n)

    # Create an array of ones of size n
    ones_array = np.ones(n)

    # Create an array of fives of size n
    fives_array = np.full(n, 5)

    return zeros_array, ones_array, fives_array
