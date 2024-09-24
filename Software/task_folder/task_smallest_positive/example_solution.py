#!function!#
def smallest_positive(numbers, threshold):
#!prefix!#
    smallest_positive = None

    for num in numbers:
        if num > threshold:
            if smallest_positive is None or num < smallest_positive:
                smallest_positive = num

    return smallest_positive