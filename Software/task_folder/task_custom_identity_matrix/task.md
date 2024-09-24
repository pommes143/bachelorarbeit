# Matrices
## Built in functions
The arrays do not have to be one dimensional. Rather, and array (you can also see ndarray in Numpy context) refers to an array of a deliberate dimensionality. A popular option for this are matrices: two-dimensional arrays.
```python
import numpy as np 
# Create arrays: Use build in functions
print(np.eye(3))
np.zeros((5,3))  # Note: Shape must be specified as a tuple!
```
```
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]

array([[0., 0., 0.],
       [0., 0., 0.],
       [0., 0., 0.],
       [0., 0., 0.],
       [0., 0., 0.]])
 ```
 ## To Do

Create a function that generates an identity matrix of a specified size, where all diagonal elements are set to a specific value other than 1.

```python
def custom_identity_matrix(n, value):
    ...
```
If the matrix cannot be created (negative n), return None. 