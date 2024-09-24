# Sums and shapes
## Rows and columns
In NumPy arrays, axes refer to the dimensions along which the elements of the array are indexed. NumPy arrays can have one or more axes, and each axis is identified by a non-negative integer.
```python
# Sum over rows or columns
my_matrix = np.array([[1, 2], [3, 4]])  # Create a new 2x2 matrix
print(my_matrix)

print(np.sum(my_matrix, axis=0))  # Sum of each column
print(np.sum(my_matrix, axis=1))  # Sum of each row
```
```
[[1 2]
 [3 4]]
[4 6]
[3 7]
```
## Reshaping 
You can reshape NumPy arrays by rearranging the elements along different axes. This is often used for preparing data for specific operations or calculations.
```python
# Change the shape of an array
print(my_matrix)
print(my_matrix.shape)

new_matrix = my_matrix.reshape((4,))  # Reshape matrix to a flat array (=> vector)
print(new_matrix)
print(new_matrix.shape)
```
```
[[1 2]
 [3 4]]
(2, 2)
[1 2 3 4]
(4,)
```
## To Do

Create a Python function that takes a 1D NumPy array as input. The function should reshape the 1D array into a 2D matrix with a specified number of rows and columns. After reshaping, calculate and return the row sums and column sums of the resulting matrix. in case if the array cannot be converted to the matrix of the requested shape, return None. 
```python
def reshape_and_sum(input_array, num_rows, num_columns):
    ...
    return row_sums, column_sums
```
