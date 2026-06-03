# 01 — Filesystem Structure & Navigation

Full checklist:

- ✅ Linux filesystem layout
- ✅ Navigation commands — pwd, cd, ls
- ✅ ~ vs / vs /root distinction
- ✅ Absolute vs relative paths
- ✅ Hidden files and directories
- ✅ The tree command

---

## What is a filesystem?

A filesystem is the system that organises data on disk into a structured hierarchy.
On Linux, this is a single tree with one root — everything lives under it.
Unlike Windows, which gives each disk its own tree (`C:\`, `D:\`), Linux has one tree for everything.

---

## The filesystem tree

The top of the tree is written as `/` (called "root").
All files, directories, and devices live somewhere below it.

### Standard top-level directories (FHS — Filesystem Hierarchy Standard)

| Directory | Purpose |
|-----------|---------|
| `/`       | Root — top of the entire filesystem tree |
| `/home`   | Home directories for regular users (e.g. `/home/codespace`) |
| `/root`   | Home directory for the root (admin) user — separate from `/home` |
| `/etc`    | System-wide configuration files (human-readable text) |
| `/var`    | Variable data — grows while system runs (logs, caches) |
| `/usr`    | Installed programs and their supporting files |
| `/tmp`    | Temporary files — cleared on every reboot |
| `/bin`    | Essential command binaries (`ls`, `cd`, `pwd`, etc.) |
| `/dev`    | Devices represented as files (disks, terminals, etc.) |

---

## Special directory symbols

| Symbol | Name | What it is |
|--------|------|------------|
| `/`    | Root | Top of the entire filesystem tree |
| `~`    | Tilde | Shortcut for your home directory (`/home/codespace`) |
| `.`    | Dot | Current directory |
| `..`   | Dot-dot | Parent directory — one level up |
| `/root` | Root's home | The admin user's home — not the filesystem root |

> **Common confusion:** `~` and `/root` are completely different things. `~` expands to your own home (`/home/codespace`). `/root` is a specific directory that belongs to the admin user.

---

## Navigation commands

### `pwd` — Print Working Directory
Shows your current location in the filesystem.
```bash
pwd
# /home/codespace
```

### `ls` — List
Lists the contents of a directory.
```bash
ls              # current directory
ls /etc         # specific directory
ls -l           # long format — permissions, owner, size, date
ls -a           # all files including hidden
ls -la          # long format + hidden (most common combo)
ls -lh          # long format with human-readable sizes
```

#### Reading `ls -l` output
```
drwxr-xr-x 2 alice users 4096 Jun 3 10:30 Documents
│         │ │     │     │    │             │
│         │ │     │     │    └── date/time  └── filename
│         │ │     │     └── size in bytes
│         │ │     └── group owner
│         │ └── user owner
│         └── link count
└── file type + permissions
    │└──────────────────── permissions (9 chars: user/group/other × rwx)
    └── file type: d=directory  -=regular file  l=symlink
```

### `cd` — Change Directory
Moves you into a different directory.
```bash
cd /etc           # go to /etc (absolute path)
cd ..             # go up one level
cd ~              # go to your home directory from anywhere
cd -              # go back to the previous directory
cd .              # stay in current directory (does nothing useful alone)
```

---

## Absolute vs relative paths

### Absolute path
- Full address starting from the root of the filesystem
- Always starts with `/`
- Works the same no matter where you currently are

```bash
cd /home/codespace/projects
cd /etc
```

### Relative path
- Address starting from your current working directory
- Never starts with `/`
- Uses `.` and `..` to navigate

```bash
cd projects        # enter projects/ from current location
cd ..              # go up one level
cd ../..           # go up two levels
```

### Path decision tree

```
Does the path start with / ?
         │
    ┌────┴────┐
   YES        NO
    │          │
ABSOLUTE    RELATIVE
(from /)    (from here)
    │          │
Works       Does the target exist
anywhere    inside your current dir?
                 │
           ┌────┴────┐
          YES         NO
           │           │
        Use it ✓    Error — use absolute path
                    or cd to the right place first
```

> **The key rule:** A relative path only works if the target exists inside your current directory.

---

## Hidden files and directories

Any file or directory whose name starts with `.` is hidden.
Hidden = not shown by default in `ls`. Not protected or encrypted — just kept out of the way.

```bash
ls -a ~     # reveal hidden files in home
ls -la ~    # hidden files + long format
```

### Common hidden files in home directory

| File/Dir | Purpose |
|----------|---------|
| `.bashrc`    | Bash shell config — runs every time a terminal opens |
| `.profile`   | Login shell config |
| `.gitconfig` | Git settings — name, email, preferences |
| `.ssh/`      | SSH keys and known hosts |
| `.`          | The current directory itself |
| `..`         | The parent directory |

---

## The `tree` command

Displays an entire directory structure visually — not just one level at a time.

```bash
tree ~              # full tree of home directory
tree -L 1 /         # 1 level deep from root
tree -L 2 /home     # 2 levels deep from /home
tree -a ~           # include hidden files
tree -d ~           # directories only, no files
```

> `-L` (Level) is the most useful flag — always use it on large directories to avoid thousands of lines of output.

---

## Common errors & fixes

| Error | What it means | Fix |
|-------|---------------|-----|
| `No such file or directory` | Path doesn't exist or is wrong | Check spelling; use `ls` to see what's actually there |
| `cd: x: Not a directory` | `x` is a file, not a directory | Can't `cd` into a file — use `cat` or `less` to read it |
| `Permission denied` | You don't have access rights | Check `ls -l`; you may need `sudo` |

---

## Quick reference

| What you want | Command |
|---------------|---------|
| Where am I? | `pwd` |
| What's in this directory? | `ls` |
| Everything including hidden | `ls -a` |
| Details + hidden | `ls -la` |
| Human-readable sizes | `ls -lh` |
| Go home | `cd` or `cd ~` |
| Go up one level | `cd ..` |
| Go back to previous location | `cd -` |
| See folder tree (2 levels) | `tree -L 2` |
| Tree including hidden files | `tree -a` |

---

## Key mental models

1. The filesystem is one tree. `/` is the trunk. Everything else is a branch or leaf.
2. Absolute paths start with `/`. Relative paths start from where you are.
3. A dot prefix = hidden. Use `ls -a` to see everything.
4. `~` always means your home. `/root` is a specific folder belonging to the admin user.