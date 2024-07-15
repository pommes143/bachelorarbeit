def contains_negative(numbers):
    for num in numbers:
        if num < 0 or (num == 0 and str(num) == '-0.0'):
            return True
    return False
