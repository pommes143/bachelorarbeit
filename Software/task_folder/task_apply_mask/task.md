# Masks
## Evaluating a boolean expression
A NumPy mask array is a Boolean array used to filter or select specific elements from another array. This powerful tool facilitates data manipulation by enabling the extraction of data based on specific conditions.

```python
import numpy as np  
mat = np.eye(4)
print(mat)

# Evaluate a boolean expression for each element
print(mat > 0)

# Use a mask
mask = mat > 0  # Evaluate boolean expression
print(mat[mask]) # Select all items/entries for which the expression yields True
```
```
[[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]
[[ True False False False]
 [False  True False False]
 [False False  True False]
 [False False False  True]]
[1. 1. 1. 1.]
```
## Evaluating a boolean expression

Create a function that takes a NumPy array and a mask array as inputs. The function should return a new array containing elements from the original array that correspond to False values in the mask array. (**HINT** it can be useful to invert the input mask for this). Please return None if the mask does not math the array.
```python
def apply_mask(input_array, mask):
    ...
```