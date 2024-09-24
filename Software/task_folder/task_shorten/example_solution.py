#!function!#
def shorten(my_list):
#!prefix!#
    # Check if the input list is empty
    if not my_list:
        return []  # Return an empty list if the input list is empty

    # Extract the first and last elements and create a new list
    shortened_list = [my_list[0], my_list[-1]]

    return shortened_list