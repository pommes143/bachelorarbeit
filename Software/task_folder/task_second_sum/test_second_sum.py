from example_solution import second_sum as second_sum
#!cut_imports!#
def test_second_sum():
    assert second_sum([1, 2, 3, 4, 5]) == 6, "It seems that the sum was calculated wrong"
    assert second_sum([9, 10, 16, 8, 0,7,5,3,2]) == 28, "It seems that the sum was calculated wrong"
    
