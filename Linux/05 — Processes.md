# 05 — Processes

## Checklist

- ✅ What a process is — PID, PPID
- ✅ Viewing processes — `ps`, `top`, `htop`, `pstree`
- ✅ Foreground vs background — `&`, `jobs`, `fg`, `bg`, `nohup`
- ✅ Killing processes — `kill`, `kill -9`, `killall`, `pgrep`, `pkill`
- ✅ Process states
- ✅ `nice` / `renice` — process priority (brief)

---

## What is a process?

Every time a command or program runs, Linux creates a **process** — a
running instance of that program. Even the terminal itself is a process.
Even `bash` is a process.

Every process has:

| Term                         | Meaning                                          |
| ---------------------------- | ------------------------------------------------ |
| **PID** (Process ID)         | A unique number assigned to that running process |
| **PPID** (Parent Process ID) | The PID of whatever process started it           |

Processes form a tree, just like the filesystem. Every process has a
parent, except the very first one started at boot.

### Example

```
bash (PID 500)
  └── ls (PID 501, PPID 500)
```

`bash` is the parent. `ls` is the child. Once `ls` finishes, it disappears —
`bash` keeps running.

### PID 1 — the root of the tree

```bash
ps -p 1
# PID TTY TIME CMD
# 1   ?   0:01 systemd
```

> PID 1 is always the first process started by the kernel — `systemd` on
> modern Linux, `init` on older systems. Every other process is a child
> (or descendant) of PID 1.

### Finding your own shell's PID

```bash
echo $$            # $$ always holds the PID of your current shell
ps -p $$            # shows details about that one specific process
```

```
    PID TTY          TIME CMD
   1209 pts/0    00:00:00 bash
```

| Column | Meaning                                                                  |
| ------ | ------------------------------------------------------------------------ |
| TTY    | Which terminal session this process belongs to (`pts` = pseudo-terminal) |
| TIME   | Actual CPU time used — not how long the process has existed              |

---

## Viewing processes — `ps`, `top`, `htop`, `pstree`

### `ps` — process status, a one-time snapshot

```bash
ps              # processes in YOUR current terminal session only
ps -e           # EVERY process on the system
ps -ef          # every process, full detail (PPID, start time, etc.)
ps aux          # BSD-style — most commonly used in practice
```

`ps aux` columns:

```
USER   PID  %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root     1   0.0  0.1  10000  2000 ?        Ss   10:00   0:01 /sbin/init
```

| Column  | Meaning                                            |
| ------- | -------------------------------------------------- |
| USER    | Who owns the process                               |
| PID     | Process ID                                         |
| %CPU    | CPU usage                                          |
| %MEM    | Memory usage                                       |
| TTY     | Terminal attached (`?` = none, runs in background) |
| STAT    | Process state                                      |
| COMMAND | What's actually running                            |

### `top` — live, continuously updating view

```bash
top
```

Refreshes every few seconds — watch CPU/memory usage change in real time.

| Key (inside `top`) | Action                        |
| ------------------ | ----------------------------- |
| `q`                | Quit                          |
| `P`                | Sort by CPU usage             |
| `M`                | Sort by memory usage          |
| `k`                | Kill a process (asks for PID) |

### `htop` — friendlier version of `top`

Not installed by default on most systems. Color-coded, scrollable, easier
to read. Same purpose as `top`, nicer interface.

```bash
sudo apt install htop -y
htop
```

### `pstree` — visual process tree

Shows the parent-child relationship of processes in a tree format.

```bash
pstree              # view the entire process tree
pstree -p           # with PIDs visible
pstree -p 1209      # show only your shell and its children
```

```
systemd─┬─dockerd─┬─containerd─┬─containerd-shim─┬─python3
        │          │            │                  └─sleep
        │          │            └─11*[{containerd}]
        │          └─6*[{dockerd}]
        ├─sshd─┬─sshd───bash───pstree
        │      └─2*[{sshd}]
        └─systemd───(sd-pam)
```

> `pstree` shows exactly who started whom — the parent-child relationship
> is immediately visible. PID 1 (`systemd`) sits at the root.

> Observed in practice: VS Code Server (`/vscode`) was the heaviest process
> in a Codespaces session — it powers the entire editor and terminal. Docker
> daemon (`dockerd`) and container-management processes ran lightly in the
> background, all owned by `root`.

---

## Foreground vs background processes

By default, a command runs in the **foreground** — it takes over the
terminal until it finishes. A **background** process runs without blocking
the terminal.

### `&` — run in the background

```bash
sleep 30 &
# [1] 1234
```

`[1]` is the job number (specific to this session). `1234` is the PID.

### `jobs` — list background/paused processes in this session

```bash
jobs
# [1]+  Running    sleep 30 &
```

### `fg` — bring a job to the foreground

```bash
fg            # most recent job
fg %1         # specific job number
```

### `Ctrl+Z` — pause the current foreground process

Doesn't kill it — freezes it in place and returns control to the terminal.

### `bg` — resume a paused job in the background

```bash
sleep 60
# Ctrl+Z
jobs
# [1]+  Stopped    sleep 60

bg
# [1]+ sleep 60 &

jobs
# [1]+  Running    sleep 60 &
```

### `nohup` — survive terminal exit

```bash
nohup python3 script.py &                      # runs in background, survives terminal logout
nohup python3 script.py > output.log 2>&1 &    # capture stdout and stderr too
```

> `nohup` (no hangup) ignores the `SIGHUP` signal sent when a terminal closes.
> Combined with `&`, it's how long-lived processes keep running even after
> you log out.

| Action                            | Key/Command       |
| --------------------------------- | ----------------- |
| Run in background                 | `command &`       |
| Pause foreground process          | `Ctrl+Z`          |
| List jobs                         | `jobs`            |
| Resume in foreground              | `fg`              |
| Resume in background              | `bg`              |
| Run in background, survive logout | `nohup command &` |

---

## Killing processes — `kill`, `kill -9`, `killall`, `pgrep`, `pkill`

### `kill` — send a signal to a process by PID

```bash
kill 1234          # SIGTERM — polite request to terminate, allows cleanup
kill -9 1234       # SIGKILL — force kill, immediate, no cleanup
kill -l            # list all available signals
```

> Always try plain `kill` first. Reach for `-9` only if the process refuses
> to die.

### `killall` — kill by process name instead of PID

```bash
killall sleep      # kill every process named "sleep"
killall -9 firefox # force kill every firefox process
```

### `pgrep` / `pkill` — find and kill by name pattern

More flexible than `killall` — can match partial names or full command lines.

```bash
pgrep -l sleep      # find all PIDs with "sleep" in the name, show names
pgrep -u codespace  # all processes owned by codespace
pkill sleep         # kill all processes named "sleep" (like killall)
pkill -f "python3 my_script.py"   # match against full command line
```

| Command            | Purpose                                         |
| ------------------ | ----------------------------------------------- |
| `pgrep name`       | Find PID(s) of processes matching name          |
| `pkill name`       | Kill processes matching name                    |
| `pkill -f pattern` | Match full command line (not just process name) |

> `pkill -f` is safer when several scripts are running — you can target
> `"python3 app.py"` without killing every Python process on the system.

### Example

```bash
sleep 120 &
ps aux | grep sleep
# codespace  2048  ...  sleep 120
# codespace  2055  ...  grep sleep     ← grep finds itself too, ignore

kill 2048

ps aux | grep sleep
# codespace  2061  ...  grep sleep     ← only grep remains, sleep is gone
```

---

## Process states

Shown in the `STAT` column of `ps aux` or `htop`.

| State    | Symbol | Meaning                                               |
| -------- | ------ | ----------------------------------------------------- |
| Running  | `R`    | Actively executing or ready to run                    |
| Sleeping | `S`    | Waiting for something (input, timer, resource)        |
| Stopped  | `T`    | Paused — e.g. via `Ctrl+Z`                            |
| Zombie   | `Z`    | Finished, but exit status not yet collected by parent |

> A zombie isn't dangerous alone — it's a leftover entry awaiting cleanup.
> Large persistent numbers of zombies signal a bug in the parent program.

---

## `nice` / `renice` — process priority (brief)

Linux decides how much CPU time to give a process based on **niceness**,
ranging from `-20` (highest priority) to `19` (lowest priority). Default
is `0`.

```bash
nice -n 10 some-command         # start a new process with lower priority
renice -n 5 -p 1234              # change niceness of an already-running process
```

> Lower niceness = more selfish = higher priority. Higher niceness = "nicer"
> to other processes = lower priority. Rarely adjusted day-to-day, but
> explains the `NI` column seen in `ps`/`top`/`htop` output.

---

## Quick reference

| What you want                      | Command                      |
| ---------------------------------- | ---------------------------- |
| Find your shell's PID              | `echo $$`                    |
| Snapshot of your processes         | `ps`                         |
| Snapshot of all processes          | `ps aux`                     |
| Live view                          | `top`                        |
| Live view (nicer)                  | `htop`                       |
| Visual process tree                | `pstree`                     |
| Visual tree with PIDs              | `pstree -p`                  |
| Run in background                  | `command &`                  |
| Pause foreground process           | `Ctrl+Z`                     |
| List background/paused jobs        | `jobs`                       |
| Resume in foreground               | `fg`                         |
| Resume in background               | `bg`                         |
| Run in background, survive logout  | `nohup command &`            |
| Politely stop a process            | `kill PID`                   |
| Force-stop a process               | `kill -9 PID`                |
| Kill by name                       | `killall name`               |
| Find process by name               | `pgrep name`                 |
| Kill by name pattern               | `pkill name`                 |
| Kill by full command line          | `pkill -f "command pattern"` |
| Adjust priority of new process     | `nice -n N command`          |
| Adjust priority of running process | `renice -n N -p PID`         |

---

## Key mental models

1. Every process has a PID and a PPID — processes form a tree, just like the filesystem. PID 1 (`systemd`) is the root.
2. `ps` is a snapshot. `top`/`htop` are live views. `pstree` shows the family tree.
3. `&` sends a process to the background immediately. `Ctrl+Z` pauses a foreground process; `bg` resumes it in the background.
4. `kill` asks nicely (SIGTERM). `kill -9` forces it (SIGKILL) — use only when necessary.
5. Process states (`R`, `S`, `T`, `Z`) describe what a process is doing right now — visible in `STAT`.
6. `nohup` + `&` keeps a process running even after the terminal closes.
7. Niceness controls CPU priority: lower number = higher priority, higher number = lower priority.
