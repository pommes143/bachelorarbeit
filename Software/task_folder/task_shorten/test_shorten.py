from example_solution import shorten as shorten
#!cut_imports!#
def test_shorten():
    # Test is arbitrary, but you should use assert.
    assert shorten([0,1,2,3,4,5,6,7]) == [0, 7], "It seems that some elements are not there or have a wrong format.*(Tuples are not lists!)"
    assert shorten(['eggs', 'fruit', 'orange juice', "ham"]) == ['eggs', "ham"], "Are you sure there are the first and the last elements only?"