#!function!#
def my_list(n):
#!prefix!#
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    # Use a list comprehension to create a list with consecutive integers from 1 to n
    result = [i for i in range(1, n + 1)]

    return result