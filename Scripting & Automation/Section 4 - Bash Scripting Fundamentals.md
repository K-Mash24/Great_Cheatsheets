# Pillar 4 — Scripting & Automation

## Section 4: Bash Scripting Fundamentals

### Section Checklist

- [x] What Bash is and why script it
- [x] The shebang line (#!/bin/bash)
- [x] Creating, making executable, and running a script
- [x] Variables and command substitution
- [x] Reading user input with read
- [x] Conditionals: if/elif/else/fi, test operators
- [x] Numeric vs string comparison, file test operators
- [x] Loops: for (list, range, glob pattern), while
- [x] Functions: positional parameters, exit status vs returning data
- [x] Hands-on exercise

---

### 4.1 What is Bash, and why script it?

Bash (**Bourne Again SHell**) is the command-line interpreter already in use in the Codespace terminal every time a command like `cd`, `ls`, or `cat` is typed. A **Bash script** is just a text file containing a sequence of those same commands, saved so it can be run repeatedly without retyping.

If Python is the language for structured logic and data handling, Bash is the language for gluing together system commands, files, and processes quickly — it's what most CI/CD pipeline steps, cron jobs, and container entrypoint scripts are written in.

---

### 4.2 The shebang line

Every Bash script starts with a **shebang** — a special first line telling the operating system which interpreter should execute the file:

```bash
#!/bin/bash
```

`#` normally starts a comment in Bash, but `#!` at the very start of a file is special-cased by the OS — it means "run this file using the program at this path." `/bin/bash` is the standard location of the Bash interpreter on virtually all Linux systems.

Without a shebang, running the script directly (`./script.sh`) may use the wrong interpreter or fail — always include it as line 1.

---

### 4.3 Creating and running your first script

```bash
nano hello.sh
```

Contents:

```bash
#!/bin/bash
echo "Hello, DevOps Journey"
```

`echo` is Bash's equivalent of Python's `print()` — it outputs text to the terminal.

**Making it executable and running it:**

```bash
chmod +x hello.sh
./hello.sh
```

Output:

```
Hello, DevOps Journey
```

`chmod +x` adds the **execute permission** to the file (covered in depth in Pillar 3 — Security, and Pillar 2 — Linux permissions). Without it, `./hello.sh` fails with `Permission denied`.

**Alternative — running without execute permission**, by explicitly invoking the interpreter:

```bash
bash hello.sh
```

This works even without `chmod +x`, since Bash is being told directly to interpret the file rather than asking the OS to execute it as a program.

---

### 4.4 Variables

```bash
#!/bin/bash
name="Keith"
echo "Hello, $name"
```

Output:

```
Hello, Keith
```

**Critical syntax rules:**

- **No spaces around `=`.** `name = "Keith"` is a syntax error in Bash — it's interpreted as trying to run a command called `name` with arguments `=` and `"Keith"`.
- Reference a variable's value with `$name` or `${name}` — the curly-brace form is safer when the variable name is adjacent to other text: `"${name}_journey"` vs the ambiguous `"$name_journey"` (which Bash would try to read as a variable called `name_journey`).

**Command substitution** — capturing the output of a command into a variable:

```bash
current_dir=$(pwd)
echo "Currently in: $current_dir"
```

`$(...)` runs the command inside and substitutes its output as a string. This is one of the most-used Bash patterns.

---

### 4.5 Reading user input

```bash
#!/bin/bash
echo "What's your name?"
read name
echo "Hello, $name"
```

Running this pauses at `read name`, waits for terminal input, then continues.

---

### 4.6 Comparison and conditionals — `if`/`then`/`else`

Bash's conditional syntax differs substantially from Python's:

```bash
#!/bin/bash
score=85

if [ $score -ge 90 ]; then
    echo "A grade"
elif [ $score -ge 80 ]; then
    echo "B grade"
else
    echo "C grade or below"
fi
```

Output: `B grade`

Breaking this down:

- `[ ]` — the **test command**, evaluates the condition inside (spaces around the brackets are required — `[$score` is a syntax error)
- `-ge` — "greater than or equal" (Bash uses letter-codes for numeric comparison, not `>=`)
- `then` — begins the block to run if true
- `fi` — closes the `if` block (`if` spelled backwards — a Bash convention also seen in `case`/`esac`)

**Numeric comparison operators:**

| Operator | Meaning               |
| -------- | --------------------- |
| `-eq`    | equal                 |
| `-ne`    | not equal             |
| `-gt`    | greater than          |
| `-ge`    | greater than or equal |
| `-lt`    | less than             |
| `-le`    | less than or equal    |

> **Critical pitfall:** `>` and `<` inside `[ ]` do **string comparison**, not numeric — and worse, `>` gets interpreted as output redirection in most contexts. Always use `-gt`/`-lt` etc. for numbers.

**String comparison:**

```bash
name="Keith"

if [ "$name" == "Keith" ]; then
    echo "Match"
fi
```

> **Pitfall:** Always quote variables inside `[ ]` (`"$name"`, not `$name`). An empty or unset variable without quotes can break the test's syntax entirely (`[ == "Keith" ]` is invalid — missing an operand).

**Checking file conditions:**

```bash
if [ -f "notes.txt" ]; then
    echo "File exists"
fi

if [ -d "saa-foundation" ]; then
    echo "Directory exists"
fi
```

`-f` tests for a regular file, `-d` for a directory — both return true/false based on existence and type.

---

### 4.7 Loops

**`for` loop over a list:**

```bash
#!/bin/bash
for tool in docker kubernetes terraform; do
    echo "Learning: $tool"
done
```

Output:

```
Learning: docker
Learning: kubernetes
Learning: terraform
```

**`for` loop over a range of numbers:**

```bash
for i in {1..5}; do
    echo "Number: $i"
done
```

Output: `Number: 1` through `Number: 5`.

**`for` loop over files matching a pattern:**

```bash
for file in *.md; do
    echo "Found: $file"
done
```

Loops over every `.md` file in the current directory — a pattern used constantly for batch-processing files.

**`while` loop:**

```bash
count=1
while [ $count -le 3 ]; do
    echo "Count is $count"
    count=$((count + 1))
done
```

Output:

```
Count is 1
Count is 2
Count is 3
```

`$((...))` is **arithmetic expansion** — the syntax for doing math in Bash, since `count + 1` alone would just be treated as text.

---

### 4.8 Functions in Bash

```bash
#!/bin/bash

greet() {
    echo "Hello, $1"
}

greet "Keith"
```

Output:

```
Hello, Keith
```

Unlike Python, Bash functions don't declare named parameters — arguments are accessed positionally via `$1`, `$2`, `$3`, etc., in the order they were passed.

**Returning a value:** Bash functions don't `return` data the way Python does — `return` in Bash only sets a numeric **exit status** (0–255, conventionally 0 = success). To get a value back, either `echo` it and capture with command substitution, or use a global variable:

```bash
add() {
    echo $(($1 + $2))
}

result=$(add 5 3)
echo "Result: $result"    # Result: 8
```

---

### Pitfalls Table

| Pitfall                                          | Why it's a problem                                                         | Fix                                                               |
| ------------------------------------------------ | -------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Spaces around `=` in variable assignment         | `name = "Keith"` is a syntax error — Bash tries to run `name` as a command | Never put spaces around `=`: `name="Keith"`                       |
| Using `>`/`<` for numeric comparison in `[ ]`    | Does string comparison, or gets read as output redirection                 | Use `-gt`, `-lt`, `-ge`, `-le`, `-eq`, `-ne` for numbers          |
| Not quoting variables inside `[ ]`               | Empty/unset variables can break the test's syntax entirely                 | Always quote: `[ "$name" == "Keith" ]`                            |
| Expecting `return` to hand back data like Python | `return` only sets a 0–255 exit status code                                | `echo` the value and capture it with `$(function_name)`           |
| Forgetting `chmod +x` before `./script.sh`       | `Permission denied` error                                                  | Run `chmod +x script.sh`, or invoke with `bash script.sh` instead |

---

### 🖥️ Hands-on Exercise

In `/workspaces/DevOps-Journey`:

```bash
nano practice.sh
chmod +x practice.sh
```

1. Declare a variable `pillar="scripting"` and echo `"Current pillar: $pillar"`
2. Use a `for` loop to print each `.md` file in `saa-foundation/04-scripting/`
3. Include an `if` statement checking whether a file called `README.md` exists in the current directory, printing a message either way
4. Define a function `add()` that takes two arguments and echoes their sum, then call it and capture the result in a variable

Run: `./practice.sh`

---

### DevOps Connection

Nearly every CI/CD pipeline step, Docker container entrypoint, and cron job on a Linux server is a Bash script under the hood — GitHub Actions workflow steps frequently run raw `bash` commands, and Dockerfiles use `RUN` and `ENTRYPOINT` instructions that execute shell scripts. Fluency here transfers directly into Phase 2.

---

**Next section:** [05-bash-scripting-advanced.md](./05-bash-scripting-advanced.md) — Bash Scripting — Advanced (arrays, argument parsing, exit codes, traps)
