#Implement further tests in a seperate file each
from example_solution import smallest_positive as smallest_positive
#!cut_imports!#
def test_smallest_positive():
    # Test is arbitrary, but you should use assert.
    numbers1 = [1, 2, 3, 4, 5]
    numbers2 = [-2, -1, 0, 5, 7, 2, -4]
    numbers3 = [-1, -2, -3, -4, -5]
    threshold = 2
    assert smallest_positive(numbers1, threshold) == 3, "It seems that the smallest number above the threshold if found wrong. Do you use a strict difference?"
    assert smallest_positive(numbers2, threshold) == 5, "It seems that the smallest number above the threshold if found wrong. Do you use a strict difference?"
    assert smallest_positive(numbers3, threshold) == None, "It seems that you forgot a condition, when there is no number aobe threshold in the list."
    
