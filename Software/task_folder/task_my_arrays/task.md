# Numpy
## What is Numpy?

Python has a rich ecosystem of modules and libraries, each designed to solve specific problems or provide specific functionality. You can also create your own modules by organizing your code into separate .py files and then importing them into your scripts when needed. NumPy is one of such packages. It aims to be the fundamental high-level building block for doing practical, real world data analysis in Python.

```python
import numpy as np

my_vector = np.array([1, 2, 3])  # Create a new vector with 3 elements (3d)

print(my_vector)
print(type(my_vector))
print(my_vector.shape)
```
```
[1 2 3]
<class 'numpy.ndarray'>
(3,)
```
```python
np.zeros(5)  # Note: Shape must be specified as a tuple!
```
```
array([0., 0., 0., 0., 0.])
```

## To Do

Write a function, that will be producing following returns based on the input integer *n*:

```python
def my_arrays(n):
    
```
1. Create an array of zeros of the size *n*.
2. Create an array of ones of the size *n*.
3. Create an array of fives of the size *n*.
4. Return None for negative **n**.

(**HINT** np.zeros(), np.ones() can be quite useful here)
**Note** This pre-alpha version can only use primitive python types as argumrnts for "run". Please provide the arguments as list and transform them in your function body via np.array().