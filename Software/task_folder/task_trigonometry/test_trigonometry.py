from example_solution import trigonometry as trigonometry
import numpy as np
#!cut_imports!#
def test_trigonometry():
    # Test case 1: Check if the function correctly calculates trigonometric values
    angle_array1 = np.array([0, 30, 45, 60])
    sine_values1, cosine_values1, tangent_values1 = trigonometry(angle_array1)
    expected_sine1 = np.array([0.0, 0.5, np.sqrt(2)/2, np.sqrt(3)/2])
    expected_cosine1 = np.array([1.0, np.sqrt(3)/2, np.sqrt(2)/2, 0.5])
    expected_tangent1 = np.array([0.0, np.sqrt(3)/3, 1.0, np.sqrt(3)])
    
    assert np.allclose(sine_values1, expected_sine1), "Sinus (positive) values are calculated not correctly."
    assert np.allclose(cosine_values1, expected_cosine1), "Cosine (positive) values are calculated not correctly"
    assert np.allclose(tangent_values1, expected_tangent1), "Tangent (positive) values are calculated not correctly"

    # Test case 2: Check if the function handles negative angles
    angle_array2 = np.array([-60, -45, -30, 0])
    sine_values2, cosine_values2, tangent_values2 = trigonometry(angle_array2)
    expected_sine2 = np.array([-np.sqrt(3)/2, -np.sqrt(2)/2, -0.5, 0.0])
    expected_cosine2 = np.array([0.5, np.sqrt(2)/2, np.sqrt(3)/2, 1.0])
    expected_tangent2 = np.array([-np.sqrt(3), -1.0, -np.sqrt(3)/3, 0.0])
    
    assert np.allclose(sine_values2, expected_sine2), "Sinus (negative angle) values are calculated not correctly."
    assert np.allclose(cosine_values2, expected_cosine2), "Cosine (negative angle) values are calculated not correctly."
    assert np.allclose(tangent_values2, expected_tangent2), "Tangent (negative angle) values are calculated not correctly."

