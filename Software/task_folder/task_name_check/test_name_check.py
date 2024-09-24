from example_solution import name_check as name_check
#!cut_imports!#
def test_name_check():
    # Test factorial of 0
    assert name_check("Robert")[0] == False, "The first output should be False, if there is no x in the name"
    assert name_check("Xena")[0] == True, "The first output for Xena should be True, as there is an x in the name. Did you account for upper case X?"
    assert name_check("Alex")[1] == ("l", "e", "x"), "The second output should be all the letters of the name, apart from the first one"