from example_solution import what_are_you as what_are_you
#!cut_imports!#
import sys
from io import StringIO

def test_what_are_you():
    captured_output = StringIO()
    sys.stdout = captured_output
    what_are_you("AI Overlord")
    what_are_you(9)
    what_are_you(2.5)
    what_are_you([1,2])
    sys.stdout = sys.__stdout__
    captured_output =  captured_output.getvalue().strip()
    assert captured_output == "<class 'str'>\n<class 'int'>\n<class 'float'>\n<class 'list'>", "The types of input variables are not printed correctly."