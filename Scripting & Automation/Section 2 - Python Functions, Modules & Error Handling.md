# Pillar 4 — Scripting & Automation
## Section 2: Python Functions, Modules & Error Handling

### Section Checklist
- [x] Functions: definition, parameters, arguments, body
- [x] return statement and implicit None returns
- [x] Default parameters and keyword arguments
- [x] *args and **kwargs
- [x] Scope: local vs global
- [x] Modules: import, from...import, aliasing, writing your own
- [x] Common standard library modules (os, sys, datetime, json, subprocess, random)
- [x] Exceptions and tracebacks
- [x] try/except handling, multiple exception types
- [x] else and finally clauses
- [x] Raising custom exceptions
- [x] Hands-on exercise

---

### 2.1 Functions — why they exist

A **function** is a named, reusable block of code that performs a specific task. Instead of copy-pasting the same logic repeatedly, you define it once and *call* it wherever needed.

```python
def greet(name):
    print(f"Hello, {name}")

greet("Keith")
greet("Codespace")
```
Output:
```
Hello, Keith
Hello, Codespace
```

Breaking this down:
- `def` — keyword that begins a function definition
- `greet` — the function's name (snake_case convention, same as variables)
- `(name)` — a **parameter**: a placeholder for input the function needs to do its job
- The indented block below is the function **body** — executed every time the function is called
- `greet("Keith")` — a **function call**; `"Keith"` here is the **argument** — the actual value passed in for `name`

---

### 2.2 `return` — sending a value back

`print()` displays something to the terminal, but it doesn't give the caller a value to use afterward. `return` does.

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)      # 8
```

Once `return` executes, the function exits immediately — code after `return` in that function never runs.

```python
def check_positive(n):
    if n > 0:
        return "positive"
    return "not positive"
```

A function with no explicit `return` implicitly returns `None`:
```python
def log_message(msg):
    print(msg)

output = log_message("test")
print(output)   # None
```

---

### 2.3 Default parameters and keyword arguments

Parameters can have default values, making them optional at call time:

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}")

greet("Keith")                     # Hello, Keith
greet("Keith", "Welcome back")     # Welcome back, Keith
greet(name="Keith", greeting="Hi") # Hi, Keith — keyword arguments, order doesn't matter
```

> **Pitfall:** Default parameters must come *after* non-default ones in the function signature. `def greet(greeting="Hello", name)` is a `SyntaxError`.

---

### 2.4 `*args` and `**kwargs`

Sometimes you don't know in advance how many arguments a function needs to accept.

**`*args`** — collects any number of extra positional arguments into a tuple:
```python
def total(*args):
    return sum(args)

total(1, 2, 3)        # 6
total(1, 2, 3, 4, 5)  # 15
```

**`**kwargs`** — collects any number of extra keyword arguments into a dict:
```python
def describe(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

describe(name="Keith", pillar=4, status="in progress")
```
Output:
```
name: Keith
pillar: 4
status: in progress
```

`*args` and `**kwargs` appear constantly in library code — they let a function accept flexible, open-ended input.

---

### 2.5 Scope — local vs global

A variable created inside a function only exists inside that function — this is called **local scope**.

```python
def my_function():
    x = 10       # local to my_function
    print(x)

my_function()   # 10
print(x)        # NameError: name 'x' is not defined
```

Variables defined outside any function have **global scope** and are readable (but not directly writable) from inside functions:

```python
counter = 0

def show_counter():
    print(counter)   # readable — 0

show_counter()
```

To *modify* a global variable from inside a function, it must be explicitly declared with `global`:
```python
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)   # 2
```

> **Callout — avoid overusing `global`.** Functions that silently mutate global state are hard to reason about and debug, especially as scripts grow. Prefer passing values in as arguments and returning results, reserving `global` for genuinely shared state (e.g., a running total across many calls in a small script).

---

### 2.6 Modules — organizing and reusing code

A **module** is simply a `.py` file containing Python code — functions, variables, classes — that can be imported and reused in other files.

**Using a built-in module:**
```python
import math

print(math.sqrt(16))     # 4.0
print(math.pi)           # 3.141592653589793
```

**Importing specific names only:**
```python
from math import sqrt, pi

print(sqrt(16))   # 4.0
print(pi)          # 3.141592653589793
```

**Aliasing on import** (common convention for long module names):
```python
import datetime as dt

now = dt.datetime.now()
print(now)
```

**Writing your own module:**

Create `helpers.py`:
```python
def double(n):
    return n * 2
```

In another file in the same directory:
```python
import helpers

print(helpers.double(5))   # 10
```

> This is exactly the pattern used once scripts grow beyond a single file — shared logic (API calls, logging setup, config loading) lives in its own module and gets imported wherever needed.

---

### 2.7 Commonly used standard library modules

| Module | Purpose | Example |
|---|---|---|
| `os` | Interact with the operating system | `os.getcwd()`, `os.listdir()` |
| `sys` | Interact with the interpreter/runtime | `sys.argv` (command-line arguments) |
| `datetime` | Dates and times | `datetime.datetime.now()` |
| `json` | Parse/generate JSON (Section 8) | `json.loads()`, `json.dumps()` |
| `subprocess` | Run shell commands from Python | `subprocess.run(["ls", "-l"])` |
| `random` | Generate random values | `random.randint(1, 10)` |

```python
import os
print(os.getcwd())          # current working directory
print(os.listdir("."))      # files in current directory
```

---

### 2.8 Errors and exceptions

When Python encounters a problem it can't proceed past, it raises an **exception** — the program halts and prints a **traceback** showing what went wrong and where.

```python
>>> 10 / 0
ZeroDivisionError: division by zero

>>> int("abc")
ValueError: invalid literal for int() with base 10: 'abc'

>>> undefined_variable
NameError: name 'undefined_variable' is not defined
```

Left unhandled, an exception **crashes the script**. In automation, that's often unacceptable — a script processing 1,000 files shouldn't die entirely because file #47 was malformed.

---

### 2.9 `try` / `except` — handling exceptions gracefully

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```
Output:
```
Cannot divide by zero
```
The program continues running after the `except` block — it does not crash.

**Catching multiple exception types:**
```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: division by zero")
    except TypeError:
        print("Error: invalid types for division")

safe_divide(10, 0)      # Error: division by zero
safe_divide(10, "a")    # Error: invalid types for division
```

**Catching any exception** (use sparingly — see pitfalls below):
```python
try:
    risky_operation()
except Exception as e:
    print(f"Something went wrong: {e}")
```
`as e` binds the exception object to a variable so its message can be inspected.

---

### 2.10 `else` and `finally`

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error")
else:
    print(f"Success: {result}")    # runs only if no exception occurred
finally:
    print("This always runs")      # runs no matter what — success or failure
```
Output:
```
Success: 5.0
This always runs
```

`finally` is commonly used for cleanup — closing a file, closing a network connection — that must happen whether or not an error occurred.

---

### 2.11 Raising your own exceptions

`raise` deliberately triggers an exception — useful for enforcing that input meets certain conditions:

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age

set_age(-5)   # ValueError: Age cannot be negative
```

This is how well-written functions protect against invalid input rather than silently producing wrong results.

---

### Pitfalls Table

| Pitfall | Why it's a problem | Fix |
|---|---|---|
| Bare `except:` with no exception type | Silently swallows *every* error, including ones you didn't anticipate (e.g., `KeyboardInterrupt`), making bugs invisible | Catch specific exception types; use `except Exception as e` at most, and log `e` |
| Overusing `global` | Functions that mutate shared state become hard to trace and debug as scripts grow | Pass values as arguments, return results; reserve `global` for genuinely shared counters/state |
| Default parameter comes before non-default | `SyntaxError` at definition time | Order non-default parameters first, defaults after |
| Forgetting a function has an implicit `None` return | Assigning the result of a function with no `return` gives `None`, causing confusing downstream errors | Always add an explicit `return` if the caller needs a value |
| Mutable default arguments (e.g., `def f(items=[])`) | The same list object is reused across all calls, causing unexpected shared state | Use `None` as default, then create the mutable object inside the function body |

---

### 🖥️ Hands-on Exercise

In `/workspaces/DevOps-Journey`:

```bash
nano practice2.py
```

1. Define a function `divide(a, b)` that returns `a / b`, using `try/except` to catch `ZeroDivisionError` and print a friendly message instead of crashing
2. Define a function `pillar_status(**kwargs)` that prints each keyword argument passed in (e.g., call it with `name="scripting", section=2, status="in progress"`)
3. Import the `os` module and print the current working directory

Run: `python3 practice2.py`

---

### DevOps Connection
Error handling is the difference between a script that fails loudly and stops an entire pipeline, versus one that logs the problem, skips the bad input, and keeps going. CI/CD pipelines (Phase 2) live or die on scripts handling unexpected input predictably — a deployment script that crashes on one malformed config file instead of catching and reporting the issue can take down an entire release process.

---

**Next section:** [03-python-file-io.md](./03-python-file-io.md) — File I/O in Python