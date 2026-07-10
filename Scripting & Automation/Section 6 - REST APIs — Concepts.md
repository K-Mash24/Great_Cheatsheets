# Pillar 4 — Scripting & Automation

## Section 6: REST APIs — Concepts

### Section Checklist

- [x] What an API is, and what makes an API "REST"
- [x] Client-server model
- [x] Resources and endpoints
- [x] HTTP methods (GET, POST, PUT, PATCH, DELETE)
- [x] Idempotency of HTTP methods
- [x] Status codes (1xx-5xx categories and common specific codes)
- [x] Headers — request and response metadata
- [x] Request bodies
- [x] Query parameters
- [x] Complete request/response example
- [x] Hands-on practice with curl

---

### 6.1 What is an API?

An **API** (Application Programming Interface) is a defined way for two pieces of software to communicate with each other. Instead of a human clicking buttons in a browser, one program sends a structured request to another program and gets a structured response back.

A **REST API** (Representational State Transfer) is the most common style of web API — it uses standard HTTP (the same protocol a browser uses to load web pages) as its communication method, with a specific set of conventions around how requests and responses are structured.

---

### 6.2 The client-server model

Every API interaction has two sides:

- **Client** — the program making the request (a Python script, a browser, `curl`, another server)
- **Server** — the program receiving the request, processing it, and sending back a response

```
Client  ──── HTTP Request ────>  Server
Client  <─── HTTP Response ───   Server
```

The client always initiates — servers don't reach out to clients unprompted in the standard REST model (that's a different pattern, covered by things like webhooks, outside this section's scope).

---

### 6.3 Resources and endpoints

REST APIs organize everything around **resources** — nouns representing "things" the API manages (a user, an order, a file). Each resource type typically has a base **endpoint** — a URL representing where to interact with it.

```
https://api.example.com/users
https://api.example.com/users/42
https://api.example.com/orders
```

- `/users` — the collection of all users
- `/users/42` — one specific user, identified by ID `42`
- `/orders` — a completely different resource, the collection of orders

> **Convention:** Resource endpoints are almost always **plural nouns** (`/users`, not `/user`), representing a collection. A specific item within that collection is addressed by appending its identifier (`/users/42`).

---

### 6.4 HTTP methods — the verbs

The URL identifies _what_ is being acted on (the resource); the **HTTP method** identifies _what action_ to take.

| Method   | Purpose                                                    | Example                                               |
| -------- | ---------------------------------------------------------- | ----------------------------------------------------- |
| `GET`    | Retrieve data — should never change anything on the server | `GET /users/42` — fetch user 42's data                |
| `POST`   | Create a new resource                                      | `POST /users` — create a new user                     |
| `PUT`    | Replace an existing resource entirely                      | `PUT /users/42` — overwrite all of user 42's data     |
| `PATCH`  | Partially update an existing resource                      | `PATCH /users/42` — update just one field, e.g. email |
| `DELETE` | Remove a resource                                          | `DELETE /users/42` — delete user 42                   |

> **Critical distinction — PUT vs PATCH:** `PUT` expects the _entire_ resource representation and replaces it wholesale — omitted fields may get wiped out or reset to defaults. `PATCH` only touches the fields explicitly included in the request. Using `PUT` when `PATCH` was intended is a common source of accidentally erasing data that wasn't included in the request body.

**Idempotency of methods** (an operation that produces the same result no matter how many times it's applied):

- `GET`, `PUT`, `DELETE` — idempotent. Calling `DELETE /users/42` five times has the same end state as calling it once (user 42 is gone either way).
- `POST` — **not** idempotent by default. Calling `POST /users` five times typically creates five separate new users.

This distinction matters heavily in automation — a retry mechanism that blindly re-sends a failed `POST` request risks creating duplicate resources, whereas retrying a `PUT` or `DELETE` is generally safe.

---

### 6.5 Status codes — the response's headline

Every HTTP response includes a three-digit **status code** summarizing the outcome. They're grouped by their first digit:

| Range | Category      | Meaning                                                   |
| ----- | ------------- | --------------------------------------------------------- |
| `1xx` | Informational | Request received, still processing (rarely seen directly) |
| `2xx` | Success       | The request worked                                        |
| `3xx` | Redirection   | Further action needed to complete the request             |
| `4xx` | Client error  | Something wrong with the request itself                   |
| `5xx` | Server error  | Something went wrong on the server's side                 |

**Commonly encountered codes:**

| Code  | Name                  | Meaning                                                                |
| ----- | --------------------- | ---------------------------------------------------------------------- |
| `200` | OK                    | Request succeeded, response body contains the result                   |
| `201` | Created               | A new resource was successfully created (typical response to `POST`)   |
| `204` | No Content            | Request succeeded, but there's nothing to return (common for `DELETE`) |
| `400` | Bad Request           | The request was malformed — invalid syntax, missing required data      |
| `401` | Unauthorized          | Authentication is required and missing or invalid                      |
| `403` | Forbidden             | Authenticated, but not permitted to perform this action                |
| `404` | Not Found             | The requested resource doesn't exist                                   |
| `429` | Too Many Requests     | Rate limit exceeded — slow down                                        |
| `500` | Internal Server Error | Something broke on the server, unrelated to what was sent              |
| `503` | Service Unavailable   | Server temporarily can't handle the request (overload, maintenance)    |

> **Callout — automation depends on checking these.** A script blindly assuming success because it got _any_ response, without checking the status code, is a common source of silent automation failures — e.g., treating a `404` or `500` response body as valid data.

---

### 6.6 Headers — metadata about the request/response

**Headers** are key-value pairs sent alongside a request or response, carrying metadata that isn't part of the main data itself.

**Common request headers:**

```
Content-Type: application/json
Authorization: Bearer <token>
Accept: application/json
```

- `Content-Type` — tells the server what format the request body is in (almost always `application/json` for modern APIs)
- `Authorization` — carries credentials proving who's making the request (API keys, tokens — covered further in Section 7)
- `Accept` — tells the server what format the client wants the response in

**Common response headers:**

```
Content-Type: application/json
X-RateLimit-Remaining: 42
```

`X-RateLimit-Remaining` (and similar `X-*` headers) are non-standard but extremely common conventions APIs use to communicate things like remaining rate-limit quota.

---

### 6.7 The request body

For methods that send data (`POST`, `PUT`, `PATCH`), the **body** carries the actual payload — typically formatted as **JSON** (JavaScript Object Notation, covered in depth in Section 8).

```json
POST /users
Content-Type: application/json

{
  "name": "Keith",
  "role": "student"
}
```

`GET` and `DELETE` requests typically have no body — any parameters they need are usually passed in the URL itself (see 6.8).

---

### 6.8 Query parameters

Additional options for a request — filters, sorting, pagination — are commonly passed as **query parameters**, appended to the URL after a `?`:

```
GET /users?role=admin&limit=10
```

- `?` starts the query string
- Each parameter is `key=value`
- `&` separates multiple parameters

This example requests users filtered to `role=admin`, limited to `10` results. Query parameters are a `GET`-request convention — since `GET` has no body, filtering criteria travel in the URL instead.

---

### 6.9 A complete request/response example

**Request:**

```
GET /users/42
Authorization: Bearer abc123
Accept: application/json
```

**Response:**

```
Status: 200 OK
Content-Type: application/json

{
  "id": 42,
  "name": "Keith",
  "role": "student"
}
```

Everything from this section is present here: an endpoint (`/users/42`), a method (`GET`), headers (`Authorization`, `Accept`, `Content-Type`), a status code (`200`), and a JSON body.

---

### Pitfalls Table

| Pitfall                                                                   | Why it's a problem                                                | Fix                                                                                            |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Not checking the status code before using the response                    | A `404` or `500` response body might be treated as valid data     | Always check status code first; branch on success vs error                                     |
| Blindly retrying a failed `POST`                                          | Can create duplicate resources since `POST` isn't idempotent      | Use idempotency keys if the API supports them, or check for existing resources before retrying |
| Using `PUT` when `PATCH` was intended                                     | Fields not included in the request body may get wiped or reset    | Use `PATCH` for partial updates; reserve `PUT` for full replacement                            |
| Forgetting `Content-Type: application/json` on a request with a JSON body | Server may fail to parse the body correctly or reject the request | Always set the header explicitly when sending JSON                                             |
| Assuming `GET` requests can carry a body                                  | Many servers ignore or reject bodies on `GET`                     | Pass parameters via the query string instead                                                   |

---

### 🖥️ Hands-on Practice (Codespace terminal)

APIs are best explored with `curl` — a command-line tool for making HTTP requests, available by default in the Codespace.

```bash
curl -i https://jsonplaceholder.typicode.com/users/1
```

`-i` includes the response headers and status line in the output, not just the body. This is a free public test API — safe to experiment against.

Try:

```bash
curl -i https://jsonplaceholder.typicode.com/users/999
```

Notice the status code — this ID doesn't exist, so `404` should appear rather than a silent failure or empty success.

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "test", "body": "hello", "userId": 1}'
```

`-X POST` sets the method, `-H` adds a header, `-d` sends the request body. The status code returned should be `201 Created`.

---

### DevOps Connection

Virtually every modern infrastructure tool exposes or consumes a REST API — Docker, Kubernetes, GitHub, Terraform providers, and monitoring tools like Grafana all communicate over REST underneath their CLIs and dashboards. Understanding status codes and idempotency directly informs writing reliable automation: knowing that a `POST` retry can create duplicates, but a `PUT`/`DELETE` retry is safe, shapes how deployment and provisioning scripts are designed to handle failures.

---

**Next section:** [07-python-requests-library.md](./07-python-requests-library.md) — Working with APIs in Python (requests library)
