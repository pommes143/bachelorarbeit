# Entries and indexation 
## Slicing 
Entries can be accessed with the indexes. The indexation starts from [0] and can be applied to all the axises of the target array. 
```python
import numpy as np   
my_matrix = np.array([[1, 2], [3, 4]])  # Create a new 2x2 matrix

print(my_matrix)
print(my_matrix.shape)
```
```
[[1 2]
 [3 4]]
(2, 2)
```
```python
# Access entries
print(my_matrix[0,0])
print(my_matrix[0,1])

my_vector = np.array([6, 7, 8]) 
print(my_vector[2])
my_vector[2] = 42  # Change an entry
print(my_vector)

# Slicing
print(my_matrix[0,:])  # First row
print(my_matrix[:, 0]) # First column
print(my_matrix[:, 1])  # Second column
```
```
1
2
8
[ 6  7 42]
[1 2]
[1 3]
[2 4][[1 2]
 [3 4]]
(2, 2)
```

## To Do 

For 2 input 2D arrays (matrices), please write a function, that will be returning the results of the sum of the elements in the left bottom corner of the matrices, and then thoose of the right top corner. 
```python
def get_corner_sums(array1, array2):
    ...
```