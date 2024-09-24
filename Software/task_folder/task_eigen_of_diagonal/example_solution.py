#!function!#
import numpy as np 
def eigen_of_diagonal(matrix):
#!prefix!#
    # Extract the diagonal elements
    diagonal = np.diag(np.diag(matrix))
    
    # Compute eigenvalues and eigenvectors of the diagonal matrix
    eigenvalues, eigenvectors = np.linalg.eig(diagonal)
    
    return eigenvalues, eigenvectors


