# 06 — Package Management

## Checklist

- ✅ What package management is — why it exists
- ✅ `apt` — Debian/Ubuntu package manager (install, remove, update, upgrade)
- ✅ `apt` vs `apt-get` vs `apt-cache` — which one to use
- ✅ Package repositories — where packages come from
- ✅ Searching for packages
- ✅ Checking what's installed
- ✅ `apt autoremove` — cleaning up dependencies
- ✅ Installing `.deb` files directly
- ✅ Adding third-party repositories (PPAs)
- ✅ `apt` history logs
- ✅ Finding where a package installed files
- ✅ Other package managers (brief) — `dpkg`, `snap`

---

## What is package management?

Every piece of software installed on Linux — `tree`, `htop`, `docker`,
anything — is called a **package**. A package bundles the program itself,
its dependencies (other software it needs to run), and instructions for
where everything should go on the filesystem.

Before package managers existed, installing software meant manually
downloading files, compiling source code, and resolving dependencies by
hand. A **package manager** automates all of that — it downloads,
installs, updates, and removes software, and tracks what's installed so
nothing gets left behind or duplicated.

Different Linux distributions use different package managers:

| Distribution family     | Package manager |
| ----------------------- | --------------- |
| Debian, Ubuntu          | `apt`           |
| Red Hat, Fedora, CentOS | `dnf` / `yum`   |
| Arch Linux              | `pacman`        |

Codespaces runs Ubuntu, so `apt` is the one in use here.

---

## `apt` — the Debian/Ubuntu package manager

`apt` stands for **Advanced Package Tool**.

### `apt` vs `apt-get` vs `apt-cache`

| Command     | Purpose                                                    | Recommendation                                  |
| ----------- | ---------------------------------------------------------- | ----------------------------------------------- |
| `apt`       | Modern, user-friendly interface for all package operations | ✅ Use this                                     |
| `apt-get`   | Older, lower-level, script-friendly                        | Legacy — avoid day-to-day                       |
| `apt-cache` | Search/show without modifying                              | Legacy — `apt search` and `apt show` replace it |

> For day-to-day use, `apt` replaces both `apt-get` and `apt-cache`. It's
> the one command to know.

### Updating the package list

```bash
sudo apt update
```

This does **not** install or upgrade anything — it refreshes `apt`'s local
list of what packages exist and what versions are available, by checking
the repositories. Always run this before installing something new.

### Installing a package

```bash
sudo apt install tree -y
```

`-y` answers "yes" to confirmation prompts automatically.

### Removing a package

```bash
sudo apt remove tree        # removes the program, keeps its config files
sudo apt purge tree         # removes the program AND its config files
```

### Upgrading packages

```bash
sudo apt upgrade            # upgrade all installed packages to latest versions
sudo apt upgrade tree       # upgrade one specific package
```

> `apt update` refreshes the list of what's available.
> `apt upgrade` actually installs the newer versions.
> Two separate steps — easy to confuse.

### `apt autoremove` — clean up dependencies

```bash
sudo apt autoremove        # remove packages that were installed as dependencies
                           # but are no longer needed by anything
```

> When you `apt remove` a package, its dependencies often remain installed.
> `autoremove` cleans them up automatically. Run it regularly to keep your
> system tidy.

---

## Where packages come from — repositories

A **repository** is a server that hosts packages (here meaning a package
source — different from a Git repo). Ubuntu's official repositories are
configured by default.

On modern Ubuntu (24.04 "noble" and later), repo configuration has moved:

```bash
cat /etc/apt/sources.list                       # mostly empty now — just a pointer comment
cat /etc/apt/sources.list.d/ubuntu.sources       # actual repo config, in deb822 format
```

> Older Ubuntu versions kept everything in a single `sources.list` file.
> If that file looks empty on a newer system, check the `.d/` directory.

### Reading a repository line

```
http://archive.ubuntu.com/ubuntu noble main amd64 Packages
                                  │     │
                                  │     └── component
                                  └── release codename (noble = 24.04)
```

| Component    | What it contains                                 |
| ------------ | ------------------------------------------------ |
| `main`       | Officially supported, open-source software       |
| `restricted` | Officially supported, proprietary (e.g. drivers) |
| `universe`   | Community-maintained open-source software        |
| `multiverse` | Software with licensing restrictions             |

`noble-updates`, `noble-security`, `noble-backports` are the same release
with different update channels — general updates, security patches, and
newer software backported to the current version.

### Adding third-party repositories (PPAs)

```bash
sudo add-apt-repository ppa:nginx/stable    # add a Personal Package Archive
sudo apt update
sudo apt install nginx
```

> PPAs (Personal Package Archives) are third-party repositories on Launchpad.
> Add them first, then `update`, then install. Be cautious — PPAs can
> conflict with official packages.

---

## Searching for and inspecting packages

```bash
apt search docker              # search package names/descriptions
apt show docker.io             # detailed info — version, size, dependencies
```

## Checking what's installed

```bash
apt list --installed                  # every installed package
apt list --installed | grep tree      # check if a specific one is installed
dpkg -l | grep tree                   # alternative, lower-level way to check
apt list --upgradable                 # see exactly which packages have updates available
```

### `apt` history logs

```bash
cat /var/log/apt/history.log         # see what was installed/removed and when
cat /var/log/apt/term.log            # see the actual terminal output of apt operations
```

> These logs are your audit trail — helpful when debugging or reviewing
> what changed on the system.

### Finding where a package installed files

```bash
which tree          # /usr/bin/tree — shows the executable path
whereis tree        # tree: /usr/bin/tree /usr/share/man/man1/tree.1.gz
dpkg -L tree        # list EVERY file installed by the "tree" package
```

> `dpkg -L` shows the complete file list for a package — useful for seeing
> what was added to the system. Try it on a package you've installed.

---

## Other package tools (brief)

| Tool   | Relationship to `apt`                                                                                                                                    |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dpkg` | The lower-level tool `apt` is built on top of. Installs `.deb` files directly. `apt` is the friendly wrapper around it.                                  |
| `snap` | A separate, newer packaging system — bundles an app with all its dependencies in an isolated container, independent of `apt`. `sudo snap install <name>` |

`apt` covers nearly everything day to day — `dpkg` is rarely used directly.

### Installing `.deb` files directly

```bash
sudo dpkg -i package.deb            # install a .deb file directly
sudo apt install -f                 # fix missing dependencies
```

> `dpkg -i` installs the `.deb`, but doesn't resolve dependencies automatically.
> Follow it with `apt install -f` to pull in any missing ones.

---

## Quick reference

| What you want                  | Command                             |
| ------------------------------ | ----------------------------------- |
| Refresh package list           | `sudo apt update`                   |
| Install a package              | `sudo apt install name -y`          |
| Remove a package (keep config) | `sudo apt remove name`              |
| Remove a package + config      | `sudo apt purge name`               |
| Clean up unused dependencies   | `sudo apt autoremove`               |
| Upgrade all packages           | `sudo apt upgrade`                  |
| Upgrade one package            | `sudo apt upgrade name`             |
| Search for a package           | `apt search name`                   |
| Show package details           | `apt show name`                     |
| List installed packages        | `apt list --installed`              |
| Check if installed             | `apt list --installed \| grep name` |
| List upgradable packages       | `apt list --upgradable`             |
| Add a PPA repository           | `sudo add-apt-repository ppa:name`  |
| Install a `.deb` file          | `sudo dpkg -i package.deb`          |
| Fix missing dependencies       | `sudo apt install -f`               |
| View apt history               | `cat /var/log/apt/history.log`      |
| Find executable path           | `which command`                     |
| Find all files from package    | `dpkg -L package`                   |
| Install via Snap               | `sudo snap install name`            |

---

## Key mental models

1. A package bundles a program with its dependencies and install instructions.
2. `apt update` refreshes the list of what's available — it changes nothing on disk. `apt upgrade` actually installs newer versions.
3. `apt` replaces `apt-get` and `apt-cache` for day-to-day use — it's the one command to know.
4. Repo config on modern Ubuntu lives in `/etc/apt/sources.list.d/ubuntu.sources`, not the old `sources.list`.
5. `remove` keeps config files behind; `purge` removes everything.
6. `autoremove` cleans up orphaned dependencies — run it regularly.
7. `dpkg` is the low-level engine; `apt` is the user-friendly layer on top of it.
8. `snap` is a separate, sandboxed packaging system — independent of `apt`.
9. `dpkg -L` shows every file a package installed — useful for exploring what's on your system.
10. PPAs give access to newer or third-party software, but use them cautiously.

```

---
```
