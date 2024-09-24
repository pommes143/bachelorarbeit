from example_solution import my_list as my_list
#!cut_imports!#
def test_my_list():
    # Test is arbitrary, but you should use assert.
    assert len(my_list(7)) == 7, "It seems that the number of created elements is not correct"