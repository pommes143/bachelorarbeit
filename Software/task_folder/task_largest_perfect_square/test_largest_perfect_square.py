from example_solution import largest_perfect_square as largest_perfect_square
#!cut_imports!#
def test_largest_perfect_square():
    # Test is arbitrary, but you should use assert.
    numbers1 = [1, 4, 9, 16, 25]
    numbers2 = [8, 10, 15, 18, 20]
    numbers3 = [49, 64, 81, 100, 121]
    assert largest_perfect_square(numbers1) == 25, "It seems that the largest sqaure is not found correctly."
    assert largest_perfect_square(numbers2) == None, "It seems that the case for None is not implemented."
    assert largest_perfect_square(numbers3) == 121, "It seems that you are finding the first, not the largest"