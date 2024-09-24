# Random samples
## numpy.random
**numpy.random** is another subpackage, which can be used to generate random elements. 
```python
import numpy as np
die_rolls = np.random.randint(1, 50) # generate a random integer between 1 and 50
print (die_rolls)
```
```
24
```
However, if you rerun the code, the number will most likely not repeat:
```python
import numpy as np
die_rolls = np.random.randint(1, 50) # generate a random integer between 1 and 50
print (die_rolls)
```
```
11
```
To receive the same random number every time, you can seed your generator:
```python
import numpy as np
np.random.seed(4)
die_rolls = np.random.randint(1, 50)
print (die_rolls)
```
```
47 
```
This way, the 47 will not be changing. 

## To Do

Simulate rolling a fair six-sided die and calculate the average value of multiple rolls. Include the random seed, so that the behaviour could be replicated, if necessary. 
```python
def simulate_dice_rolls(num_rolls, random_seed=None):
    ...
    return average_value
```