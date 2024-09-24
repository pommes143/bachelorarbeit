from example_solution import greet as greet
#!cut_imports!#

def test_print_out():
    assert submission_captured_output == "Hello Alice\nHello Bob", "You forgot to greet Alice and Bob on the console."