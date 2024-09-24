#!function!#
def contains_negative(numbers):
#!prefix!#
    return any(num < 0 for num in numbers)
