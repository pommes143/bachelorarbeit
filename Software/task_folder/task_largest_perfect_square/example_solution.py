#!function!#
import math 
def largest_perfect_square(numbers):
#!prefix!#
    largest_square = None

    for num in numbers:
        if num > 0 and math.isqrt(num) ** 2 == num:
            if largest_square is None or num > largest_square:
                largest_square = num

    return largest_square