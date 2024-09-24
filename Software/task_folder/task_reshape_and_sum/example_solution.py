#!function!#
import numpy as np 
def reshape_and_sum(input_array, num_rows, num_columns):
#!prefix!#
    if num_rows * num_columns != input_array.size:
        return None  # Return None for incompatible dimensions

    # Reshape the input array into a matrix
    reshaped_matrix = input_array.reshape((num_rows, num_columns))

    # Calculate row sums and column sums
    row_sums = np.sum(reshaped_matrix, axis=1)
    column_sums = np.sum(reshaped_matrix, axis=0)

    return row_sums, column_sums