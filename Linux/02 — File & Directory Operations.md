# 02 — File & Directory Operations

## Checklist
- ✅ Creating files — `touch`, `>`, `>>`
- ✅ Creating directories — `mkdir`, `mkdir -p`
- ✅ Copying — `cp`, `cp -i`, `cp -r`
- ✅ Moving & renaming — `mv`, `mv -i`
- ✅ Deleting — `rm`, `rm -rf`, `rmdir`
- ✅ Wildcards — `*`, `?`
- ✅ Viewing file contents — `cat`, `less`, `head`, `tail`

---

## Creating files

### `touch`
Creates an empty file instantly. If the file already exists, `touch` updates its timestamp (last modified time) without changing its contents.
```bash
touch notes.txt
touch file1.txt file2.txt file3.txt    # create multiple at once
touch existing.txt                     # updates timestamp, doesn't empty the file
```

### Redirection with `>`
Creates a file and writes content into it. Overwrites the **entire file** if it already exists.
```bash
echo "hello world" > notes.txt
```

### Redirection with `>>`
Appends to the file. Existing content is preserved.
```bash
echo "first line" > notes.txt
echo "second line" >> notes.txt
```

| Operator | Behaviour |
|----------|-----------|
| `>`      | Wipes the file, writes fresh |
| `>>`     | Keeps existing content, adds to the bottom |

> **Warning:** `>` is destructive — it wipes the entire file, not just one line.

---

## Creating directories

### `mkdir` — make directory
```bash
mkdir projects                         # single directory
mkdir docs notes images                # multiple at once
mkdir projects/linux                   # inside an existing directory
mkdir -p projects/linux/section-2      # create full nested path in one shot
```

> `-p` creates all missing parent directories along the way. Without it,
> `mkdir a/b/c` fails if `a/b` doesn't already exist.

---

## Copying — `cp`

```bash
cp source destination
```

```bash
cp notes.txt backup/                   # copy into a directory
cp notes.txt backup/notes-copy.txt     # copy and rename at the same time
cp -r projects projects-backup         # copy a directory and all its contents
cp -i notes.txt backup/                # interactive — asks before overwriting
```

| Flag | Meaning |
|------|---------|
| `-r` | Recursive — required for directories |
| `-i` | Interactive — prompts before overwriting |

> `-i` is a safety net. Use it when unsure whether the destination already has a file with the same name.

---

## Moving & renaming — `mv`

```bash
mv source destination
```

```bash
mv notes.txt archive/                  # move into a directory
mv old-name.txt new-name.txt           # rename in the same location
mv notes.txt archive/renamed.txt       # move and rename in one step
mv projects archive/                   # move a directory (no -r needed)
mv -i notes.txt archive/               # interactive — asks before overwriting
```

| Flag | Meaning |
|------|---------|
| `-i` | Interactive — prompts before overwriting |

> Unlike `cp`, `mv` leaves no copy behind — the original is gone.
> Unlike `cp`, `mv` doesn't need `-r` for directories.

---

## Deleting — `rm` and `rmdir`

> **Warning:** Linux has no recycle bin. Deleted = gone permanently.

### `rm` — remove files
```bash
rm notes.txt                           # delete a file
rm file1.txt file2.txt                 # delete multiple files
rm -i notes.txt                        # interactive — asks for confirmation
rm -r projects/                        # delete a directory and all its contents
rm -rf projects/                       # force delete — no prompts, no mercy
```

### `rmdir` — remove empty directories only
```bash
rmdir empty-dir/                       # only works if the directory is empty
```

| Command  | Behaviour |
|----------|-----------|
| `rm`     | Deletes files |
| `rm -r`  | Deletes a directory and everything inside it |
| `rm -rf` | Force deletes — no confirmation, no recovery |
| `rmdir`  | Deletes a directory only if it is empty — safe option |

> Safety tip: `rm -rf` is irreversible. Some users alias `rm` to `rm -i` to prevent accidental deletion.

---

## Wildcards — `*` and `?`

Wildcards let you match multiple files in a single command without naming each one.

### `*` — matches any number of characters (including zero)
```bash
rm *.log                               # delete all .log files
cp *.txt backup/                       # copy all .txt files into backup/
ls chapter-*.md                        # list all markdown files starting with "chapter-"
```

### `?` — matches exactly one character
```bash
ls file-?.txt                          # matches file-1.txt, file-a.txt — NOT file-10.txt
rm photo-??.jpg                        # matches photo-01.jpg, photo-AB.jpg (exactly 2 chars)
```

| Wildcard | Matches | Example |
|----------|---------|---------|
| `*` | Anything or nothing | `*.txt` — all text files |
| `?` | Exactly one character | `file-?.txt` — file-1.txt, file-a.txt |

> **Caution with `rm *`:** Always run `ls *` first to see what you're about to delete.

---

## Viewing file contents

### `cat` — print entire file to screen
```bash
cat notes.txt
```
Best for short files. Dumps everything at once — long files will scroll past you.

### `less` — scrollable viewer
```bash
less notes.txt
```
Opens the file in a pager so you can scroll through it. More feature-rich than the older `more` command.

| Key | Action |
|-----|--------|
| `Space` or `f` | Page down |
| `b` | Page up |
| `q` | Quit |
| `/word` | Search for "word" |
| `n` | Next search result |
| `N` | Previous search result |

Best for long files like logs.

### `head` — first N lines
```bash
head notes.txt                         # first 10 lines (default)
head -n 5 notes.txt                    # first 5 lines
head -n 3 file1.txt file2.txt          # shows first 3 lines of each file with a header
```

### `tail` — last N lines
```bash
tail notes.txt                         # last 10 lines (default)
tail -n 5 notes.txt                    # last 5 lines
tail -f notes.txt                      # follow — prints new lines as the file grows
tail -f -n 20 app.log                  # last 20 lines, then follow
```

> `tail -f` is essential for watching log files in real time.

---

## `file` — determine file type

Linux doesn't rely on extensions to know what a file is. Use `file` to identify what something actually contains:
```bash
file unknown.bin                       # tells you if it's ASCII text, binary, image, etc.
file script.sh                         # might show "Bourne-Again shell script"
```

---

## Quick reference

| What you want | Command |
|---------------|---------|
| Create empty file | `touch file.txt` |
| Write to file (overwrite) | `echo "text" > file.txt` |
| Append to file | `echo "text" >> file.txt` |
| Create directory | `mkdir dir` |
| Create nested directories | `mkdir -p a/b/c` |
| Copy file | `cp src dest` |
| Copy file (safe) | `cp -i src dest` |
| Copy directory | `cp -r src dest` |
| Move / rename | `mv src dest` |
| Move / rename (safe) | `mv -i src dest` |
| Delete file | `rm file.txt` |
| Delete directory | `rm -r dir` |
| Force delete | `rm -rf dir` |
| Delete empty directory | `rmdir dir` |
| Delete all `.log` files | `rm *.log` |
| Match single character | `ls file-?.txt` |
| Print file | `cat file.txt` |
| Scroll through file | `less file.txt` |
| First N lines | `head -n N file.txt` |
| Last N lines | `tail -n N file.txt` |
| Watch file live | `tail -f file.txt` |
| Identify file type | `file filename` |

---

## Key mental models

1. `>` wipes the whole file. `>>` adds to it. One character difference, huge consequence.
2. `mv` has no copy — the original disappears. `cp` always leaves the source intact.
3. `-i` on `cp`, `mv`, and `rm` asks before overwriting or deleting — use it when unsure.
4. `rm -rf` is irreversible. No undo, no bin, no second chances.
5. `rmdir` is your safety net — it refuses to delete anything non-empty.
6. `cat` for short files, `less` for long ones, `tail -f` for live logs.
7. `*` matches anything, `?` matches exactly one character. Always `ls` before a destructive wildcard command.