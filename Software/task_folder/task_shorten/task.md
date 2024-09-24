# Lists 1

# Ordered Collection
Lists are used to store collections of data and are created using square brackets. They are ordered and allow duplicate values. The items within a list are indexed, beginning with [0].

```python
a = [1,2,3,1,4,5,6]
print(type(a))

# Indexing operator with positve values
print(a[0])  # First item
print(a[1])  # Second item

# with negative values
print(a[-1])  # Last item
print(a[-2])  # Item before last item
print(a[-3])  # ...
```
```
list
1
2
6
5
4
```
# To Do

Define a function, that will create and return a new list, containing the first and the last value of the input list.
```python
def shorten(my_list):
    ...

