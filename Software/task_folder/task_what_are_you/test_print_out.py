from example_solution import what_are_you as what_are_you
#!cut_imports!#


def test_print_out():
    assert submission_captured_output == "<class 'str'>\n<class 'int'>\n<class 'float'>\n<class 'bool'>", "You forgot to test out your function. Or maybe, the order of your output is wrong?"
    