## Revised Markdown File (With Additions)

# 10 — Text Processing (grep/sed/awk/pipes)

## Checklist

- ✅ Pipes — `|`
- ✅ `grep` — searching text
- ✅ `grep` context flags — `-A`, `-B`, `-C`
- ✅ `grep -o` — extracting matches
- ✅ `sed` — stream editing
- ✅ `awk` — field processing
- ✅ `cut` — extracting columns
- ✅ `sort`, `uniq`, `wc` — utility commands
- ✅ `tr` — translating characters
- ✅ `find` — powerful file searching
- ✅ `xargs` — building command lines
- ✅ Combining tools into pipelines

---

## Pipes — `|`

A **pipe** takes the output of one command and feeds it directly as input
to the next — no intermediate files needed.

```bash
command1 | command2 | command3
```

Data flows left to right. Each command does one thing; pipes chain them
together into a pipeline.

```bash
ls /etc | wc -l              # count how many entries are in /etc
cat /etc/passwd | grep root  # find root-related lines in passwd
ps aux | sort -k3 -rn        # list processes sorted by CPU usage
```

> The Unix philosophy: small tools that each do one thing well, combined
> through pipes to do something powerful.

---

## `grep` — searching text

`grep` searches for a pattern in text and prints matching lines.

```bash
grep "root" /etc/passwd              # lines containing "root"
grep -i "root" /etc/passwd           # case-insensitive
grep -v "root" /etc/passwd           # invert — lines NOT containing "root"
grep -n "root" /etc/passwd           # show line numbers
grep -r "root" /etc/                 # recursive — search all files in /etc
grep -l "root" /etc/*                # only show filenames, not matching lines
grep -c "root" /etc/passwd           # count matching lines
grep -E "root|sudo" /etc/passwd      # extended regex — match root OR sudo
grep "^root" /etc/passwd             # lines starting with "root"
grep "bash$" /etc/passwd             # lines ending with "bash"
grep -q "pattern" file.txt           # quiet mode — no output (for scripts)
```

### Context flags — seeing surrounding lines

```bash
grep -A 3 "error" log.txt    # show 3 lines AFTER match
grep -B 2 "error" log.txt    # show 2 lines BEFORE match
grep -C 1 "error" log.txt    # show 1 line BEFORE AND AFTER match
```

### `grep -o` — extract only the matching part

```bash
grep -o '[0-9]*' file.txt    # extract only numbers
grep -o -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' log.txt  # extract IPs
```

### Regex basics used in grep

| Pattern | Matches                      |
| ------- | ---------------------------- |
| `.`     | Any single character         |
| `*`     | Zero or more of the previous |
| `^`     | Start of line                |
| `$`     | End of line                  |
| `[abc]` | Any one of a, b, or c        |
| `[0-9]` | Any digit                    |
| `\b`    | Word boundary                |

---

## `sed` — stream editor

`sed` reads text line by line and applies transformations. Most common
use: find-and-replace.

```bash
sed 's/old/new/' file.txt             # replace first occurrence per line
sed 's/old/new/g' file.txt            # replace ALL occurrences per line (g=global)
sed 's/old/new/gi' file.txt           # case-insensitive replace
sed -i 's/old/new/g' file.txt         # edit the file in place
sed -n '5,10p' file.txt               # print only lines 5 to 10
sed '3d' file.txt                     # delete line 3
sed '/root/d' file.txt                # delete all lines containing "root"
sed 's/^/> /' file.txt                # prepend "> " to every line
```

### Multiple expressions

```bash
sed -e 's/old1/new1/g' -e 's/old2/new2/g' file.txt
```

> `-i` makes `sed` edit the file directly. Without `-i`, it only prints to
> the screen — the file is untouched. Always test without `-i` first.

---

## `awk` — field processor

`awk` treats each line as a set of fields separated by whitespace (or a
delimiter you specify). Best for extracting specific columns from
structured text.

```bash
awk '{print $1}' file.txt             # print the first field of every line
awk '{print $1, $3}' file.txt         # print fields 1 and 3
awk -F: '{print $1}' /etc/passwd      # use : as delimiter, print first field
awk -F: '{print $1, $7}' /etc/passwd  # print username and login shell
awk '$3 > 1000' /etc/passwd           # print lines where field 3 > 1000
awk 'NR==5' file.txt                  # print only line 5
awk 'NR>=2 && NR<=5' file.txt         # print lines 2 through 5
awk '{sum += $1} END {print sum}'     # sum all values in field 1
```

### BEGIN and END patterns

```bash
awk 'BEGIN {print "Start"} {print $1} END {print "End"}' file.txt
```

Useful for adding headers and footers.

### Special awk variables

| Variable      | Meaning                               |
| ------------- | ------------------------------------- |
| `$0`          | The entire line                       |
| `$1`, `$2`... | Individual fields                     |
| `NR`          | Current line number                   |
| `NF`          | Number of fields on the current line  |
| `FS`          | Field separator (default: whitespace) |

---

## `cut` — extracting columns

Simpler than `awk` for basic column extraction from delimited files.

```bash
cut -d: -f1 /etc/passwd               # delimiter=colon, field 1 (usernames)
cut -d: -f1,7 /etc/passwd             # extract fields 1 and 7
cut -c1-5 file.txt                    # characters 1 through 5 of each line
```

> Use `cut` for simple extraction, `awk` when you need logic or conditions.

---

## `sort`, `uniq`, `wc`

### `sort` — sort lines

```bash
sort file.txt                          # alphabetical sort
sort -r file.txt                       # reverse order
sort -n file.txt                       # numeric sort
sort -k2 file.txt                      # sort by second field
sort -k3 -rn file.txt                  # sort by field 3, numeric, reversed
sort -u file.txt                       # sort and remove duplicates
```

### `uniq` — deduplicate adjacent lines

```bash
uniq file.txt                          # remove consecutive duplicate lines
uniq -c file.txt                       # count occurrences of each line
uniq -d file.txt                       # only show duplicated lines
sort file.txt | uniq                   # full deduplication (sort first)
sort file.txt | uniq -c | sort -rn     # count frequency, most common first
```

> `uniq` only deduplicates **adjacent** lines — always `sort` first for
> full deduplication.

### `wc` — word/line/character count

```bash
wc file.txt                            # lines, words, characters
wc -l file.txt                         # line count only
wc -w file.txt                         # word count only
wc -c file.txt                         # byte count only
ls /etc | wc -l                        # count entries in /etc
```

---

## `tr` — translate characters

`tr` reads from stdin and replaces or deletes individual characters.

```bash
echo "hello" | tr 'a-z' 'A-Z'         # lowercase to uppercase
echo "HELLO" | tr 'A-Z' 'a-z'         # uppercase to lowercase
echo "hello world" | tr -d 'l'        # delete all occurrences of 'l'
echo "hello   world" | tr -s ' '      # squeeze multiple spaces into one
cat file.txt | tr '\n' ','            # replace newlines with commas
```

---

## `find` — powerful file searching

`find` is the go-to tool for locating files and is often combined with `xargs`.

```bash
find . -name "*.log"               # find all .log files
find /etc -type f -name "*.conf"   # find all .conf files
find . -mtime -1                   # files modified within last 24 hours
find . -size +10M                  # files larger than 10MB
find . -name "*.tmp" -delete       # find and delete .tmp files
find . -type f -exec grep -l "error" {} \;  # find files containing "error"
```

---

## `xargs` — building command lines from stdin

`xargs` is how you take output from one command and use it as arguments to another. Essential for batch operations.

```bash
cat files.txt | xargs rm          # delete all files listed in files.txt
cat files.txt | xargs -n1 rm      # delete one at a time
find . -name "*.log" | xargs rm   # find and delete all .log files
find . -name "*.txt" | xargs wc -l # count lines in all .txt files
```

---

## Combining tools into pipelines

Real command-line work is almost always a pipeline. Small tools,
chained together.

### Most common login shells on the system

```bash
cat /etc/passwd | cut -d: -f7 | sort | uniq -c | sort -rn
```

1. `cut -d: -f7` — extract shell field
2. `sort` — required before `uniq`
3. `uniq -c` — count each unique shell
4. `sort -rn` — highest count first

### Top 5 processes by memory usage

```bash
ps aux | sort -k4 -rn | head -n 5
```

### Count users with bash as their shell

```bash
grep "/bin/bash$" /etc/passwd | wc -l
```

### Search all scripts in a directory for a function name

```bash
grep -r "function_name" /path/to/scripts/ | grep "\.sh$"
```

### Extract and rank IPs from a log file

```bash
grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' access.log \
  | sort | uniq -c | sort -rn
```

### Find and delete all .tmp files

```bash
find . -name "*.tmp" -type f | xargs rm
```

### Count lines in all .log files

```bash
find . -name "*.log" -type f | xargs wc -l
```

---

## Quick reference

| What you want                  | Command                                        |
| ------------------------------ | ---------------------------------------------- |
| Pipe output to another command | `cmd1 \| cmd2`                                 |
| Search for pattern             | `grep "pattern" file`                          |
| Case-insensitive search        | `grep -i "pattern" file`                       |
| Invert match                   | `grep -v "pattern" file`                       |
| Context after match            | `grep -A 3 "pattern" file`                     |
| Context before match           | `grep -B 3 "pattern" file`                     |
| Context around match           | `grep -C 1 "pattern" file`                     |
| Extract only matching part     | `grep -o "pattern" file`                       |
| Quiet mode (no output)         | `grep -q "pattern" file`                       |
| Recursive search               | `grep -r "pattern" dir/`                       |
| Count matching lines           | `grep -c "pattern" file`                       |
| Find-replace (print only)      | `sed 's/old/new/g' file`                       |
| Find-replace (edit in place)   | `sed -i 's/old/new/g' file`                    |
| Delete matching lines          | `sed '/pattern/d' file`                        |
| Print specific line range      | `sed -n '5,10p' file`                          |
| Multiple sed expressions       | `sed -e 's/old/new/g' -e 's/old2/new2/g' file` |
| Print specific field           | `awk '{print $2}' file`                        |
| Custom delimiter               | `awk -F: '{print $1}' file`                    |
| Conditional field filter       | `awk '$3 > 100' file`                          |
| BEGIN/END in awk               | `awk 'BEGIN {...} {...} END {...}' file`       |
| Extract column (simple)        | `cut -d: -f1 file`                             |
| Sort alphabetically            | `sort file`                                    |
| Sort numerically               | `sort -n file`                                 |
| Sort by field                  | `sort -k2 file`                                |
| Remove duplicate lines         | `sort file \| uniq`                            |
| Count occurrences              | `sort file \| uniq -c \| sort -rn`             |
| Count lines                    | `wc -l file`                                   |
| To uppercase                   | `echo "text" \| tr 'a-z' 'A-Z'`                |
| Delete a character             | `echo "text" \| tr -d 'x'`                     |
| Find files by name             | `find . -name "*.txt"`                         |
| Find files by type             | `find . -type f -name "*.conf"`                |
| Find recently modified files   | `find . -mtime -1`                             |
| Find and delete files          | `find . -name "*.tmp" -delete`                 |
| Build command lines from stdin | `cat list.txt \| xargs command`                |

---

## Key mental models

1. Pipes connect commands — output of one becomes input of the next. Data flows left to right.

2. `grep` finds lines. `sed` transforms lines. `awk` works on fields within lines. `cut` extracts fields simply.

3. `grep -v` inverts — prints everything that does NOT match. Useful for filtering noise.

4. `grep -A`/`-B`/`-C` show context around matches — essential for debugging logs.

5. `grep -o` extracts just the matching part — perfect for pulling IPs, email addresses, etc.

6. `sed` without `-i` is safe — it only prints, never modifies. Add `-i` only when sure.

7. `awk -F:` sets the delimiter — essential for colon-separated files like `/etc/passwd`.

8. `uniq` only removes adjacent duplicates — always `sort` first for true deduplication.

9. `find` locates files; `xargs` builds commands from that output — a powerful combination.

10. Build pipelines incrementally — add one command at a time and verify output before adding the next.
