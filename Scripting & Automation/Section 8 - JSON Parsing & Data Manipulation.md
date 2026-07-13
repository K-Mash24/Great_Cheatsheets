# Pillar 4 — Scripting & Automation

## Section 8: JSON Parsing & Data Manipulation

### Section Checklist

- [x] What JSON is and its data types vs Python equivalents
- [x] Python json module: loads(), load(), dumps(), dump()
- [x] Parsing JSON strings with json.loads()
- [x] Converting Python to JSON with json.dumps(), pretty-printing with indent
- [x] Reading/writing JSON files directly with load()/dump()
- [x] Navigating nested JSON structures
- [x] Handling missing keys safely with .get()
- [x] Handling malformed JSON (JSONDecodeError)
- [x] jq for command-line JSON parsing in Bash
- [x] Hands-on exercise (Python + Bash)

---

### 8.1 What is JSON?

**JSON** (JavaScript Object Notation) is a lightweight, text-based data format for representing structured data. Despite the name, it's language-agnostic — virtually every programming language can read and write it. It's the dominant format for REST API request/response bodies (Sections 6–7) and for configuration files.

```json
{
  "name": "Keith",
  "pillar": 4,
  "active": true,
  "tools": ["docker", "kubernetes"],
  "cert": null
}
```

**JSON data types and their Python equivalents:**

| JSON type        | Python equivalent | Notes                                                 |
| ---------------- | ----------------- | ----------------------------------------------------- |
| object `{}`      | `dict`            | key-value pairs, keys always in double quotes         |
| array `[]`       | `list`            | ordered collection                                    |
| string           | `str`             | always double-quoted — single quotes are invalid JSON |
| number           | `int` or `float`  | no distinction in JSON itself                         |
| `true` / `false` | `True` / `False`  | lowercase in JSON, capitalized in Python              |
| `null`           | `None`            | JSON's version of "no value"                          |

> **Critical syntax note:** JSON requires **double quotes** for strings and keys — `{'name': 'Keith'}` (single quotes) is **not** valid JSON, even though it's valid Python. This trips people up constantly when hand-writing JSON payloads.

---

### 8.2 Python's `json` module — the four core functions

```python
import json
```

| Function       | Direction                   | Purpose                                      |
| -------------- | --------------------------- | -------------------------------------------- |
| `json.loads()` | JSON string → Python object | Parse a JSON string already in memory        |
| `json.load()`  | JSON file → Python object   | Parse JSON directly from an open file        |
| `json.dumps()` | Python object → JSON string | Serialize a Python object to a JSON string   |
| `json.dump()`  | Python object → JSON file   | Serialize and write directly to an open file |

The naming pattern: **no `s`** means it works with **files**; **with `s`** means it works with **strings** already in memory ("loads" = "load string", "dumps" = "dump string").

---

### 8.3 `json.loads()` — parsing a JSON string

```python
import json

json_string = '{"name": "Keith", "pillar": 4, "active": true}'
data = json.loads(json_string)

print(data["name"])       # Keith
print(type(data))         # <class 'dict'>
```

This is exactly what `response.json()` does internally in Section 7 — `requests` calls `json.loads()` on `response.text` behind the scenes.

---

### 8.4 `json.dumps()` — converting Python back to a JSON string

```python
import json

data = {"name": "Keith", "pillar": 4, "active": True}
json_string = json.dumps(data)

print(json_string)
# {"name": "Keith", "pillar": 4, "active": true}
print(type(json_string))   # <class 'str'>
```

Notice `True` (Python) became `true` (JSON) automatically — `json.dumps()` handles this type conversion.

**Pretty-printing with `indent`:**

```python
print(json.dumps(data, indent=2))
```

Output:

```json
{
  "name": "Keith",
  "pillar": 4,
  "active": true
}
```

Without `indent`, `dumps()` produces a single compact line — fine for sending over the network, unreadable for humans debugging output. `indent=2` (or `4`) formats it for readability.

---

### 8.5 Reading and writing JSON files directly

```python
import json

# Writing
data = {"name": "Keith", "pillar": 4}
with open("config.json", "w") as f:
    json.dump(data, f, indent=2)

# Reading
with open("config.json", "r") as f:
    loaded_data = json.load(f)

print(loaded_data["name"])   # Keith
```

`json.load(f)` and `json.dump(data, f, ...)` take the file object `f` directly — no need to manually `.read()` the file first and then call `json.loads()` on the resulting string, though that would also work. Combining this with Section 3's `with` statement is the standard pattern for config files in real scripts.

---

### 8.6 Navigating nested JSON structures

Real-world JSON is rarely flat — it commonly nests objects inside objects, and arrays of objects:

```python
data = {
    "user": {
        "name": "Keith",
        "pillars": ["networking", "linux", "security"],
        "contact": {
            "email": "keith@example.com"
        }
    }
}

print(data["user"]["name"])                    # Keith
print(data["user"]["pillars"][0])              # networking
print(data["user"]["contact"]["email"])        # keith@example.com
```

Chained bracket access mirrors the nesting structure exactly — each `[]` steps one level deeper.

**Looping over a list of nested objects** (a very common API response shape):

```python
users = [
    {"name": "Keith", "role": "student"},
    {"name": "Alice", "role": "mentor"}
]

for user in users:
    print(f"{user['name']} — {user['role']}")
```

Output:

```
Keith — student
Alice — mentor
```

---

### 8.7 Handling missing keys safely

Directly indexing a dict with `[]` raises `KeyError` if the key doesn't exist:

```python
data = {"name": "Keith"}
print(data["email"])   # KeyError: 'email'
```

**`.get()`** — the safer alternative, returning `None` (or a specified default) instead of raising an exception:

```python
print(data.get("email"))              # None
print(data.get("email", "no email"))  # no email
```

> **Critical for real-world API data:** Fields are often optional or inconsistently present across different records in a response. Using `.get()` instead of `[]` when parsing external data prevents a single missing field from crashing an entire batch-processing script — directly connecting back to Section 2's error-handling philosophy.

---

### 8.8 Handling malformed JSON

```python
import json

bad_json = '{"name": "Keith", "pillar": }'   # missing value — invalid JSON

try:
    data = json.loads(bad_json)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

`json.JSONDecodeError` is raised when the string simply isn't valid JSON syntax — distinct from `KeyError` (a missing key in otherwise-valid JSON). Scripts parsing JSON from external, untrusted, or unreliable sources (an API having a bad day, a corrupted config file) should anticipate both failure modes.

---

### 8.9 `jq` — JSON parsing from the command line / Bash

`jq` is a command-line tool for filtering and transforming JSON, used constantly alongside `curl` in Bash scripts (tying directly back to Sections 4–6).

```bash
curl -s https://jsonplaceholder.typicode.com/users/1 | jq
```

`-s` (silent) suppresses `curl`'s progress output; piping into `jq` pretty-prints the JSON automatically.

**Extracting a specific field:**

```bash
curl -s https://jsonplaceholder.typicode.com/users/1 | jq '.name'
```

Output:

```
"Keith Mash"
```

`.name` accesses the `name` key — the leading `.` is required syntax for `jq`, representing "the root of the JSON document."

**Nested field access:**

```bash
curl -s https://jsonplaceholder.typicode.com/users/1 | jq '.address.city'
```

**Extracting from an array of objects:**

```bash
curl -s https://jsonplaceholder.typicode.com/users | jq '.[0].name'
```

`.[0]` accesses the first element of the top-level array, then `.name` on that element.

**Extracting a field from every item in an array:**

```bash
curl -s https://jsonplaceholder.typicode.com/users | jq '.[].name'
```

`.[]` (no index) iterates over every element, applying `.name` to each — outputs one quoted string per user.

**Raw output without quotes** (useful for piping into other commands or variables):

```bash
curl -s https://jsonplaceholder.typicode.com/users/1 | jq -r '.name'
```

Output:

```
Keith Mash
```

`-r` strips the surrounding quotes `jq` normally adds — critical when the extracted value needs to be used directly in a Bash variable or another command, since `"Keith Mash"` (with quotes) and `Keith Mash` behave differently once assigned to a shell variable.

**Combining with Bash variables (ties directly to Sections 4–5):**

```bash
name=$(curl -s https://jsonplaceholder.typicode.com/users/1 | jq -r '.name')
echo "User name: $name"
```

---

### Pitfalls Table

| Pitfall                                                      | Why it's a problem                                                                       | Fix                                                                                |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Hand-writing JSON with single quotes                         | Invalid JSON — `json.loads()` will raise `JSONDecodeError`                               | Always use double quotes for JSON strings and keys                                 |
| Using `[]` instead of `.get()` on external/API data          | A single missing key raises `KeyError` and can crash batch processing                    | Use `.get()` with a sensible default when parsing untrusted or variable-shape data |
| Forgetting `-r` when piping `jq` output into a Bash variable | The variable ends up containing literal quote characters                                 | Add `-r` to strip quotes from string output                                        |
| Assuming all JSON parses successfully                        | Malformed JSON (missing commas, unquoted keys, trailing commas) raises `JSONDecodeError` | Wrap parsing in `try/except json.JSONDecodeError` for untrusted input              |
| Confusing `jq '.[0]'` and `jq '.[]'`                         | `.[0]` returns one element; `.[]` returns/iterates all elements — easy to mix up         | Remember: index number = one item, empty brackets = every item                     |

---

### 🖥️ Hands-on Exercise

In `/workspaces/DevOps-Journey`:

**Python side** — `nano json_practice.py`:

1. Create a nested Python dict representing a pillar (`name`, `sections_complete`, and a nested `topics` list)
2. Write it to `pillar_status.json` using `json.dump()` with `indent=2`
3. Read it back with `json.load()` and print the `topics` list using a `for` loop
4. Use `.get()` to safely check for a `"deadline"` key that doesn't exist, printing a default message if absent

**Bash side** — in the terminal: 5. Run `cat pillar_status.json | jq '.topics'` 6. Run `cat pillar_status.json | jq -r '.name'` and confirm the output has no surrounding quotes

---

### DevOps Connection

JSON is the universal data-interchange format across the entire DevOps toolchain — Kubernetes manifests (often authored in YAML but convertible to/from JSON), Terraform state files, GitHub Actions workflow outputs, and every cloud provider's CLI (`--output json`) all speak JSON. `jq` specifically is a staple in CI/CD pipeline scripts for extracting values from tool output to pass into subsequent steps.

---

**Next section:** [09-automation-patterns.md](./09-automation-patterns.md) — Automation Patterns (scheduling, idempotency, logging, error handling)
