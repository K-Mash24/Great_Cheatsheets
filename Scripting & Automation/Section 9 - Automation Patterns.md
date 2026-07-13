# Pillar 4 — Scripting & Automation

## Section 9: Automation Patterns

### Section Checklist

- [x] What makes a script "automation-ready"
- [x] Idempotency principle and check-before-act pattern
- [x] Idempotency applied to API operations
- [x] Logging module vs print(), severity levels
- [x] Combining logging with error handling
- [x] Retry logic with exponential backoff
- [x] Scheduling automation with cron (syntax, examples, crontab)
- [x] Cron environment pitfalls
- [x] Full realistic automation script example
- [x] Hands-on exercise

---

### 9.1 What makes a script "automation-ready"?

Everything up to this point covered how to write functional scripts. This section covers what separates a script that works _once, when run and watched_ from one that works reliably _unattended, on a schedule, for months, without anyone watching._ This section ties Sections 1–8 together into production-quality thinking.

---

### 9.2 Idempotency — the central automation principle

An **idempotent** operation produces the same end state no matter how many times it's applied.

Why this matters for automation specifically: scheduled scripts, retries, and re-runs are inevitable. A script that isn't idempotent creates a growing list of problems every time it accidentally runs twice.

**Non-idempotent example:**

```python
def create_log_entry():
    with open("audit.log", "a") as f:
        f.write("User created\n")
```

Run this script twice (e.g., a retry after a network blip made it look like it failed) and `audit.log` now falsely shows two user-creation events instead of one.

**Idempotent version — check before acting:**

```python
import os

def create_log_entry():
    entry = "User created\n"
    if os.path.exists("audit.log"):
        with open("audit.log", "r") as f:
            if entry in f.read():
                return   # already logged, do nothing
    with open("audit.log", "a") as f:
        f.write(entry)
```

Now running it multiple times leaves the same end state as running it once.

**The general idempotency pattern:**

1. Check whether the desired end state already exists
2. If yes, do nothing (or confirm and exit cleanly)
3. If no, make the change

This exact pattern is why Terraform and Ansible (Phase 2) can be safely re-run repeatedly — they check current state before making changes, rather than blindly re-executing every action.

---

### 9.3 Idempotency with API operations

Tying back to Section 6/7's discussion of HTTP method idempotency — the same principle applies at the script level:

```python
import requests

def ensure_user_exists(name, email):
    # Check first
    response = requests.get(
        "https://api.example.com/users",
        params={"email": email},
        timeout=5
    )
    existing = response.json()

    if existing:
        print(f"User {email} already exists — skipping creation")
        return existing[0]

    # Only create if it doesn't already exist
    response = requests.post(
        "https://api.example.com/users",
        json={"name": name, "email": email},
        timeout=5
    )
    return response.json()
```

This wraps a non-idempotent `POST` in a "check-then-act" pattern, making the overall function safe to call repeatedly.

---

### 9.4 Logging — replacing `print()` with structured records

`print()` has been used throughout this pillar for simplicity, but real automation scripts use Python's built-in `logging` module instead. The difference matters once a script runs unattended: `print()` output vanishes unless someone happened to be watching the terminal, while logs can be written to a file, timestamped, and categorized by severity.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="script.log"
)

logging.info("Script started")
logging.warning("Config value missing, using default")
logging.error("Failed to connect to API")
```

Output written to `script.log`:

```
2026-07-13 10:15:32 [INFO] Script started
2026-07-13 10:15:33 [WARNING] Config value missing, using default
2026-07-13 10:15:34 [ERROR] Failed to connect to API
```

**Logging severity levels, in increasing order of seriousness:**

| Level      | When to use                                                                        |
| ---------- | ---------------------------------------------------------------------------------- |
| `DEBUG`    | Fine-grained diagnostic detail, useful only when actively troubleshooting          |
| `INFO`     | Normal operation milestones — "script started," "processed 50 records"             |
| `WARNING`  | Something unexpected but not breaking — a missing optional config, a slow response |
| `ERROR`    | Something failed — a request errored, a file couldn't be read                      |
| `CRITICAL` | The whole script/system is in serious trouble and likely can't continue            |

Setting `level=logging.INFO` means messages at `INFO` and above are recorded; `DEBUG` messages are silently ignored unless the level is lowered. This lets a script ship with verbose `DEBUG` logging built in, quietly available by changing one line, without cluttering normal output.

> **Callout:** For any script that runs unattended (cron job, CI/CD step), logging to a file is not optional in practice — it's the only record of what happened if something goes wrong at 3 AM with nobody watching.

---

### 9.5 Combining logging with error handling

```python
import logging
import requests

logging.basicConfig(level=logging.INFO, filename="script.log",
                     format="%(asctime)s [%(levelname)s] %(message)s")

def fetch_data(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        logging.info(f"Successfully fetched {url}")
        return response.json()
    except requests.exceptions.Timeout:
        logging.error(f"Timeout while fetching {url}")
        return None
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error fetching {url}: {e}")
        return None
```

This is Section 2's `try/except` and Section 7's `requests` error handling, now feeding into a permanent, timestamped record instead of a `print()` statement that disappears the moment the terminal closes.

---

### 9.6 Retry logic with backoff

Transient failures (a brief network blip, a server momentarily overloaded) are common enough that automation scripts often retry before giving up entirely — but retrying instantly and repeatedly can make an already-struggling server worse.

```python
import time
import logging

def fetch_with_retry(url, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt == max_attempts:
                logging.error(f"All {max_attempts} attempts failed for {url}")
                raise
            time.sleep(2 ** attempt)   # exponential backoff: 2s, 4s, 8s...
```

`2 ** attempt` is **exponential backoff** — each retry waits longer than the last (2 seconds, then 4, then 8), giving a struggling server increasing breathing room rather than hammering it with immediate retries.

> **Critical connection:** This is only safe to do because of Section 9.3's idempotency pattern. Retrying a non-idempotent `POST` blindly can create duplicate resources on every retry — retry logic and idempotency are two halves of the same reliability strategy.

---

### 9.7 Scheduling automation — `cron`

**`cron`** is the standard Linux utility for running scripts automatically on a schedule, without any human triggering them.

**Cron syntax — five fields plus the command:**

```
* * * * * /path/to/script.sh
│ │ │ │ │
│ │ │ │ └── day of week (0-6, Sunday=0)
│ │ │ └──── month (1-12)
│ │ └────── day of month (1-31)
│ └──────── hour (0-23)
└────────── minute (0-59)
```

**Examples:**

```bash
# Run every day at 2:00 AM
0 2 * * * /home/user/backup.sh

# Run every 15 minutes
*/15 * * * * /home/user/check_status.sh

# Run every Monday at 9:00 AM
0 9 * * 1 /home/user/weekly_report.sh
```

**Editing your crontab:**

```bash
crontab -e
```

Opens an editor where each line is one scheduled job, using the syntax above.

**Viewing current scheduled jobs:**

```bash
crontab -l
```

> **Critical automation pitfall:** Cron jobs run in a minimal environment — they don't have the same `PATH`, environment variables, or working directory as an interactive terminal session. A script that works fine when run manually can fail silently under cron because it can't find a command it assumed was available, or a relative file path doesn't resolve to what was expected. Always use absolute paths in cron-scheduled scripts, and explicitly set any environment variables the script needs.

---

### 9.8 Bringing it all together — a realistic automation script shape

```python
#!/usr/bin/env python3
import logging
import time
import requests
import os

logging.basicConfig(
    level=logging.INFO,
    filename="automation.log",
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def check_resource_exists(name):
    """Idempotency check before acting."""
    response = requests.get(
        "https://api.example.com/resources",
        params={"name": name},
        timeout=5
    )
    return len(response.json()) > 0

def create_resource(name, max_attempts=3):
    """Retry with exponential backoff."""
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.post(
                "https://api.example.com/resources",
                json={"name": name},
                timeout=5
            )
            response.raise_for_status()
            logging.info(f"Created resource: {name}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt == max_attempts:
                logging.error(f"Failed to create {name} after {max_attempts} attempts")
                raise
            time.sleep(2 ** attempt)

def main():
    resource_name = "web-server-01"

    if check_resource_exists(resource_name):
        logging.info(f"{resource_name} already exists — nothing to do")
        return

    create_resource(resource_name)

if __name__ == "__main__":
    main()
```

Every piece introduced across this entire pillar appears here: functions and modules (Section 2), the `requests` library (Section 7), JSON handling (Section 8), idempotency, logging, and retry logic (Section 9). This is the realistic shape of a small production automation script.

> **Note on `if __name__ == "__main__":`** — this guard ensures `main()` only runs when the script is executed directly (`python3 script.py`), not when it's imported as a module into another script. Standard convention for any script that might also be reused as a library.

---

### Pitfalls Table

| Pitfall                                                | Why it's a problem                                                        | Fix                                                               |
| ------------------------------------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Non-idempotent operations in scheduled/retried scripts | Duplicate resources, duplicate log entries, or corrupted state on re-run  | Always check current state before acting (check-then-act pattern) |
| Using `print()` in unattended scripts                  | Output vanishes with no record if nobody was watching the terminal        | Use the `logging` module writing to a file                        |
| Retrying instantly and repeatedly on failure           | Can worsen an already-struggling server ("retry storm")                   | Use exponential backoff (`time.sleep(2 ** attempt)`)              |
| Retrying non-idempotent operations blindly             | Can create duplicate resources on every retry                             | Combine retry logic with idempotency checks                       |
| Relative file paths or missing env vars in cron jobs   | Script works manually but fails silently under cron's minimal environment | Use absolute paths; explicitly set required environment variables |

---

### 🖥️ Hands-on Exercise

In `/workspaces/DevOps-Journey`:

```bash
nano automation_practice.py
```

1. Set up `logging` to write to `practice.log`, with `INFO` level and timestamps
2. Define a function `resource_exists(path)` that checks with `os.path.exists()` whether a file already exists (idempotency check)
3. Define a function `create_resource(path, content)` that creates the file only if `resource_exists()` returns `False`, logging either "already exists" or "created" accordingly
4. Wrap a network call (reuse the `jsonplaceholder` API from earlier sections) in retry logic with exponential backoff, logging each attempt
5. Use the `if __name__ == "__main__":` guard

Run the script twice in a row and confirm via `cat practice.log` that the second run correctly detects the file already exists rather than recreating it.

**Optional (if comfortable):** Set up a real cron job using `crontab -e` that runs this script every 5 minutes, then check `practice.log` a few minutes later to confirm it ran unattended.

---

### DevOps Connection

This section _is_ the DevOps connection — idempotency, structured logging, retry-with-backoff, and scheduling are the exact patterns underlying Ansible playbooks, Terraform applies, Kubernetes reconciliation loops, and CI/CD pipeline steps. Every tool in Phase 2 is, at its core, a more sophisticated implementation of the same principles just built here from scratch in Python and Bash.

---

**Pillar 4 complete.** All 9 sections finished:

1. Python Fundamentals ✅
2. Python Functions, Modules & Error Handling ✅
3. File I/O in Python ✅
4. Bash Scripting Fundamentals ✅
5. Bash Scripting — Advanced ✅
6. REST APIs — Concepts ✅
7. Working with APIs in Python (requests) ✅
8. JSON Parsing & Data Manipulation ✅
9. Automation Patterns ✅

**Next:** Publish workflow — commit all markdown to `Great_Cheatsheets`, build `html/scripting.html` matching the existing site style, update `index.html`, commit to `DevOps-Journey`, verify live. Per the website build rule, `style.css` and `js/global.js` need to be uploaded before HTML generation begins.
