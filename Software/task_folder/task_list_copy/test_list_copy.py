from example_solution import list_copy as list_copy
#!cut_imports!#
def test_list_copy():
    # Test is arbitrary, but you should use assert.
    assert list_copy([1, 2, 3, 4, 5])[0] == [2, 3, 4], "There is an error in creating the new list"
    assert list_copy([1, 2, 3, 4, 5])[1] == [1, 2, 3, 4, 5], "The original list is not preserved"