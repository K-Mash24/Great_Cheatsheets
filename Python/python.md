# 🐍 Python Intro Cheatsheet

> A beginner-friendly reference for core Python syntax and concepts. Use this to quickly remind yourself of how things work in Python.

---

## 📋 Table of Contents

1. [Variables & Data Types](#1-variables--data-types)
2. [Output & Input](#2-output--input)
3. [Basic Operations](#3-basic-operations)
4. [Strings](#4-strings)
5. [Lists](#5-lists)
6. [Dictionaries](#6-dictionaries)
7. [Conditionals](#7-conditionals)
8. [Loops](#8-loops)
9. [Functions](#9-functions)
10. [Imports](#10-imports)

---

## 1. Variables & Data Types

Variables store data. Python automatically detects the type — no need to declare it.

```python
x = 5               # int    → whole number
name = "Alice"      # str    → text
pi = 3.14           # float  → decimal number
is_valid = True     # bool   → True or False
```

Check a variable's type with `type()`:

```python
print(type(x))          # <class 'int'>
print(type(name))       # <class 'str'>
print(type(pi))         # <class 'float'>
print(type(is_valid))   # <class 'bool'>
```

| Type | Example | Description |
|------|---------|-------------|
| `int` | `5` | Whole number |
| `float` | `3.14` | Decimal number |
| `str` | `"Alice"` | Text / string |
| `bool` | `True` / `False` | Boolean value |

---

## 2. Output & Input

```python
print("Hello, World!")              # Prints text to the console
print(f"My name is {name}")        # f-string: embed variables in strings
print("Sum:", 3 + 4)               # Print multiple values
print("Line 1\nLine 2")            # \n creates a new line
```

```python
user_input = input("Enter your name: ")   # Prompts user for input
print(f"Hello, {user_input}!")            # Prints their response
```

> 💡 `input()` always returns a **string**. Use `int()` or `float()` to convert it if needed.
> ```python
> age = int(input("Enter your age: "))
> ```

---

## 3. Basic Operations

### Arithmetic

```python
print(5 + 3)    # Addition        → 8
print(10 - 4)   # Subtraction     → 6
print(3 * 4)    # Multiplication  → 12
print(9 / 2)    # Division        → 4.5  (always returns float)
print(2 ** 3)   # Exponentiation  → 8
print(10 % 3)   # Modulus         → 1    (remainder)
print(7 // 2)   # Floor Division  → 3    (rounds down)
```

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `10 - 4` | `6` |
| `*` | Multiplication | `3 * 4` | `12` |
| `/` | Division | `9 / 2` | `4.5` |
| `**` | Exponentiation | `2 ** 3` | `8` |
| `%` | Modulus | `10 % 3` | `1` |
| `//` | Floor Division | `7 // 2` | `3` |

### Comparison Operators

```python
5 == 5      # Equal to           → True
5 != 3      # Not equal to       → True
5 > 3       # Greater than       → True
5 < 3       # Less than          → False
5 >= 5      # Greater or equal   → True
5 <= 4      # Less or equal      → False
```

### Logical Operators

```python
True and False  # Both must be True  → False
True or False   # At least one True  → True
not True        # Inverts value      → False
```

---

## 4. Strings

```python
greeting = "hello"

print(len(greeting))                # Length           → 5
print(greeting.upper())             # Uppercase        → HELLO
print(greeting.lower())             # Lowercase        → hello
print(greeting.capitalize())        # Capitalise       → Hello
print(greeting.replace("h", "j"))   # Replace          → jello
print(greeting.strip())             # Remove whitespace from both ends
print(greeting.split("l"))          # Split into list  → ['he', '', 'o']
print("hello" in greeting)          # Check substring  → True
print(f"Hi, {name}!")               # f-string         → Hi, Alice!
```

### String Indexing & Slicing

```python
word = "Python"

print(word[0])      # First character     → P
print(word[-1])     # Last character      → n
print(word[0:3])    # Slice positions 0–2 → Pyt
print(word[2:])     # From index 2 onward → thon
print(word[:4])     # Up to index 3       → Pyth
print(word[::-1])   # Reversed            → nohtyP
```

> 💡 Strings in Python are **immutable** — you can't change individual characters. You create a new string instead.

---

## 5. Lists

A list is an ordered, changeable collection of items.

```python
my_list = [1, 2, 3]

my_list.append(4)       # Add to end        → [1, 2, 3, 4]
my_list.insert(1, 99)   # Insert at index   → [1, 99, 2, 3, 4]
my_list.remove(2)       # Remove by value   → [1, 99, 3, 4]
my_list.pop()           # Remove last item  → [1, 99, 3]
my_list.sort()          # Sort ascending    → [1, 3, 99]
my_list.reverse()       # Reverse order     → [99, 3, 1]

print(my_list[0])       # Access by index   → 99
print(len(my_list))     # Length            → 3
print(my_list)
```

### List Slicing

```python
nums = [10, 20, 30, 40, 50]

print(nums[1:3])    # Index 1 to 2  → [20, 30]
print(nums[:2])     # First 2 items → [10, 20]
print(nums[3:])     # From index 3  → [40, 50]
print(nums[-2:])    # Last 2 items  → [40, 50]
```

### List Methods Summary

| Method | Description |
|--------|-------------|
| `.append(x)` | Add item to end |
| `.insert(i, x)` | Insert at index `i` |
| `.remove(x)` | Remove first occurrence of `x` |
| `.pop()` | Remove and return last item |
| `.sort()` | Sort in place (ascending) |
| `.reverse()` | Reverse in place |
| `.index(x)` | Return index of `x` |
| `.count(x)` | Count occurrences of `x` |
| `.clear()` | Remove all items |

---

## 6. Dictionaries

A dictionary stores data as **key: value** pairs.

```python
person = {"name": "Alice", "age": 25}

print(person["name"])               # Access value       → Alice
print(person.get("age"))            # Safe access        → 25
print(person.get("email", "N/A"))   # Default if missing → N/A

person["email"] = "a@mail.com"      # Add new key-value
person["age"] = 26                  # Update existing value
del person["email"]                 # Delete a key

print(person.keys())                # All keys
print(person.values())              # All values
print(person.items())               # All key-value pairs
print("name" in person)             # Check key exists → True
```

---

## 7. Conditionals

```python
age = 18

if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")
```

### One-line Conditional (Ternary)

```python
label = "Adult" if age >= 18 else "Minor"
print(label)    # → Adult
```

---

## 8. Loops

### For Loop

```python
# Loop a set number of times
for i in range(5):
    print(f"Count: {i}")       # 0, 1, 2, 3, 4

# range(start, stop, step)
for i in range(1, 10, 2):
    print(i)                   # 1, 3, 5, 7, 9

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Loop with index using enumerate()
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

### While Loop

```python
count = 0
while count < 3:
    print(f"While count: {count}")
    count += 1
```

### Loop Control

```python
for i in range(10):
    if i == 3:
        continue    # Skip this iteration
    if i == 7:
        break       # Stop the loop entirely
    print(i)
```

| Keyword | Purpose |
|---------|---------|
| `break` | Exit the loop immediately |
| `continue` | Skip to the next iteration |
| `pass` | Do nothing (placeholder) |

---

## 9. Functions

```python
# Basic function
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))       # → Hello, Alice!


# Function with multiple parameters
def add(a, b):
    return a + b

print(add(3, 7))            # → 10


# Default parameter value
def greet(name="stranger"):
    return f"Hello, {name}!"

print(greet())              # → Hello, stranger!
print(greet("Bob"))         # → Hello, Bob!


# Multiple return values
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 9, 4])
print(low, high)            # → 1 9


# Arbitrary number of arguments
def total(*args):
    return sum(args)

print(total(1, 2, 3, 4))   # → 10
```

> 💡 Keep functions **small and focused** — one function should do one thing.

---

## 10. Imports

```python
# Import a full module
import math

print(math.sqrt(16))        # Square root  → 4.0
print(math.pi)              # Pi constant  → 3.14159...
print(math.floor(4.9))      # Floor        → 4
print(math.ceil(4.1))       # Ceiling      → 5
print(math.pow(2, 3))       # Power        → 8.0
print(math.abs(-5))         # Absolute     → 5


# Import specific functions only
from math import sqrt, pi

print(sqrt(25))             # → 5.0
print(pi)                   # → 3.14159...


# Import with an alias
import math as m
print(m.sqrt(9))            # → 3.0


# Import everything (not recommended for large modules)
from math import *
print(sqrt(36))             # → 6.0
```

### Common Built-in Modules

| Module | Use For |
|--------|---------|
| `math` | Mathematical functions |
| `random` | Random numbers |
| `datetime` | Dates and times |
| `os` | File system and OS operations |
| `sys` | Python interpreter info |
| `json` | Parse and write JSON |
| `re` | Regular expressions |

---

> ✅ **Quick Reminder:** Python uses **indentation** (4 spaces) instead of curly braces `{}` to define code blocks. Consistent indentation is not optional — it's part of the syntax.