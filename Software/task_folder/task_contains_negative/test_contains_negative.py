from example_solution import contains_negative as contains_negative
#!cut_imports!#
def test_contains_negative():
    # Test is arbitrary, but you should use assert.
    assert contains_negative([1, 2, 3, 4, 5]) == False, "There is no negative numbers in [1, 2, 3, 4, 5]"
    assert contains_negative([1, 2, -3, 4, 5]) == True, "There is a negative numbers in [1, 2, -3, 4, 5]"