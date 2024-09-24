# Control Structures

## Boolean Expressions

```python
c = True

not_c = not c
print(not_c)

c_test = c is False
print(c_test)

c_test2 = not_c is not True
print(c_test2)

l = True and False
print(l)

print(True or False)
```
```
False
False
True
False
True
```
## Conditions

```python
a = 2
if a == 3:
    print("a = 3")
elif a == 2:
    print("a = 2")
else:
    print("a != 2")
```
```
a = 2
```
```python
# All expressions with a boolean result are valid conditions
if a > 3:
    print("a > 3")
    
if len("ABC") == 3:
    print("String with length 3")
```
```
String with length 3
```
## To Do
Create a function that checks if a given list of numbers contains any negative numbers. The function should return True if there are negative numbers and False otherwise. (**HINT** you can use "any()" to check the list)

```python
def contains_negative(numbers):
    ...
```
