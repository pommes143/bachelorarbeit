#!function!#
import numpy as np 
def simulate_dice_rolls(num_rolls, random_seed=None):
#!prefix!#
    # Set the random seed if provided
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Simulate die rolls using random integers between 1 and 6
    die_rolls = np.random.randint(1, 7, size=num_rolls)
    
    # Calculate the average value of the die rolls
    average_value = np.mean(die_rolls)
    
    return average_value
