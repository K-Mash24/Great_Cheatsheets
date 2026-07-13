# Pillar 4 — Scripting & Automation

## Section 7: Working with APIs in Python (`requests` library)

### Section Checklist

- [x] Installing and importing requests
- [x] Making GET requests, response object attributes
- [x] Checking for success before using a response; raise_for_status()
- [x] Making POST requests with json= payloads
- [x] PUT, PATCH, DELETE requests
- [x] Query parameters via params=
- [x] Headers and authentication (API keys, Basic auth)
- [x] Secrets management via environment variables
- [x] Timeouts as a defensive habit
- [x] Pagination patterns (page-based and cursor-based)
- [x] Hands-on exercise

---

### 7.1 Installing and importing `requests`

`requests` is Python's most widely used library for making HTTP calls — it wraps the messy details of raw socket/HTTP handling into a simple, readable interface.

```bash
pip install requests --break-system-packages
```

```python
import requests
```

> `requests` is a third-party library, not part of Python's standard library — unlike `os`, `json`, or `sys` from Section 2, it must be installed separately before it can be imported.

---

### 7.2 Making a `GET` request

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1")
print(response.status_code)   # 200
print(response.text)          # raw response body as a string
```

The `response` object bundles status code, headers, and body from Section 6 into one object with convenient attributes and methods.

**Key `response` attributes:**

| Attribute/Method       | Returns                                                                                 |
| ---------------------- | --------------------------------------------------------------------------------------- |
| `response.status_code` | The HTTP status code as an integer, e.g. `200`                                          |
| `response.text`        | The response body as a raw string                                                       |
| `response.json()`      | The response body parsed into a Python dict/list (only works if the body is valid JSON) |
| `response.headers`     | A dict-like object of response headers                                                  |
| `response.ok`          | `True` if status code is under `400`, `False` otherwise                                 |

**Parsing JSON directly:**

```python
response = requests.get("https://jsonplaceholder.typicode.com/users/1")
data = response.json()
print(data["name"])    # accesses it like any Python dict
```

`.json()` does the equivalent of `json.loads(response.text)` (JSON-parsing mechanics covered in Section 8) — it's a convenience method built into `requests` itself.

---

### 7.3 Checking for success before using the response

```python
response = requests.get("https://jsonplaceholder.typicode.com/users/999")

if response.status_code == 200:
    data = response.json()
    print(data["name"])
else:
    print(f"Request failed with status {response.status_code}")
```

> **Critical:** Never assume a request succeeded just because it returned _a_ response — a failed request (`404`, `500`) still returns a valid `response` object; only the status code confirms the body actually contains what's expected. Calling `.json()` on an error response can raise its own exception if the error body isn't valid JSON, compounding the confusion.

**`raise_for_status()`** — a shortcut that raises an exception automatically on any `4xx`/`5xx` response:

```python
try:
    response = requests.get("https://jsonplaceholder.typicode.com/users/999")
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
```

This combines Section 2's `try/except` directly with API error handling — a very common real-world pattern.

---

### 7.4 Making a `POST` request

```python
import requests

payload = {"title": "test post", "body": "hello", "userId": 1}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)

print(response.status_code)   # 201
print(response.json())
```

The `json=` parameter does two things automatically:

1. Converts the Python dict `payload` into a JSON string
2. Sets the `Content-Type: application/json` header automatically

This replaces manually setting headers and serializing data — `requests` handles both, which is exactly why it's preferred over lower-level HTTP libraries.

---

### 7.5 `PUT`, `PATCH`, and `DELETE`

```python
# PUT - full replacement
response = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"id": 1, "title": "updated", "body": "new content", "userId": 1}
)

# PATCH - partial update
response = requests.patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"title": "just updating the title"}
)

# DELETE
response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)   # 200 (this test API always returns 200, real APIs often return 204)
```

Each method mirrors its corresponding HTTP verb from Section 6 directly — `requests.get()`, `requests.post()`, `requests.put()`, `requests.patch()`, `requests.delete()`.

---

### 7.6 Query parameters

Rather than manually building a URL string with `?key=value&key2=value2`, `requests` handles it via the `params` argument:

```python
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1}
)
print(response.url)   # https://jsonplaceholder.typicode.com/posts?userId=1
```

`requests` handles URL-encoding special characters automatically — spaces, ampersands, etc. in parameter values — which is easy to get wrong doing it manually.

---

### 7.7 Headers and authentication

Most real-world APIs require authentication — proving who's making the request. Two of the most common patterns:

**API key in a header:**

```python
headers = {"Authorization": "Bearer abc123token"}
response = requests.get("https://api.example.com/data", headers=headers)
```

**Basic authentication (username/password):**

```python
response = requests.get(
    "https://api.example.com/data",
    auth=("username", "password")
)
```

`requests` handles encoding the `auth` tuple into the correct `Authorization` header format automatically.

> **Critical security callout:** Never hardcode API keys, tokens, or passwords directly into a script committed to a repository. Load them from environment variables instead:
>
> ```python
> import os
> token = os.environ.get("API_TOKEN")
> headers = {"Authorization": f"Bearer {token}"}
> ```
>
> This ties directly back to `os` from Section 2 and to the security principles from Pillar 3 — a secret leaked into `Great_Cheatsheets` or `DevOps-Journey` git history is extremely difficult to fully remove afterward, even after "deleting" it in a later commit.

---

### 7.8 Timeouts — a critical defensive habit

By default, `requests` waits **indefinitely** for a server to respond — a hung server can freeze the entire script forever.

```python
try:
    response = requests.get("https://api.example.com/data", timeout=5)
except requests.exceptions.Timeout:
    print("Request timed out after 5 seconds")
```

`timeout=5` means "give up and raise an exception if no response arrives within 5 seconds."

> **Callout:** Always set a `timeout` on requests used in automation. A script without one, running as a scheduled job, can hang indefinitely on a slow or dead server — turning a five-minute cron job into one that never finishes and blocks everything scheduled after it.

---

### 7.9 Pagination

APIs handling large datasets rarely return everything in one response — they **paginate**, returning a limited number of results per request along with information on how to get the next batch.

**Common pagination style — page number and page size:**

```python
import requests

all_users = []
page = 1

while True:
    response = requests.get(
        "https://api.example.com/users",
        params={"page": page, "per_page": 50},
        timeout=5
    )
    data = response.json()

    if not data:          # empty list means no more results
        break

    all_users.extend(data)
    page += 1

print(f"Total users fetched: {len(all_users)}")
```

**Common pagination style — cursor/token-based** (frequent in modern APIs like GitHub's):

```python
all_items = []
url = "https://api.example.com/items"

while url:
    response = requests.get(url, timeout=5)
    data = response.json()
    all_items.extend(data["results"])
    url = data.get("next_page_url")   # None once there are no more pages
```

Both patterns share the same shape: loop, request a batch, accumulate results, check for a "more data" signal, repeat until it's gone. The specific mechanism (page numbers vs cursor tokens) varies by API — always check the target API's documentation for which style it uses.

---

### Pitfalls Table

| Pitfall                                                                                                       | Why it's a problem                                                                    | Fix                                                                             |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Not checking status code before calling `.json()`                                                             | Error response bodies may not be valid JSON, raising a confusing secondary exception  | Check `response.status_code` or use `raise_for_status()` first                  |
| No `timeout` set                                                                                              | A hung server freezes the script indefinitely                                         | Always pass `timeout=` (e.g. `timeout=5`)                                       |
| Hardcoding API keys/tokens in script source                                                                   | Secrets committed to git history are extremely hard to fully remove later             | Load credentials via `os.environ.get()`                                         |
| Assuming all APIs paginate the same way                                                                       | A script written for page-based pagination silently breaks against a cursor-based API | Always check the specific API's documentation for its pagination style          |
| Forgetting `json=` sends `Content-Type` automatically and using `data=` with a manually dumped string instead | Easy to forget the header, causing servers to reject or misparse the body             | Prefer `json=payload` over manually serializing with `json.dumps()` and `data=` |

---

### 🖥️ Hands-on Exercise

In `/workspaces/DevOps-Journey`:

```bash
nano api_practice.py
```

1. Make a `GET` request to `https://jsonplaceholder.typicode.com/posts`, with `timeout=5`
2. Use `raise_for_status()` inside a `try/except requests.exceptions.HTTPError` block
3. Parse the JSON response and print the `title` of the first 5 posts using a `for` loop with slicing (`data[:5]`)
4. Make a `POST` request creating a new post with a `json=` payload, and print the resulting status code and the `id` field from the response

Run: `python3 api_practice.py`

---

### DevOps Connection

Nearly every infrastructure automation task involving a cloud provider, monitoring tool, or CI/CD platform ultimately comes down to Python scripts wrapping this exact `requests` pattern — authenticate, request, check status, parse JSON, handle pagination. Tools like the AWS SDK (`boto3`) are essentially very elaborate wrappers around this same fundamental workflow, tailored to a specific API's endpoints and authentication scheme.

---

**Next section:** [08-json-parsing.md](./08-json-parsing.md) — JSON Parsing & Data Manipulation
