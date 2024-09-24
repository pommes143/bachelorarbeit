# Importing Modules in Python
## Modules

Modules in Python are files containing Python code, functions, and variables that can be reused in other Python scripts or programs. 
They allow you to organize your code into separate files, making it more modular and maintainable. Modules help avoid code duplication and promote code reuse.


```python
import math   # Import the module 'math'
math.sqrt(25)  # Call a function from the module (in this case function 'sqrt' from the module 'math')
```
One example for an equation

$$ s=\sqrt{25} $$

```python
from math import sqrt  # Import the function 'sqrt' from the module 'math'
print(sqrt(25))   # NOTE: We do not need to specify the module any more! (Be aware of naming conflicts)
```
```
5
```
In there introductory modules, we will be importing the packages for you, but please be aware that for coding outside the ITS you would have to install and call them before using!

## To Do 

Create a function that finds the largest perfect square (a number that is a square of an integer) in a list of numbers and returns it. If no perfect square is found, the function should return None. 

You can implement this task with the following function using the **math.isqrt()** function from the **math** package to check if a number is a perfect square, but feel free to explore other options!

```python
def largest_perfect_square(numbers):
    ...
```