# Trigonometric functions
## np.sin(), np.cos(), np.tan()
Numpy is a rich library with a variaty of in-built functions. In particular, trigonometric functions. 
```python
import numpy as np
x = np.array([0., 1., 30, 90])
print("sine:", np.sin(x),
      "\ncosine:", np.cos(x),
      "\ntangent:", np.tan(x))
```

```
sine: [ 0.          0.84147098 -0.98803162  0.89399666] 
cosine: [ 1.          0.54030231  0.15425145 -0.44807362] 
tangent: [ 0.          1.55740772 -6.4053312  -1.99520041]
```

## To Do

Create a function that for an input array of angles (in degrees) returns sin, cos, and tan for each element.  

```python
def trigonometry(angle_array):
    ...
```
(**HINT** as you can see  in the example above, trigonometric functions take the values in radians. There are several methods for the conversion, for example, **np.pi** can be quite helpful here.)