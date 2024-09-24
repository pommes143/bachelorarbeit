from example_solution import eigen_of_diagonal as eigen_of_diagonal
import numpy as np
#!cut_imports!#

def test_eigen_of_diagonal():
    # Test case 1: Check if the function correctly computes eigenvalues and eigenvectors
    input_matrix1 = np.array([[4, -2, 0],
                            [1,  1, 0],
                            [0,  0, 2]])
    eigenvalues1, eigenvectors1 = eigen_of_diagonal(input_matrix1)
    
    # Expected eigenvalues of the diagonal matrix
    expected_eigenvalues1 = np.array([4, 1, 2])
    
    # Eigenvectors of a diagonal matrix are the standard basis vectors
    expected_eigenvectors1 = np.array([[1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 1]])
    
    assert np.allclose(eigenvalues1, expected_eigenvalues1), "Test case 1 (eigenvalues) failed"
    assert np.allclose(eigenvectors1, expected_eigenvectors1), "Test case 1 (eigenvectors) failed"
