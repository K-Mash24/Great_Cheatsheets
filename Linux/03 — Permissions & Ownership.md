# 03 — Permissions & Ownership

## Checklist
- ✅ How Linux permissions work — read, write, execute
- ✅ The permission string — decoded
- ✅ Owners — user, group, other
- ✅ `chmod` — changing permissions (symbolic + numeric)
- ✅ `chown` — changing ownership
- ✅ `chgrp` — changing group
- ✅ `sudo` — acting as administrator

---

## Why permissions exist

Linux is a multi-user operating system — multiple users can be on the same
machine at once. Permissions control who can read, modify, or execute any
given file or directory.

Every file has three things attached to it:
- One user owner
- One group owner
- A set of permissions for each category of user

---

## The three permission types

| Permission | Symbol | On a file | On a directory |
|------------|--------|-----------|----------------|
| Read | `r` | View contents | List contents with `ls` |
| Write | `w` | Modify or delete | Create, delete, rename files inside |
| Execute | `x` | Run as a program | Enter with `cd` |

> You need `x` on a directory just to `cd` into it — even if you have `r`.

---

## The three user categories

| Category | Symbol | Who it applies to |
|----------|--------|------------------|
| User | `u` | The owner of the file |
| Group | `g` | Anyone in the file's assigned group |
| Other | `o` | Everyone else on the system |

---

## Reading the permission string

```
d  rwx  r-x  r-x
│   │    │    │
│   │    │    └── other
│   │    └─────── group
│   └──────────── user (owner)
└──────────────── type: d=directory  -=file  l=symlink
```

Each block of three is always `r` then `w` then `x`. A `-` means that
permission is not granted.

### Real examples

| Output | Meaning |
|--------|---------|
| `-rw-r--r--` | File. Owner: read+write. Group: read. Other: read. |
| `drwxr-xr-x` | Directory. Owner: full. Group: read+execute. Other: read+execute. |
| `drwx------` | Directory. Owner: full. Group: none. Other: none. |
| `drwxrwxrwt` | Directory. Everyone: full. Sticky bit set (`t`). |

### Real system examples observed

| Path | Permissions | Why |
|------|-------------|-----|
| `/etc/hosts` | `-rw-r--r--` | Root edits it, everyone reads it |
| `/etc/passwd` | `-rw-r--r--` | Same — user list is public but root-controlled |
| `/tmp` | `drwxrwxrwt` | Shared scratch pad — sticky bit prevents deleting others' files |
| `/root` | `drwx------` | Admin's home — completely locked to everyone else |

---

## `chmod` — changing permissions

### Symbolic mode

```bash
chmod [who][operator][permission] filename
```

| Who | Operator | Permission |
|-----|----------|------------|
| `u` user | `+` add | `r` read |
| `g` group | `-` remove | `w` write |
| `o` other | `=` set exactly | `x` execute |
| `a` all | | |

```bash
chmod u+x script.sh          # add execute for owner
chmod g-w notes.txt          # remove write from group
chmod o=r notes.txt          # set other to read only
chmod a+r notes.txt          # give everyone read
chmod u+x,g-w notes.txt      # multiple changes at once
```

### Numeric mode

| Permission | Value |
|------------|-------|
| `r` | 4 |
| `w` | 2 |
| `x` | 1 |
| none | 0 |

Add them up for each category (user, group, other):

| Number | Permissions | Calculation |
|--------|-------------|-------------|
| `7` | `rwx` | 4+2+1 |
| `6` | `rw-` | 4+2+0 |
| `5` | `r-x` | 4+0+1 |
| `4` | `r--` | 4+0+0 |
| `0` | `---` | 0+0+0 |

```bash
chmod 755 script.sh     # rwxr-xr-x — scripts, directories
chmod 644 notes.txt     # rw-r--r-- — regular files, config files
chmod 700 private.txt   # rwx------ — owner only, full access
chmod 600 secret.txt    # rw------- — owner read+write only
chmod 777 shared.txt    # rwxrwxrwx — full access for everyone
```

> `755` and `644` are the two most common values — memorise them.

---

## `chown` — changing ownership

```bash
chown newowner filename
chown user:group filename          # change both at once
chown -R user:group directory/     # recursive — apply to whole directory
```

```bash
sudo chown root notes.txt          # make root the owner
sudo chown codespace notes.txt     # give back to codespace
sudo chown codespace:root notes.txt # owner=codespace, group=root
```

> `chown` requires `sudo` — only root can transfer ownership of files.
> A regular user cannot take ownership away from root without sudo.

---

## `chgrp` — changing group

Changes only the group owner of a file.

```bash
chgrp newgroup filename
chgrp root notes.txt               # assign to root group
chgrp -R codespace projects/       # recursive
```

> In practice, `chown user:group` does both at once so `chgrp` is rarely needed.

---

## `sudo` — acting as administrator

`sudo` (superuser do) lets an authorised user run a single command with
root privileges.

```bash
sudo chown root notes.txt          # run as root
sudo chmod 600 /etc/hosts          # modify a system file
```

| Term | Meaning |
|------|---------|
| `root` | The administrator account — no permission restrictions |
| `sudo` | A way for a regular user to act as root for one command |
| sudoers | The list of users allowed to use `sudo` |

> `sudo` asks for your password the first time, then remembers for a few minutes.

---

## Quick reference

| What you want | Command |
|---------------|---------|
| View permissions | `ls -l filename` |
| Give owner execute | `chmod u+x file` |
| Remove group write | `chmod g-w file` |
| Set other to read only | `chmod o=r file` |
| Common file permissions | `chmod 644 file` |
| Common script permissions | `chmod 755 file` |
| Owner only, full access | `chmod 700 file` |
| Change file owner | `sudo chown user file` |
| Change owner and group | `sudo chown user:group file` |
| Change recursively | `sudo chown -R user:group dir/` |
| Change group only | `chgrp group file` |
| Run as administrator | `sudo command` |

---

## Key mental models

1. Every file has one owner, one group, and permissions for three categories: user, group, other.
2. Permissions are always read in order: `r` then `w` then `x`. A `-` means denied.
3. Execute on a directory means the ability to `cd` into it — not just to run programs.
4. Numeric mode: 7=rwx, 6=rw-, 5=r-x, 4=r--, 0=---. Three digits = user/group/other.
5. `755` for scripts and directories. `644` for regular files. Memorise these two.
6. `chown` needs `sudo`. Regular users cannot reassign ownership away from root.
7. `sudo` is not a user — it's a temporary privilege escalation for one command.