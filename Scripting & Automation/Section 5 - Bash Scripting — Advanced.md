# Pillar 4 — Scripting & Automation

## Section 5: Bash Scripting — Advanced

### Section Checklist

- [x] Arrays: declaring, accessing, looping, counting, appending
- [x] Positional parameters and script arguments ($0, $1, $@, $#, $?)
- [x] shift for processing unknown numbers of arguments
- [x] Exit codes and their role in automation
- [x] set -e, set -u, set -o pipefail
- [x] trap for guaranteed cleanup on exit/signals
- [x] getopts for flag-based argument parsing
- [x] Hands-on exercise

---

### 5.1 Arrays

Bash supports arrays — ordered lists of values, similar to Python lists but with notably different syntax.

**Declaring and populating:**

```bash
tools=("docker" "kubernetes" "terraform")
```

No commas between elements — just spaces, inside parentheses.

**Accessing elements:**

```bash
echo "${tools[0]}"     # docker
echo "${tools[1]}"     # kubernetes
```

> **Critical:** Array access always requires curly braces: `${tools[0]}`, not `$tools[0]`. Without the braces, Bash reads `$tools` (which evaluates to the _first_ element only) followed by the literal text `[0]`.

**All elements, and count:**

```bash
echo "${tools[@]}"      # docker kubernetes terraform
echo "${#tools[@]}"      # 3 — the number of elements
```

`@` inside `[ ]` means "all elements." `#` before the array name means "count of."

**Looping over an array:**

```bash
for tool in "${tools[@]}"; do
    echo "Learning: $tool"
done
```

Output:

```
Learning: docker
Learning: kubernetes
Learning: terraform
```

> **Pitfall:** Always quote `"${tools[@]}"` in loops. Without quotes, an element containing spaces (e.g., `"docker compose"`) would get split into two separate loop iterations instead of staying intact.

**Adding an element:**

```bash
tools+=("ansible")
echo "${tools[@]}"    # docker kubernetes terraform ansible
```

---

### 5.2 Positional parameters and script arguments

Scripts can accept arguments from the command line, accessed the same way function arguments were in Section 4:

```bash
#!/bin/bash
echo "Script name: $0"
echo "First arg: $1"
echo "Second arg: $2"
echo "All args: $@"
echo "Number of args: $#"
```

Running:

```bash
./script.sh hello world
```

Output:

```
Script name: ./script.sh
First arg: hello
Second arg: world
All args: hello world
Number of args: 2
```

| Variable        | Meaning                                                |
| --------------- | ------------------------------------------------------ |
| `$0`            | The script's own name/path                             |
| `$1`, `$2`, ... | Individual positional arguments                        |
| `$@`            | All arguments as separate words                        |
| `$#`            | Total count of arguments                               |
| `$?`            | Exit status of the _last_ command run (covered in 5.4) |

---

### 5.3 `shift` — processing arguments one at a time

`shift` removes `$1` and shifts every remaining argument down by one position — `$2` becomes the new `$1`, and so on. This is the standard pattern for looping through an unknown number of arguments:

```bash
#!/bin/bash
while [ $# -gt 0 ]; do
    echo "Processing: $1"
    shift
done
```

Running `./script.sh a b c` outputs:

```
Processing: a
Processing: b
Processing: c
```

Each iteration, `$1` is the "current" argument, and `shift` advances to the next one — the loop ends when `$#` (the remaining count) hits 0.

---

### 5.4 Exit codes

Every command and script, when it finishes, produces a numeric **exit status** between 0 and 255. By convention:

- `0` = success
- Any nonzero value (typically `1`) = some kind of failure

```bash
ls /nonexistent
echo $?     # prints the exit code of the previous command — 2, meaning "No such file or directory"
```

**Setting your own script's exit code with `exit`:**

```bash
#!/bin/bash
if [ ! -f "config.txt" ]; then
    echo "Error: config.txt not found"
    exit 1
fi
echo "Proceeding..."
```

`exit 1` immediately stops the script and sets its exit status to `1` — anything checking this script's success (another script, a CI/CD pipeline step) sees the failure.

**Why this matters enormously in automation:** CI/CD pipelines, `cron` jobs, and orchestration tools all decide whether to proceed, retry, or alert _based on exit codes_ — not on whether output "looked okay." A script that encounters an error but exits with `0` anyway will silently report success to everything downstream.

**Checking exit codes to control flow:**

```bash
grep "error" logfile.txt
if [ $? -eq 0 ]; then
    echo "Error found in log"
else
    echo "No errors found"
fi
```

`grep` exits `0` if it found a match, `1` if it didn't — a common pattern for using search commands as conditionals.

**Shorthand using `&&` and `||`:**

```bash
mkdir new_folder && echo "Created successfully"
cd missing_folder || echo "Failed to enter directory"
```

`&&` runs the next command only if the previous one succeeded (exit `0`); `||` runs the next command only if the previous one failed (nonzero exit).

---

### 5.5 `set -e`, `set -u`, `set -o pipefail` — safer scripts

By default, Bash scripts **keep running even after a command fails** — a dangerous default for automation, where a failed step should usually stop everything rather than continue on possibly-corrupted state.

```bash
#!/bin/bash
set -e   # exit immediately if any command exits non-zero
set -u   # treat unset variables as an error, not empty string
set -o pipefail   # a pipeline fails if ANY command in it fails, not just the last one
```

Placed at the top of a script, these three lines are an extremely common defensive pattern (sometimes combined as `set -euo pipefail`):

- **`set -e`** — without it, a script that fails on line 3 will still barrel ahead to line 4, 5, etc., often causing confusing downstream failures instead of stopping cleanly at the actual point of failure.
- **`set -u`** — without it, a typo like `$nmae` instead of `$name` silently evaluates to an empty string rather than raising an error, which can cause a script to (for example) `rm -rf $nmae/` and delete the entire current directory instead of a subfolder.
- **`set -o pipefail`** — without it, `false | true` reports success (exit `0`) because only the _last_ command in the pipe (`true`) is checked by default.

> **Callout:** This trio is close to a default best practice for any Bash script meant to run unattended (cron jobs, CI/CD steps, deployment scripts). Interactive one-off scripts can skip it, but anything automated should almost always include it.

---

### 5.6 `trap` — running cleanup code on exit or signal

`trap` lets a script run a specific command when it receives a signal (like being interrupted) or when it exits — regardless of whether it exited successfully or due to an error.

```bash
#!/bin/bash

cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/tempfile
}

trap cleanup EXIT

echo "Doing work..."
touch /tmp/tempfile
sleep 2
echo "Work done"
```

`trap cleanup EXIT` registers the `cleanup` function to run automatically whenever the script exits — whether it finished normally, hit `exit 1`, or was interrupted with `Ctrl+C`.

**Common signals to trap:**

| Signal    | Trigger                                                     |
| --------- | ----------------------------------------------------------- |
| `EXIT`    | Script exits, for any reason (success, error, or interrupt) |
| `SIGINT`  | User presses `Ctrl+C`                                       |
| `SIGTERM` | Process receives a termination request (e.g., from `kill`)  |

This is the Bash equivalent of Python's `finally` block from Section 2 — guaranteed cleanup regardless of how the script ends.

---

### 5.7 `getopts` — proper flag-based argument parsing

Positional arguments (`$1`, `$2`) work for simple scripts, but real-world CLI tools use named flags (`-f filename`, `-v` for verbose). `getopts` is Bash's built-in tool for parsing these.

```bash
#!/bin/bash

while getopts "n:v" opt; do
    case $opt in
        n) name="$OPTARG" ;;
        v) verbose=true ;;
        \?) echo "Invalid option"; exit 1 ;;
    esac
done

echo "Name: $name"
echo "Verbose: $verbose"
```

Running:

```bash
./script.sh -n Keith -v
```

Output:

```
Name: Keith
Verbose: true
```

Breaking down the flag string `"n:v"`:

- `n:` — the colon means `-n` **requires a value** (accessed via `$OPTARG`)
- `v` — no colon means `-v` is a standalone flag (a boolean switch, no value needed)

`case`/`esac` works like a more readable alternative to a long `if`/`elif` chain when checking one variable against multiple possible values — `esac` is `case` spelled backwards, following the same convention as `fi` and `done`.

---

### Pitfalls Table

| Pitfall                                           | Why it's a problem                                                           | Fix                                                    |
| ------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------ |
| Accessing array elements without `${}`            | `$tools[0]` reads as the first element plus literal text `[0]`               | Always use `${tools[0]}`                               |
| Looping over an array without quotes              | Elements containing spaces get split into multiple iterations                | Use `"${tools[@]}"` with quotes                        |
| Assuming a script that "ran" means it succeeded   | A script can produce output and still exit non-zero (or vice versa)          | Always check `$?` or use `set -e`                      |
| Skipping `set -euo pipefail` in automated scripts | Unset variables, mid-pipeline failures, and later-line errors go unnoticed   | Add the trio at the top of every unattended script     |
| Forgetting `trap` for cleanup                     | Temp files/processes can be left behind if a script errors or is interrupted | Register a `cleanup` function with `trap cleanup EXIT` |

---

### 🖥️ Hands-on Exercise

In `/workspaces/DevOps-Journey`:

```bash
nano advanced_practice.sh
chmod +x advanced_practice.sh
```

1. Start with `set -euo pipefail`
2. Declare an array of pillar names and loop over it with `"${array[@]}"`
3. Use `getopts` to accept a `-p` flag (a pillar number, requires a value) and a `-v` flag (verbose, no value)
4. Register a `trap` that echoes `"Script finished"` on `EXIT`
5. Check `$#` and exit with code `1` and an error message if no flags were provided

Run it several ways: `./advanced_practice.sh -p 4 -v`, then with no arguments to confirm the exit-code error path works, then check `echo $?` after each run.

---

### DevOps Connection

Nearly every production-grade shell script — deployment scripts, entrypoint scripts in Docker images, CI/CD pipeline steps — relies on this section's tools specifically: `set -euo pipefail` to fail fast and loudly, `trap` for guaranteed cleanup of temporary resources, and `getopts` for accepting configuration flags rather than hardcoding values. Scripts without these safeguards are a common source of silent failures in real infrastructure.

---

**Next section:** [06-rest-api-concepts.md](./06-rest-api-concepts.md) — REST APIs — Concepts
