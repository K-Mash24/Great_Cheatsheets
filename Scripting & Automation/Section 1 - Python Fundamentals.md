# Section 1: Python Fundamentals

## Section Checklist

- [x] What Python is (interpreted language) and how it runs
- [x] REPL vs script execution
- [x] Variables and dynamic typing
- [x] Core data types (int, float, str, bool, None)
- [x] Type conversion / casting
- [x] Arithmetic, comparison, and logical operators
- [x] Strings: immutability, f-strings, methods, slicing, zero-based indexing
- [x] Comments and truthiness
- [x] Collections: lists, tuples, dictionaries
- [x] Control flow: if/elif/else
- [x] Control flow: for loops, range(), while loops
- [x] Simple input/output
- [x] Hands-on exercise

---

### 1.1 What is Python, actually?

Python is an **interpreted** language — there is no separate compile step producing a standalone executable before running (contrast with C, where source is compiled into a binary first). A program called the **Python interpreter** reads a `.py` file line by line and executes it directly.

This gives a fast feedback loop: write code, run it, see the result immediately — exactly why Python dominates scripting and automation work.

**Check version:**

```bash
python3 --version
```

Expected output:

```
Python 3.11.x
```

> **Note:** Always use `python3`, not `python`, on Linux. Many systems don't alias `python` to `python3` — bare `python` may fail with "command not found" or invoke a legacy Python 2 install if one still exists on the system.

---

### 1.2 Running Python two ways

**1. The interactive interpreter (REPL — Read-Eval-Print Loop)**

```bash
python3
```

Lands in an interactive prompt:

```
Python 3.11.4 (main, ...)
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Type expressions, see results instantly:

```python
>>> 2 + 2
4
>>> "hello" + " world"
'hello world'
```

Exit with `exit()` or `Ctrl+D`.

**2. Running a script file**

```bash
nano hello.py
```

```python
print("Hello, DevOps Journey")
```

```bash
python3 hello.py
```

Output:

```
Hello, DevOps Journey
```

The REPL is for quick experiments. Script files are for anything saved, edited, and reused — essentially everything in automation.

---

### 1.3 Variables

A **variable** is a name referring to a value stored in memory. Python is **dynamically typed** — no type declaration up front; the interpreter infers the type from the assigned value.

```python
name = "Keith"
age = 5
is_learning = True
```

No `int name = 5` syntax (unlike Java/C). Just `name = value`.

**Naming rules:**

- Letters, digits, underscores only; cannot start with a digit
- Case‑sensitive (`age` ≠ `Age`)
- Convention: `snake_case` (`user_name`, not `userName` — that's a Java/JavaScript convention)
- **Reserved keywords** cannot be used as variable names (e.g., `if`, `for`, `while`, `def`, `return`).

---

### 1.4 Core data types

| Type       | Example          | Meaning                                   |
| ---------- | ---------------- | ----------------------------------------- |
| `int`      | `42`             | Whole number                              |
| `float`    | `3.14`           | Decimal number                            |
| `str`      | `"hello"`        | Text (single or double quotes both valid) |
| `bool`     | `True` / `False` | Boolean — capitalized, unlike JSON/JS     |
| `NoneType` | `None`           | Represents "no value" — Python's null     |

Check type at runtime:

```python
>>> x = 42
>>> type(x)
<class 'int'>
```

**Type conversion (casting):**

```python
>>> str(42)        # '42'
>>> int("42")       # 42
>>> float("3.14")   # 3.14
>>> int("abc")      # ValueError: invalid literal for int() with base 10: 'abc'
```

> **Callout:** An impossible conversion raises an **exception** — an error that can be caught and handled programmatically (covered in Section 2). Scripts that accept external input must anticipate this.

---

### 1.5 Basic operators

**Arithmetic:**

```python
>>> 7 + 3    # 10
>>> 7 - 3    # 4
>>> 7 * 3    # 21
>>> 7 / 3    # 2.333... (true division, always float)
>>> 7 // 3   # 2 (floor division, discards remainder)
>>> 7 % 3    # 1 (modulo — the remainder)
>>> 7 ** 3   # 343 (exponentiation)
```

**Comparison** (returns `bool`):

```python
>>> 5 == 5    # True
>>> 5 != 3    # True
>>> 5 > 3     # True
>>> 5 <= 5    # True
```

**Logical:**

```python
>>> True and False   # False
>>> True or False    # True
>>> not True          # False
```

**Truthiness (important!)**

In Python, any value can be used in a boolean context. The following are considered `False`:

- `None`
- `False`
- Zero of any numeric type (`0`, `0.0`)
- Empty sequences/collections (`""`, `[]`, `()`, `{}`, `set()`)

Everything else is `True`.

```python
>>> if []:
...     print("True")
... else:
...     print("False")
False
```

This makes code like `if not user_list:` very common and clean.

---

### 1.6 Strings in depth

Strings are **immutable** — an existing string object cannot be changed in place. Methods that appear to modify a string actually return a new string.

```python
>>> s = "hello"
>>> s.upper()
'HELLO'
>>> s              # unchanged
'hello'
```

**f-strings** (modern, preferred formatting method):

```python
>>> name = "Keith"
>>> pillar = 4
>>> print(f"{name} is on Pillar {pillar}")
Keith is on Pillar 4
```

The `f` prefix enables `{}` to embed variables directly, replacing older `.format()` and `%`-style formatting (still seen in legacy code, but you don't need to master them — just recognise them).

**Common string methods:**

```python
>>> s = "  Hello World  "
>>> s.strip()                       # 'Hello World' — trims whitespace
>>> s.lower()                       # '  hello world  '
>>> s.replace("World", "Python")    # '  Hello Python  '
>>> s.split(" ")                    # ['', '', 'Hello', 'World', '', '']
>>> len(s)                          # 15 (includes spaces)
```

**Slicing:**

```python
>>> s = "networking"
>>> s[0]        # 'n' (first character, index 0)
>>> s[0:4]      # 'netw' (index 0 up to, not including, 4)
>>> s[-1]       # 'g' (negative indexing counts from the end)
>>> s[::-1]     # 'gnikrowten' (reversed)
```

> **Critical detail:** Python indexing is **zero-based** — the first character is index `0`. This is consistent across all sequence types (strings, lists, tuples) and is a frequent early source of off-by-one errors.

---

### 1.7 Comments

Comments are ignored by the interpreter; they exist solely for human readers. Use them to explain _why_ something is done, not _what_ is done (the code itself shows what).

```python
# Single-line comment

"""
Multi-line comment / docstring
(usually used for function/module documentation)
"""
```

In scripts, always start with a comment explaining the purpose:

```python
# check_pillar_status.py
# Checks the completion status of Phase 1 pillars
```

---

### 1.8 Collections: lists, tuples, dicts

**Lists** — ordered, mutable:

```python
>>> tools = ["docker", "kubernetes", "terraform"]
>>> tools[0]                # 'docker'
>>> tools.append("ansible")
>>> tools
['docker', 'kubernetes', 'terraform', 'ansible']
>>> tools[1] = "k8s"        # mutate in place
>>> len(tools)              # 4
```

**Tuples** — ordered, **immutable**:

```python
>>> coords = (10, 20)
>>> coords[0]      # 10
>>> coords[0] = 5  # TypeError: 'tuple' object does not support item assignment
```

Use tuples for data that should not change — e.g., a fixed coordinate pair, or a function returning a fixed group of values.

**Dictionaries (`dict`)** — key-value pairs:

```python
>>> user = {"name": "Keith", "pillar": 4, "active": True}
>>> user["name"]           # 'Keith'
>>> user["pillar"] = 5      # update value
>>> user["cert"] = "CCP"    # add new key
>>> user
{'name': 'Keith', 'pillar': 5, 'active': True, 'cert': 'CCP'}
>>> user.keys()             # dict_keys(['name', 'pillar', 'active', 'cert'])
>>> user.values()           # dict_values(['Keith', 5, True, 'CCP'])
```

Dictionaries map almost one‑to‑one onto **JSON** objects — the data format used by virtually every REST API (Sections 6–8 of this pillar).

---

### 1.9 Control flow — conditionals

```python
score = 85

if score >= 90:
    print("A grade")
elif score >= 80:
    print("B grade")
else:
    print("C grade or below")
```

Output: `B grade`

> **Critical syntax rule:** Python uses **indentation** to define code blocks — not curly braces `{}` (unlike C/Java/JavaScript). Convention: **4 spaces** per level. Never mix tabs and spaces — causes `IndentationError`.

---

### 1.10 Control flow — loops

**`for` loop:**

```python
tools = ["docker", "kubernetes", "terraform"]
for tool in tools:
    print(f"Learning: {tool}")
```

Output:

```
Learning: docker
Learning: kubernetes
Learning: terraform
```

**`range()`:**

```python
for i in range(5):
    print(i)
```

Output: `0 1 2 3 4` — `range(5)` produces five values, 0 through 4, not through 5.

**`while` loop:**

```python
count = 0
while count < 3:
    print(f"Count is {count}")
    count += 1   # shorthand for count = count + 1
```

Output:

```
Count is 0
Count is 1
Count is 2
```

**`break` and `continue`** (briefly):

- `break` exits the loop immediately.
- `continue` skips the rest of the current iteration and moves to the next.

---

### 1.11 Simple Input/Output

To make scripts interactive, use `input()`:

```python
name = input("Enter your name: ")
print(f"Hello, {name}!")
```

`input()` always returns a string. Convert if needed:

```python
age = int(input("Enter your age: "))
```

---

### 🖥️ Hands-on Exercise

Create a script called `pillar_status.py` that:

1. Defines a dictionary for each Phase 1 pillar (networking, linux, security, scripting, databases) with keys `name` and `completed` (boolean).
2. Stores these dictionaries in a list.
3. Loops through the list and prints:
   - `"Pillar: <name> — COMPLETE"` if `completed` is `True`
   - `"Pillar: <name> — IN PROGRESS"` if `completed` is `False`
4. Asks the user for their current pillar and prints a personalised status message using the data.

```bash
nano pillar_status.py
```

Run: `python3 pillar_status.py`

---

### DevOps Connection

Python is the dominant language for infrastructure automation glue code — custom scripts calling APIs, parsing config files, orchestrating deployment steps beyond what Bash alone handles cleanly. Ansible (Phase 2, Pillar 4) is written in Python; its modules are Python under the hood.

---

**Next section:** [02-python-functions-modules-errors.md](./02-python-functions-modules-errors.md) — Python Functions, Modules & Error Handling
