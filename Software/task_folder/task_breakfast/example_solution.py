#!function!#
def breakfast(sentence):
#!prefix!#
    # Step 1: Translate the string into a list of products
    products = sentence.split(', ')
    
    # Step 2: Append "coffee" to the breakfast list
    products.append("coffee")
    
    # Step 3: Extend the list to accommodate leftovers
    products.extend(["pizza", "noodles"])
    
    # Step 4: Find out the length of the product list
    length_of_products = len(products)
    
    # Step 5: Create a new list with the first 2 products
    new_list = products[:2]
    
    # Step 6: Find out the lengths of the products in the new list and calculate their sum
    sum_of_lengths = sum(len(product) for product in new_list)
    
    # Step 7: Add "coffee" to the beginning of the new list
    new_list.insert(0, "coffee")
    
    return length_of_products, sum_of_lengths, new_list