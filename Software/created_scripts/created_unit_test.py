import unittest
import numpy as np
from example_solution import simulate_dice_rolls

def test_simulate_dice_rolls():
    # Test with num_rolls = 0
    average_value0 = simulate_dice_rolls(0, 4)
    assert average_value0 == 0.0

    # Test with a lower random seed value
    average_value1 = simulate_dice_rolls(100, 0)
    assert 1 <= average_value1 <= 6

    # Test with a large number of rolls
    average_value2 = simulate_dice_rolls(10000, 42)
    assert np.isclose(average_value2, 3.5, atol=0.1)

test_simulate_dice_rolls()
if __name__ == '__main__': # pragma: no cover
    unittest.main()