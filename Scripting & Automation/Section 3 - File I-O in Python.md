# Pillar 4 — Scripting & Automation

## Section 3: File I/O in Python

### Section Checklist

- [x] Why file I/O matters for automation
- [x] open() and file modes (r, w, a, x, r+)
- [x] Binary modes (rb, wb) and encoding
- [x] with statement / context managers
- [x] Reading files: read(), readlines(), iterating line-by-line
- [x] Writing files: write(), writelines()
- [x] Appending vs overwriting
- [x] Checking file existence: os.path.exists() vs try/except FileNotFoundError
- [x] Working with file paths: os.path.join() and pathlib
- [x] Manual parsing of simple delimited data
- [x] Hands-on exercise

---

### 3.1 Why file I/O matters for automation

Scripts in DevOps constantly read configuration, write logs, or process data dumped by other tools. Being comfortable opening, reading, and writing files is the difference between a script that only works interactively and one that runs unattended as part of a pipeline.

---

### 3.2 Opening a file — the basics

```python
f = open("notes.txt", "r")
content = f.read()
print(content)
f.close()
```

`open()` takes a filename and a **mode**:

| Mode   | Meaning                                                        |
| ------ | -------------------------------------------------------------- |
| `"r"`  | Read (default) — file must exist                               |
| `"w"`  | Write — creates file if missing, **overwrites** if it exists   |
| `"a"`  | Append — creates file if missing, adds to the end if it exists |
| `"x"`  | Exclusive create — fails if file already exists                |
| `"r+"` | Read and write, file must exist                                |
| `"rb"` | Read binary (e.g., images, binaries)                           |
| `"wb"` | Write binary                                                   |

> **Critical:** `"w"` mode **destroys existing content** the instant the file is opened, even if `.write()` is never called. Double-check the mode before running a script against a file you care about.

Calling `f.close()` manually is required to release the file handle — forgetting it can leave data unflushed to disk or lock the file on some systems.

---

### 3.3 The `with` statement — context managers (the correct way)

Manually closing files is error-prone — an exception between `open()` and `close()` skips the close entirely. Python's `with` statement guarantees the file closes automatically, even if an error occurs inside the block.

```python
with open("notes.txt", "r") as f:
    content = f.read()
    print(content)
# f is automatically closed here, even if an exception occurred above
```

This is called a **context manager** — `with` handles setup (opening) and guaranteed teardown (closing) around the indented block. This is the idiomatic way to work with files in Python; manual `open()`/`close()` is considered legacy style going forward.

**Note:** `with` works with any context manager, not just files — database connections, network sockets, and locks all use the same pattern.

**Specifying encoding** (critical for cross-platform compatibility):

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

Without specifying encoding, Python uses the system default, which may differ across platforms and cause unexpected errors when reading files with non-ASCII characters.

---

### 3.4 Reading files — three methods

```python
with open("notes.txt", "r") as f:
    content = f.read()          # entire file as one string
```

```python
with open("notes.txt", "r") as f:
    lines = f.readlines()       # list of strings, one per line (each keeps its trailing \n)
```

```python
with open("notes.txt", "r") as f:
    for line in f:               # memory-efficient — reads one line at a time
        print(line.strip())      # .strip() removes the trailing newline
```

**When to use which:**

- `.read()` — small files, need the whole content as one block (e.g., a config string)
- `.readlines()` — need random access to specific lines, or need a list to manipulate
- Iterating directly over `f` — large files, processing line-by-line without loading everything into memory at once

---

### 3.5 Writing files

```python
with open("output.txt", "w") as f:
    f.write("First line\n")
    f.write("Second line\n")
```

> Note: `.write()` does **not** add a newline automatically — `\n` must be included manually, unlike `print()` which adds one by default.

**Writing multiple lines from a list:**

```python
lines = ["docker\n", "kubernetes\n", "terraform\n"]

with open("tools.txt", "w") as f:
    f.writelines(lines)
```

`.writelines()` does not add newlines between items either — they must already be present in each string.

---

### 3.6 Appending vs overwriting

```python
# First run
with open("log.txt", "w") as f:
    f.write("Log started\n")

# Second run — using "w" again would DESTROY the first line
with open("log.txt", "a") as f:
    f.write("Second entry\n")
```

After both runs, `log.txt` contains:

```
Log started
Second entry
```

Using `"w"` on the second run instead of `"a"` would leave only `Second entry` — the first line gone without warning.

---

### 3.7 Checking whether a file exists first

Attempting to read a file that doesn't exist raises `FileNotFoundError`:

```python
>>> open("missing.txt", "r")
FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
```

Two common approaches — check first, or handle the exception:

**Check first (using `os.path`):**

```python
import os

if os.path.exists("notes.txt"):
    with open("notes.txt", "r") as f:
        print(f.read())
else:
    print("File not found")
```

**Handle the exception (often preferred — avoids a race condition where the file could be deleted between the check and the open):**

```python
try:
    with open("notes.txt", "r") as f:
        print(f.read())
except FileNotFoundError:
    print("File not found")
```

> **Callout:** The exception-handling approach is generally more robust in real automation scripts. Checking existence first and then opening is technically two separate operations — something else (another process, a scheduled cleanup job) could delete the file in between, causing the "checked" branch to still fail.

---

### 3.8 Working with file paths

Hardcoding paths like `"notes.txt"` only works if the script runs from the exact directory containing that file.

**Using `os.path` (traditional):**

```python
import os

path = os.path.join("saa-foundation", "04-scripting", "notes.txt")
print(path)   # saa-foundation/04-scripting/notes.txt
```

`os.path.join()` handles the correct path separator for the operating system automatically (`/` on Linux/Mac, `\` on Windows) — safer than hardcoding slashes.

**Useful `os.path` functions:**

```python
os.path.exists(path)     # True/False — does it exist
os.path.isfile(path)     # True/False — is it a file (not a directory)
os.path.isdir(path)      # True/False — is it a directory
os.path.abspath(path)    # converts to full absolute path
os.path.basename(path)   # just the filename, e.g. 'notes.txt'
os.path.dirname(path)    # just the directory portion
```

**Using `pathlib` (modern, recommended):**

```python
from pathlib import Path

path = Path("saa-foundation") / "04-scripting" / "notes.txt"
print(path)               # saa-foundation/04-scripting/notes.txt
print(path.exists())      # True/False
print(path.is_file())     # True/False
print(path.name)          # 'notes.txt'
print(path.parent)        # 'saa-foundation/04-scripting'

# Read and write directly from pathlib
content = Path("notes.txt").read_text()
Path("output.txt").write_text("Hello, World!\n")
```

> `pathlib` is the modern standard in Python 3.4+ and is more intuitive than `os.path`. It's worth adopting for new code.

---

### 3.9 Reading and writing simple delimited data manually

Not every task needs the `csv` module — sometimes simple line-splitting is enough for basic comma- or pipe-separated data:

```python
with open("servers.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        name, ip = parts[0], parts[1]
        print(f"Server: {name}, IP: {ip}")
```

Given `servers.txt` containing:

```
web01,192.168.1.10
web02,192.168.1.11
```

Output:

```
Server: web01, IP: 192.168.1.10
Server: web02, IP: 192.168.1.11
```

> For anything beyond trivial comma-separated lines (quoted fields, embedded commas, headers), Python's built-in `csv` module handles edge cases this manual approach doesn't — worth knowing it exists even though it's outside this section's scope.

---

### Pitfalls Table

| Pitfall                                             | Why it's a problem                                                                          | Fix                                                                          |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Using `"w"` mode on a file you meant to append to   | Silently destroys all existing content the moment the file is opened                        | Use `"a"` for appending; double check mode before running against real files |
| Forgetting `.close()` on manually opened files      | File handle stays open, risking unflushed data or resource leaks in long-running scripts    | Always use `with open(...) as f:` instead of manual open/close               |
| Assuming `.write()` adds a newline                  | Output lines run together with no separation                                                | Explicitly append `\n` to each write                                         |
| Checking `os.path.exists()` then opening separately | Race condition — file can be deleted between the check and the open, causing a crash anyway | Prefer `try/except FileNotFoundError` around the open itself                 |
| Hardcoding paths with `/` or `\`                    | Breaks when the script runs on a different OS                                               | Use `os.path.join()` or `pathlib` to build paths portably                    |
| Not specifying `encoding`                           | Different systems may use different default encodings, causing `UnicodeDecodeError`         | Always use `encoding="utf-8"` for text files                                 |
| Using `.read()` on a huge file                      | Loads the entire file into memory, potentially exhausting RAM                               | Use iteration over the file object for large files                           |

---

### 🖥️ Hands-on Exercise

In `/workspaces/DevOps-Journey`:

```bash
nano file_practice.py
```

**Part 1:**

1. Write three pillar names to `pillars.txt`, one per line, using `"w"` mode
2. Reopen the file with `"r"` mode and print each line (stripped of the trailing newline) using a `for` loop over the file object
3. Append a fourth pillar name using `"a"` mode
4. Wrap the read operation in a `try/except FileNotFoundError` block

**Part 2:**

5. Create a list of dictionaries: `[{"name": "web01", "ip": "192.168.1.10"}, {"name": "web02", "ip": "192.168.1.11"}]`
6. Write them to `servers.csv` in a simple comma-separated format (name,ip) using `"w"`
7. Read the file back and print each server's name and IP

Run: `python3 file_practice.py`, then `cat pillars.txt` and `cat servers.csv` to confirm the file contents match expectations.

---

### DevOps Connection

Reading configuration files, parsing log files, and writing structured output are constant tasks in automation — a deployment script might read a list of servers from a file to loop over, or a monitoring script might tail a log file looking for error patterns. The `with` statement's guaranteed cleanup matters even more in long-running automation, where an unclosed file handle in a script that runs thousands of times can quietly exhaust system resources.

---

**Next section:** [04-bash-scripting-fundamentals.md](./04-bash-scripting-fundamentals.md) — Bash Scripting Fundamentals
