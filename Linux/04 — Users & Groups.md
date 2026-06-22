# 04 — Users & Groups

## Checklist
- ✅ What users and groups are
- ✅ `/etc/passwd` and `/etc/group` — where users and groups are stored
- ✅ `whoami`, `id`, `groups` — inspecting your own identity
- ✅ `useradd` / `usermod` / `userdel` — managing users
- ✅ `groupadd` / `groupmod` / `groupdel` — managing groups
- ✅ `passwd` — setting passwords
- ✅ Switching users — `su`

---

## What is a user?

Every process that runs on Linux runs as a specific user. Every file is owned
by a specific user. Users are how Linux tracks who is doing what and enforces
permissions.

| Type | Description | Example |
|------|-------------|---------|
| Root | The superuser — no restrictions | `root` |
| Regular | Human users with home directories | `codespace` |
| System | Created by software, not humans — run background services | `www-data`, `nobody` |

---

## What is a group?

A group is a collection of users. Instead of setting permissions for each
user individually, you put users in a group and set permissions on the
group once.

Every user has:
- One **primary group** — assigned at creation, same name as the user by default
- Zero or more **supplementary groups** — additional groups they belong to

> Real example observed: the `codespace` user belongs to its own primary
> group, plus supplementary groups created by installed tools — `docker`,
> `python`, `golang`, `nvm`, `ssh`, and more. Each tool creates a group and
> adds the user to it so commands work without needing `sudo` every time.

---

## Where users and groups are stored

### `/etc/passwd` — the user database

Passwords are **not** stored here despite the name. Each line is one user:

```
codespace:x:1000:1000::/home/codespace:/bin/bash
│         │ │    │    │ │              └── login shell
│         │ │    │    │ └── home directory
│         │ │    │    └── comment (usually full name)
│         │ │    └── primary group ID (GID)
│         │ └── user ID (UID)
│         └── password placeholder (x = stored in /etc/shadow)
└── username
```

### `/etc/group` — the group database

```
codespace:x:1000:
│         │ │    └── members (comma-separated)
│         │ └── group ID (GID)
│         └── password placeholder
└── group name
```

### `/etc/shadow` — actual passwords

Stores hashed passwords. Only readable by root — this is where real
password security lives.

---

## Inspecting your own identity

### `whoami`
Prints your username only. Deliberately simple — no flags, no extra info.
```bash
whoami
# codespace
```

### `id`
Prints your UID, GID, and every group you belong to in one shot.
```bash
id
# uid=1000(codespace) gid=1000(codespace) groups=1000(codespace),989(docker),988(golang)...
```

### `groups`
Prints just the group names — a simpler view than `id`.
```bash
groups
# codespace pipx python oryx golang docker sdkman rvm php conda nvs nvm hugo ssh
```

> All three should agree with what's in `/etc/passwd` and `/etc/group` —
> they're just different views of the same underlying data.

---

## Managing users

All of these require `sudo` since they affect the whole system.

### `useradd` — create a new user
```bash
sudo useradd newuser                    # minimal — NO home directory created
sudo useradd -m newuser                 # create WITH a home directory
sudo useradd -m -s /bin/bash newuser    # also set login shell
sudo useradd -m -s /bin/bash -G docker devuser   # add to a group at creation
```

| Flag | Meaning |
|------|---------|
| `-m` | Create a home directory |
| `-s` | Set the login shell |
| `-g` | Set primary group |
| `-G` | Set supplementary groups (comma-separated) |

> Without `-m`, no home directory is created. Almost always use `-m`.

### `usermod` — modify an existing user
```bash
sudo usermod -aG docker existinguser    # ADD to the docker group
sudo usermod -s /bin/bash existinguser  # change their shell
sudo usermod -l newname oldname         # rename the user
```

> `-aG` appends to a group. Without `-a`, `-G` **replaces** all their
> supplementary groups instead of adding one — a common mistake.
> The group must already exist via `groupadd` before you can add anyone to it.

### `userdel` — delete a user
```bash
sudo userdel newuser           # delete user, leave home directory behind
sudo userdel -r newuser        # delete user AND their home directory
```

---

## Managing groups

### `groupadd` — create a new group
```bash
sudo groupadd developers
```

### `groupmod` — modify a group
```bash
sudo groupmod -n newname oldname    # rename a group
```

### `groupdel` — delete a group
```bash
sudo groupdel developers
```

> Can't delete a group still set as someone's **primary** group — change
> their primary group first.

### Adding/removing a user from a group — two ways
```bash
sudo usermod -aG developers testuser    # add via usermod
sudo gpasswd -a testuser developers     # add via gpasswd
sudo gpasswd -d testuser developers     # remove via gpasswd
```

> **Verify with the source, not a summary.** `groups username` is a useful
> quick check, but when in doubt, check `/etc/group` directly:
> ```bash
> cat /etc/group | grep -E "developers|devteam"
> ```
> This caught a real typo during practice — a command created a stray
> group called `sevelopers` instead of `developers`. Linux doesn't validate
> group names against what you "meant" — a typo in a group-creating command
> silently creates a brand new real group. Always double check with
> `/etc/group` if something looks off.

---

## `passwd` — setting passwords

```bash
sudo passwd testuser        # set or change testuser's password (as admin)
passwd                      # change YOUR OWN password (no sudo needed)
sudo passwd -l testuser     # lock the account (disable login)
sudo passwd -u testuser     # unlock it
sudo passwd -d testuser     # delete the password entirely (risky — no password required to log in)
```

> Typed characters don't show on screen when entering a password — that's
> normal, not a glitch.

---

## Switching users — `su`

`su` stands for **switch user**.

```bash
su testuser           # switch to testuser, asks for THEIR password
su - testuser          # switch AND load their environment (home dir, shell config)
exit                   # return to your previous user
```

> The `-` matters. Without it, you keep your old environment but act as the
> new user. Always use `su - username`.

```bash
sudo -i                   # become root entirely, with root's own environment
sudo -u testuser whoami   # run ONE command as testuser, then return immediately
```

> `sudo -u` is the one used most in real work — running a single command as
> someone else without fully switching sessions.

> Note: in a containerized environment like Codespaces, `su - user` may not
> behave exactly like a standard Linux server (e.g. `pwd` may not land in
> their home directory as expected). The command itself is correct — the
> container environment is the variable.

---

## Quick reference

| What you want | Command |
|---------------|---------|
| Check your username | `whoami` |
| Check UID/GID/groups | `id` |
| Check group names only | `groups` |
| Create user with home dir | `sudo useradd -m -s /bin/bash username` |
| Add user to a group | `sudo usermod -aG groupname username` |
| Delete user (keep home) | `sudo userdel username` |
| Delete user + home dir | `sudo userdel -r username` |
| Create a group | `sudo groupadd groupname` |
| Rename a group | `sudo groupmod -n newname oldname` |
| Delete a group | `sudo groupdel groupname` |
| Add user to group (alt) | `sudo gpasswd -a username groupname` |
| Remove user from group | `sudo gpasswd -d username groupname` |
| Set/change a password | `sudo passwd username` |
| Lock an account | `sudo passwd -l username` |
| Switch user (full env) | `su - username` |
| Run one command as another user | `sudo -u username command` |
| Become root | `sudo -i` |

---

## Key mental models

1. `/etc/passwd` stores user info, not passwords. `/etc/shadow` stores the real (hashed) passwords.
2. Every user has exactly one primary group and any number of supplementary groups.
3. A group must exist (`groupadd`) before you can add anyone to it.
4. `usermod -aG` appends to groups. Leaving off `-a` replaces them entirely — a destructive mistake.
5. Typos in group names don't error — they silently create new, real groups. Verify against `/etc/group` when unsure.
6. `su - username` (with the dash) loads the target user's full environment. Without it, you keep your own.
7. `sudo -u username command` runs a single command as someone else — the most common real-world use case.
