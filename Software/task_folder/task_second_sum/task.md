# Loops
## While
```python
# while loop
i = 0
while i < 5:
    print(i)
    i += 1
    

cond = True
while cond is True:
    print("Bla")
    cond = False
```
```
0
1
2
3
4
Bla
```
```python
"""
General syntax

while <cond> == True:
    ...
"""
```
## For
```python
# for loop
for i in range(1,5):
    print(i)
    
for _ in range(5):
    print("Hi")
```
```
1
2
3
4
Hi
Hi
Hi
Hi
Hi
```
```python
"""
General syntax

for i in somelist:
    ...
"""
```
## To Do

For an input list of numbers, please define a following function: 

```python
def second_sum(input):
    ...
```
Which outputs the sum of every second number of the list. 
This way, for an input [1, 2, 3, 4, 5], the expected output should be (2 + 4):

```
6
```
(**Hint** you can also check the length of a list with len(my_list))