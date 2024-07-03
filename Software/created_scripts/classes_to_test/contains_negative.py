#!function!#
def contains_negative(numbers):
#!prefix!#
    return any(num < 0 for num in numbers)

if __name__ == '__main__':
    print(contains_negative([1,2,3,-1,-1.0]))