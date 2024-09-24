# Lists 2
## Creating lists
There are many ways to create a list, here are a couple of them:

```python
# Create a list by using range 
z = list(range(0, 10))
print(z)
print(range(0, 10))

z = list(range(1, 20, 2))  # Stepsize has to be an integer!
print(z)

# Create a list by using list comprehension
print([x**2 for x in [1,2,3,4,5,6]])
```
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
range(0, 10)
[1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
[1, 4, 9, 16, 25, 36]
```
## Creating lists
Create a function, that for each integer **n** will create an arbitrary list with **n** elements: 

```python
def my_list(n):
    ...
```