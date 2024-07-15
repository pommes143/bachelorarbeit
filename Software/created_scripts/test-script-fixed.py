import numpy as np
import example_solution

def test_trigonometry():
    angle_array1 = np.array([0, 30, 45, 60])
    sine_values1, cosine_values1, tangent_values1 = example_solution.trigonometry(angle_array1)
    expected_sine1 = np.array([0.0, 0.5, np.sqrt(2)/2, np.sqrt(3)/2])
    assert np.allclose(sine_values1, expected_sine1), "Sinus (positive) values are calculated not correctly."

    angle_array2 = np.array([150, 120, 90, 60])
    sine_values2, cosine_values2, tangent_values2 = example_solution.trigonometry(angle_array2)
    expected_sine2 = np.array([np.sin(np.deg2rad(150)), np.sin(np.deg2rad(120)), np.sin(np.deg2rad(90)), np.sin(np.deg2rad(60)])
    assert np.allclose(sine_values2, expected_sine2), "Sinus (negative angle) values are calculated not correctly."

    angle_array3 = np.array([-30, -45, -60])
    sine_values3, cosine_values3, tangent_values3 = example_solution.trigonometry(angle_array3)
    expected_sine3 = np.array([np.sin(np.deg2rad(-30)), np.sin(np.deg2rad(-45)), np.sin(np.deg2rad(-60)])
    assert np.allclose(sine_values3, expected_sine3), "Sinus (negative angle) values are calculated not correctly."
