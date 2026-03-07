# ============================================
# INTRODUCTORY PYTHON COMMANDS CHEATSHEET
# ============================================


# ----------------------------
# 1. VARIABLES & DATA TYPES
# ----------------------------
x = 5               # integer
name = "Alice"      # string
pi = 3.14           # float
is_valid = True     # boolean

print(type(x))          # <class 'int'>
print(type(name))       # <class 'str'>
print(type(pi))         # <class 'float'>
print(type(is_valid))   # <class 'bool'>


# ----------------------------
# 2. OUTPUT & INPUT
# ----------------------------
print("Hello, World!")                  # print to console
print(f"My name is {name}")            # f-string output
# user_input = input("Enter your name: ")  # get user input (uncomment to use)


# ----------------------------
# 3. BASIC OPERATIONS
# ----------------------------
print(5 + 3)    # Addition        → 8
print(10 - 4)   # Subtraction     → 6
print(3 * 4)    # Multiplication  → 12
print(9 / 2)    # Division        → 4.5
print(2 ** 3)   # Exponentiation  → 8
print(10 % 3)   # Modulus         → 1
print(7 // 2)   # Floor Division  → 3


# ----------------------------
# 4. STRINGS
# ----------------------------
greeting = "hello"
print(len(greeting))            # Length       → 5
print(greeting.upper())         # Uppercase    → HELLO
print(greeting.capitalize())    # Capitalize   → Hello
print(greeting.replace("h", "j"))  # Replace   → jello
print(f"Hi, {name}!")           # f-string     → Hi, Alice!


# ----------------------------
# 5. LISTS
# ----------------------------
my_list = [1, 2, 3]
my_list.append(4)       # Add item       → [1, 2, 3, 4]
my_list.remove(2)       # Remove item    → [1, 3, 4]
print(my_list[0])       # Access index   → 1
print(len(my_list))     # Length         → 3
print(my_list)


# ----------------------------
# 6. DICTIONARIES
# ----------------------------
person = {"name": "Alice", "age": 25}
print(person["name"])           # Access value → Alice
person["email"] = "a@mail.com"  # Add new key
print(person)


# ----------------------------
# 7. CONDITIONALS
# ----------------------------
age = 18
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")


# ----------------------------
# 8. LOOPS
# ----------------------------

# For loop
for i in range(5):
    print(f"Count: {i}")

# While loop
count = 0
while count < 3:
    print(f"While count: {count}")
    count += 1

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)


# ----------------------------
# 9. FUNCTIONS
# ----------------------------
def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

print(greet("Alice"))   # → Hello, Alice!
print(add(3, 7))        # → 10


# ----------------------------
# 10. IMPORTS
# ----------------------------
import math

print(math.sqrt(16))    # Square root  → 4.0
print(math.pi)          # Pi constant  → 3.14159...
print(math.floor(4.9))  # Floor        → 4
print(math.ceil(4.1))   # Ceiling      → 5