#!function!#
import numpy as np 
def get_corner_sums(array1, array2):
    # Convert input lists to NumPy arrays
    array1 = np.array(array1)
    array2 = np.array(array2)
    
    n1, m1 = array1.shape
    n2, m2 = array2.shape
    left_bottom_sum = int(array1[n1-1, 0] + array2[n2-1, 0])
    right_top_sum = int(array1[0, m1-1] + array2[0, m2-1])
    return left_bottom_sum, right_top_sum
