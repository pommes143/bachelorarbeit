from example_solution import factorial as factorial
#!cut_imports!#
def test_factorial():
    # Test factorial of 0
    assert factorial(0) == 1, "Factorial of 0 is 1"
    
    # Test factorial of positive numbers
    assert factorial(1) == 1, "Factorial of 1 is 1"
    assert factorial(5) == 120, "Factorial of 5 is 120"
    assert factorial(10) == 3628800, "Factorial of 10 is 3628800"