# Breakfast


In this task, you have to define a function called "breakfast"

```python
def breakfast(sentence):
    ...
```
As an input ("sentence") you will be receiving a string with products, like: "ham, fruit, orange juice". 
Within your function: 
1. Translate the string into a list of products (**hint**: split the string by comma with **split()** function)
2. Append an irreplacable product ("coffee") to the breakfast list with .append()
3. Extend the list to accomodate people who prefer leftovers from the previous evening ["pizza", "noodles"] with .extend()
4. Find out the length of the product list you have created. 
5. Create a new list with the first 2 products from the list you have created. 
6. Find out the lengths of the products in the new list and calculate their sum ((**hint**: you can use a loop for this)). 
7. Add "coffee" to the beginning of the new list with .insert()

For the input in the example above, the following output is expected: 

```
6, 8, ["coffee", "ham", "fruit"] 
```
Would you like to run this function to try what happens if the input string is empty?