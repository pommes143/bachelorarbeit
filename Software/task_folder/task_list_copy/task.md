# Lists 3
## References and copies
Not everything in Python can be passed by value: 
```python
# ATTENTION: How to copy a list
a2 = a   # Not a copy but a reference

a3 = a[:]  # This is a copy!

#Example
b=[1,2,3]
c= [4,5,6]
b1 = b
c1 = c[:]

b1.append(100)
c1.append(7)


print(b1)
print(b)

print(c1)
print(c)
```
```
[1, 2, 3, 100]
[1, 2, 3, 100]
[4, 5, 6, 7]
[4, 5, 6]
```
As we can see, the changes in *b1* (reference) were doubled in the original list *b*, however, the *c1* (copy) was treated separately from the original list *c*.

## To Do 

Define the function:
```python
def list_copy(my_list):
    ...
```
Which take a list as an input, and creates a new list with first and last elements of the original list removed (original list should be preserved). Return both the new list and the old list. 
