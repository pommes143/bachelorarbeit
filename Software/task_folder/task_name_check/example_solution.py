#!function!#
def name_check(my_name):
#!prefix!#
    lowercase_name = my_name.lower()
    my_name_tuple = tuple(lowercase_name)
    a = "x" in my_name_tuple
    b = my_name_tuple[1:] 
    return a,b