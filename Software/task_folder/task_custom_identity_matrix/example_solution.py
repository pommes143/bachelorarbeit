#!function!#
import numpy as np 
def custom_identity_matrix(n, value):
#!prefix!#

    if n <= 0:
        return None  # Return None for invalid input
    
    # Create an identity matrix of size n x n with diagonal elements set to the specified value
    identity_matrix = np.eye(n) * value

    return identity_matrix