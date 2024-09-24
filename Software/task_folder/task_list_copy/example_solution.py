#!function!#
def list_copy(my_list):
#!prefix!#
    # Check if the input list has at least two elements
    if len(my_list) < 2:
        return [],my_list  # Return an empty list if there are fewer than two elements in the input list

    # Create a new list by slicing the original list
    new_list = my_list[1:-1]

    return new_list, my_list
