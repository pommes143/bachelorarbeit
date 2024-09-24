# Linear algebra
## Linalg
The NumPy linear algebra subpackage (numpy.linalg) provide efficient low level implementations of standard linear algebra algorithms. 
For example, in you can solve systems of linear equations

2x₀ + 3x₁ = 1
3x₀ + 4x₁ = 1

```python 
import numpy as np

a = np.array([[2, 3], [3, 4]])

b = np.array([1, 1])

x = np.linalg.solve(a, b)

print(x)
```
```
[-1.  1.]
```
## To Do

Write a function, that for has a matrix as an argument and: 
1. Removes all the values but diagonal (**np.diag()** can be helpful here)
2. Computes eigenvalues and eigenvectors of the new diagonal matrix (**np.linalg.eig()** is worth checking out)

Please use the following format:

```python
def eigen_of_diagonal(matrix):
    ...
```