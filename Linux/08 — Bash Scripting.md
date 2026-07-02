# 08 — Bash Scripting

## Checklist

- ✅ What a shell script is — shebang, execution
- ✅ Script safety — `set -e`, `set -u`
- ✅ Variables and command substitution
- ✅ Parameter expansion — default values
- ✅ User input — `read`
- ✅ Conditionals — `if`, `elif`, `else`
- ✅ Case statements — multi-branch
- ✅ Loops — `for`, `while`, `break`, `continue`
- ✅ Functions
- ✅ Arguments — `$0`, `$1`, `$@`, `$#`
- ✅ Exit codes — `$?`
- ✅ Arrays
- ✅ Command chaining — `&&`, `||`
- ✅ Here documents — multi-line text
- ✅ `trap` — cleanup on exit
- ✅ Common mistakes and debugging
- ✅ Practical script patterns

---

## What is a shell script?

A shell script is a plain text file containing a sequence of commands that bash executes in order — exactly as if you typed them one by one into the terminal. The power is automation: one file, run once, does the work of dozens of commands.

### The shebang line

Every bash script starts with this on line 1:

```bash
#!/bin/bash
```

The **shebang** (hashbang) tells the OS which interpreter to use. Without it, the OS doesn't know whether to hand the file to bash, Python, or something else.

### Creating and running a script

```bash
touch hello.sh
```

Inside the file:

```bash
#!/bin/bash
echo "Hello from a script"
```

Running it:

```bash
chmod +x hello.sh    # give execute permission
./hello.sh           # run it
```

> `./` means "in the current directory." Linux doesn't look in the current directory for executables by default — only in directories listed in `$PATH`. The `./` prefix is required.

---

## Script safety — `set -e`, `set -u`

```bash
#!/bin/bash
set -e          # Exit immediately if any command fails
set -u          # Exit if any undefined variable is used
set -x          # Print each command before executing (debug mode)

# Or combine them
set -eux
```

These flags make scripts safer and more predictable. `set -e` prevents scripts from continuing after errors. `set -u` catches typos in variable names.

---

## Variables

```bash
name="Keith"
echo "Hello, $name"
echo "Hello, ${name}s"    # braces needed when variable is next to other text
```

Rules:

- No spaces around `=` — `name = "Keith"` fails
- Reference with `$` — `$name` or `${name}`

### Common built-in variables

| Variable | Meaning                           |
| -------- | --------------------------------- |
| `$HOME`  | Your home directory               |
| `$USER`  | Current username                  |
| `$PWD`   | Current working directory         |
| `$PATH`  | Directories searched for commands |
| `$$`     | PID of the current shell          |

### Parameter expansion — default values

```bash
# Use default value if variable is unset
echo ${name:-"default"}    # prints "default" if name is unset

# Set variable to default if unset
echo ${name:="default"}    # sets name to "default" if unset
```

Useful for handling optional arguments with sensible defaults.

### Command substitution

Store the output of a command in a variable:

```bash
today=$(date)
echo "Today is $today"

files=$(ls | wc -l)
echo "There are $files files here"
```

`$(command)` runs the command and captures its output as a string.

---

## Arrays

```bash
# Define array
fruits=("apple" "banana" "mango")

# Access elements
echo ${fruits[0]}        # apple
echo ${fruits[@]}        # all elements
echo ${#fruits[@]}       # array length

# Loop through array
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done
```

Arrays are essential for handling lists of items in scripts.

---

## User input — `read`

```bash
echo "What is your name?"
read name
echo "Hello, $name"
```

One-liner with a prompt:

```bash
read -p "Enter your name: " name
```

| Flag | Meaning                                       |
| ---- | --------------------------------------------- |
| `-p` | Show a prompt string before waiting           |
| `-s` | Silent mode — input not shown (for passwords) |

---

## Conditionals — `if`, `elif`, `else`

```bash
#!/bin/bash
read -p "Enter a number: " num

if [ $num -gt 10 ]; then
    echo "Greater than 10"
elif [ $num -eq 10 ]; then
    echo "Exactly 10"
else
    echo "Less than 10"
fi
```

> Spaces inside `[ ]` are required — `[ $num -gt 10 ]` works, `[$num -gt 10]` does not.

### Numeric comparison operators

| Operator | Meaning               |
| -------- | --------------------- |
| `-eq`    | equal                 |
| `-ne`    | not equal             |
| `-gt`    | greater than          |
| `-lt`    | less than             |
| `-ge`    | greater than or equal |
| `-le`    | less than or equal    |

### String comparison operators

| Operator | Meaning             |
| -------- | ------------------- |
| `=`      | equal               |
| `!=`     | not equal           |
| `-z`     | string is empty     |
| `-n`     | string is not empty |

### File test operators

| Operator  | Meaning                           |
| --------- | --------------------------------- |
| `-f file` | file exists and is a regular file |
| `-d dir`  | directory exists                  |
| `-e path` | path exists (file or directory)   |
| `-r file` | file is readable                  |
| `-x file` | file is executable                |

```bash
if [ -f /etc/hosts ]; then
    echo "/etc/hosts exists"
fi
```

---

## Case statements — multi-branch conditional

```bash
#!/bin/bash
read -p "Enter a fruit: " fruit

case $fruit in
    apple|Apple)
        echo "🍎 Apple"
        ;;
    banana|Banana)
        echo "🍌 Banana"
        ;;
    orange|Orange)
        echo "🍊 Orange"
        ;;
    *)
        echo "Unknown fruit"
        ;;
esac
```

`case` is cleaner than multiple `if/elif` statements when checking many possible values.

---

## Loops — `for`, `while`

### `for` loop

```bash
# Loop over a list
for fruit in apple banana mango; do
    echo "Fruit: $fruit"
done

# Loop over files
for file in *.txt; do
    echo "Found: $file"
done

# Loop with a range
for i in {1..5}; do
    echo "Number $i"
done

# C-style loop
for ((i=0; i<5; i++)); do
    echo "i is $i"
done
```

### `while` loop

```bash
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```

> `$((expression))` is arithmetic expansion — how you do math in bash.

### Loop control

```bash
break       # exit the loop entirely
continue    # skip to the next iteration
```

---

## Functions

```bash
#!/bin/bash

greet() {
    echo "Hello, $1"
}

greet "Keith"
greet "World"
```

`$1` inside a function refers to the first argument passed to that function — not to the script's own arguments.

### Returning data from a function

Bash functions don't return values like other languages — they return an exit code (0–255). To pass data back, use `echo` and capture with `$()`:

```bash
add() {
    echo $(( $1 + $2 ))
}

result=$(add 3 5)
echo "Result: $result"    # Result: 8
```

---

## Arguments — `$0`, `$1`, `$@`, `$#`

When called with arguments, bash makes them available automatically:

```bash
./script.sh hello world
```

| Variable | Value                           |
| -------- | ------------------------------- |
| `$0`     | Script name (`./script.sh`)     |
| `$1`     | First argument (`hello`)        |
| `$2`     | Second argument (`world`)       |
| `$@`     | All arguments as separate words |
| `$#`     | Number of arguments             |

```bash
#!/bin/bash
echo "Script name: $0"
echo "First arg:   $1"
echo "All args:    $@"
echo "Arg count:   $#"
```

---

## Exit codes — `$?`

Every command exits with a code. `0` = success. Anything non-zero = failure.

```bash
ls /etc/hosts
echo $?        # 0 — success

ls /nonexistent
echo $?        # 2 — failure
```

Set your own exit code:

```bash
exit 0     # success
exit 1     # failure (convention: 1 = general error)
```

Use in conditionals:

```bash
if ls /etc/hosts > /dev/null 2>&1; then
    echo "File exists"
else
    echo "File not found"
fi
```

> `> /dev/null 2>&1` silences all output — redirects both stdout and stderr to `/dev/null`, Linux's bin for discarded output.

---

## Command chaining — `&&`, `||`

```bash
# Run second command only if first succeeds
mkdir newdir && cd newdir

# Run second command only if first fails
command || echo "Command failed"

# Combine
command1 && command2 || echo "Something went wrong"
```

Command chaining is used constantly in scripts and on the command line for conditional execution.

---

## Here documents — multi-line text

```bash
# Print multi-line text
cat << EOF
This is a
multi-line
message
EOF

# Use with variables
name="Keith"
cat << EOF
Hello $name,
Welcome to the script.
EOF
```

Here documents are perfect for printing help messages, generating configuration files, or creating multi-line output.

---

## `trap` — cleanup on exit

```bash
#!/bin/bash
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/tempfile.$$
}

trap cleanup EXIT

# Script runs here...
echo "Script running..."
touch /tmp/tempfile.$$
```

`trap` ensures cleanup happens even if the script is interrupted or exits unexpectedly.

---

## `select` — menu selection

```bash
#!/bin/bash
echo "Select an option:"
select choice in "Date" "Uptime" "Users" "Quit"; do
    case $choice in
        "Date") date ;;
        "Uptime") uptime ;;
        "Users") who ;;
        "Quit") break ;;
        *) echo "Invalid option" ;;
    esac
done
```

`select` creates interactive menus with numbered options automatically.

---

## Common mistakes and debugging

```bash
# Common mistake: missing spaces in [ ]
if [ "$name" = "Keith" ]; then   # Correct
if ["$name" = "Keith"]; then     # Wrong — missing spaces

# Debug with -x
bash -x script.sh                # Run with debug mode

# Check syntax without executing
bash -n script.sh                # Syntax check only

# Quote variables to prevent word splitting
file="my file.txt"
cat "$file"                      # Correct
cat $file                        # Wrong — tries to open "my" and "file.txt"
```

Debugging is an essential skill for script writers.

---

## Practical script patterns

### Validate input before acting

```bash
#!/bin/bash
file="$1"

if [ -z "$file" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

if [ -f "$file" ]; then
    echo "Processing $file"
else
    echo "Error: $file not found"
    exit 1
fi
```

### Loop through command output

```bash
#!/bin/bash
for user in $(cat /etc/passwd | cut -d: -f1); do
    echo "User: $user"
done
```

### Simple backup script

```bash
#!/bin/bash
source="$1"
backup="${source}.bak"

cp "$source" "$backup"
echo "Backed up $source to $backup"
```

### Interactive menu script

```bash
#!/bin/bash
echo "Select an option:"
select choice in "Show Date" "Show Uptime" "Show Users" "Quit"; do
    case $choice in
        "Show Date") date ;;
        "Show Uptime") uptime ;;
        "Show Users") who ;;
        "Quit") break ;;
        *) echo "Invalid option" ;;
    esac
done
```

---

## Quick reference

| What you want               | Syntax                                            |
| --------------------------- | ------------------------------------------------- |
| Script header               | `#!/bin/bash`                                     |
| Script safety               | `set -eux`                                        |
| Set a variable              | `name="value"`                                    |
| Use a variable              | `$name` or `${name}`                              |
| Default value               | `${name:-"default"}`                              |
| Command substitution        | `result=$(command)`                               |
| Arithmetic                  | `$((a + b))`                                      |
| Read user input             | `read -p "prompt: " var`                          |
| If / elif / else            | `if [ condition ]; then ... elif ... else ... fi` |
| Case statement              | `case $var in pattern) ... ;; esac`               |
| For loop (list)             | `for item in a b c; do ... done`                  |
| For loop (range)            | `for i in {1..5}; do ... done`                    |
| While loop                  | `while [ condition ]; do ... done`                |
| Define function             | `funcname() { ... }`                              |
| Call function               | `funcname arg1 arg2`                              |
| Script arguments            | `$0` `$1` `$2` `$@` `$#`                          |
| Last exit code              | `$?`                                              |
| Exit script                 | `exit 0` or `exit 1`                              |
| Silence output              | `command > /dev/null 2>&1`                        |
| Command chaining (and)      | `cmd1 && cmd2`                                    |
| Command chaining (or)       | `cmd1 || cmd2`                                    |
| File exists?                | `[ -f file ]`                                     |
| Directory exists?           | `[ -d dir ]`                                      |
| String empty?               | `[ -z "$var" ]`                                   |
| Define array                | `arr=("a" "b" "c")`                               |
| Use array elements          | `${arr[@]}`                                       |
| Array length                | `${#arr[@]}`                                      |
| Multi-line text             | `cat << EOF ... EOF`                              |
| Cleanup on exit             | `trap function EXIT`                              |
| Debug mode                  | `bash -x script.sh`                               |
| Syntax check                | `bash -n script.sh`                               |

---

## Key mental models

1. A script is just commands in a file. The shebang tells the OS which interpreter to run them with.

2. No spaces around `=` when setting variables. Always use `$` to read them. Quote variables to prevent word splitting.

3. `$(command)` captures command output into a variable — this is how scripts compose operations.

4. `[ ]` test expressions require spaces inside the brackets. Missing a space = syntax error.

5. Bash functions return exit codes, not values. Use `echo` + `$()` to pass data back from a function.

6. `$1`, `$2`, `$@`, `$#` are the gateway to making reusable scripts — always validate input first.

7. `$?` is how you know if the last command succeeded. `0` = success, non-zero = failure.

8. `exit 1` immediately stops the script and signals failure to whatever called it.

9. `set -e` and `set -u` make scripts safer by stopping on errors and catching undefined variables.

10. `&&` and `||` are essential for conditional command execution — `&&` runs on success, `||` runs on failure.

11. `trap` ensures cleanup happens even when scripts exit unexpectedly.

12. Arrays and case statements make scripts more powerful and maintainable for complex logic.
```

---

