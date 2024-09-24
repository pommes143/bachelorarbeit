from example_solution import variables as variables
#!cut_imports!#
def test_variables():
    # Test factorial of 0
    assert variables(0)[0] == str(0), "The first output should be string"
    assert variables(0)[1] == int(0), "The second output should be integer"
    assert variables(0)[2] == float(0), "The third output should be float"