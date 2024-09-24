from example_solution import square as square
#!cut_imports!#
def test_square():
    # Test square of 0
    assert square(0) == 0, "Square of 0 is 0"
    
    # Test square of positive numbers
    assert square(1) == 1, "Square of 1 is 1"
    assert square(2) == 4, "Square of 2 is 4"
    assert square(3) == 9, "Square of 3 is 9"
    assert square(4) == 16, "Square of 4 is 16"
    
    # Test square of negative numbers
    assert square(-1) == 1, "Square of -1 is 1"
    assert square(-2) == 4, "Square of -2 is 4"
    assert square(-3) == 9, "Square of -3 is 9"
    assert square(-4) == 16, "Square of -4 is 16"