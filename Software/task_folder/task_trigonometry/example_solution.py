#!function!#
import numpy as np 
def trigonometry(angle_array):
#!prefix!#
    # Convert degrees to radians
    angle_radians = np.deg2rad(angle_array)
    
    # Calculate sine, cosine, and tangent
    sine_values = np.sin(angle_radians)
    cosine_values = np.cos(angle_radians)
    tangent_values = np.tan(angle_radians)
    
    return sine_values, cosine_values, tangent_values

