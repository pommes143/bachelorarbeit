# Comments and Tuples

## Comments

You can use a one-line or multi-line comments. 
```python
# This is a one-line comment
print('Ok!')
```
```
Ok!
```
```python
'''
I am a multi line comment
bla bla
bla
'''
print('Gotcha!')
```
```
Gotcha!
```
## Tuples
A tuple is a collection of the data, which is ordered, allows duplicate values, but is *unchangeable*. The indexation begins with [0]. 
Also, you can unpack a tuple to obtain its singular values.

```python
# NOTE: A tuple is in round parantheses.
t = (1,2,3)  # NOTE: A tuple is immutable (=> can not be changed after it's created)
print(t)
print(t[0])
print(t[1])
```
```
(1, 2, 3)
1
2
```
```python
# Unpack a tuple
a, b, c = t

print(a)
print(b)
print(c)
```
```
1
2
3
```
```python
# Slicing tuples
my_tuple =(1,2,3,4,5)
print(my_tuple[2:]) #Print elements from index 2 to end 
```
```
(3, 4, 5)
```
## Typecasting tuples

Similarly to previous exercises, you can typecast tuples.

```python
a = 'ITS'
print (tuple(a))
```
```
('I', 'T', 'S')
```

## To Do

Create a function in the following format: 

```python
def name_check(my_name):
    ...
```
For the name given, this function should: 
1. Create a tuple containing the letters of your name from a string.
2. Check whether or not x is in the name. ()
3. Create tuple containing all but the first letter in `my_name`

> Desired output for the name `"Riza"`:
```
False, ('i', 'z', 'a')
```
**Note:** You can check whether something is included in a tuple (or list) by using the keyword "in", e.g: (var in tuple)