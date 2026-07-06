## Revised Markdown File (With Additions)

# 09 — systemd & Services

## Checklist

- ✅ What systemd is — PID 1, units
- ✅ Service management — `start`, `stop`, `restart`, `reload`, `status`
- ✅ Enabling & disabling at boot
- ✅ Masking and unmasking units
- ✅ Viewing and editing unit files — `cat`, `edit`
- ✅ Listing and inspecting units
- ✅ Viewing logs — `journalctl`
- ✅ Writing a basic unit file
- ✅ Timers — systemd's cron replacement
- ✅ Targets — systemd's equivalent of runlevels
- ✅ System control — `reboot`, `poweroff`, `suspend`
- ✅ Boot performance — `systemd-analyze`

---

## What is systemd?

When the Linux kernel finishes booting, the first process it starts is PID 1.
On modern Linux, PID 1 is **systemd**. Everything that follows — starting
services, mounting filesystems, setting up networking — is orchestrated by
systemd.

systemd manages **units** — its name for any resource it knows how to
manage. The most common unit type is a **service** (a background process),
but units can also represent mount points, timers, sockets, and more.

### Unit file locations

| Path                   | Purpose                                            |
| ---------------------- | -------------------------------------------------- |
| `/lib/systemd/system/` | Default unit files installed by packages           |
| `/etc/systemd/system/` | Your overrides and custom units — takes precedence |

---

## Service management — `systemctl`

`systemctl` is the command used to interact with systemd.

```bash
sudo systemctl start nginx        # start a service now
sudo systemctl stop nginx         # stop a service now
sudo systemctl restart nginx      # stop then start
sudo systemctl reload nginx       # reload config without stopping (if supported)
sudo systemctl status nginx       # show current state and recent logs
```

### Reading `systemctl status` output

```
● nginx.service - A high performance web server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled)
     Active: active (running) since Mon 2025-06-09 10:00:00 UTC
   Main PID: 1234 (nginx)
```

| Field                      | Meaning                                    |
| -------------------------- | ------------------------------------------ |
| `Loaded`                   | Whether the unit file was found and parsed |
| `Active: active (running)` | Service is currently running               |
| `Active: inactive (dead)`  | Service is not running                     |
| `Active: failed`           | Service tried to start but crashed         |
| `enabled`                  | Will start automatically at boot           |
| `disabled`                 | Will not start at boot                     |

---

## Enabling & disabling at boot

`systemctl start` only lasts until the next reboot. To make a service
persistent across reboots:

```bash
sudo systemctl enable nginx           # start automatically at boot
sudo systemctl disable nginx          # remove from boot sequence
sudo systemctl enable --now nginx     # enable AND start immediately in one step
sudo systemctl is-enabled nginx       # check if set to start at boot
sudo systemctl is-active nginx        # check if currently running
```

> `enable` and `start` are separate operations. A service can be enabled
> (starts at boot) but currently stopped, or started now but not enabled
> (won't survive a reboot). Use `enable --now` to do both at once.

---

## Masking & unmasking — preventing accidental starts

Masking is stronger than disabling — it symlinks the unit to `/dev/null`,
preventing it from starting even manually.

```bash
sudo systemctl mask nginx       # prevent from ever starting (even manually)
sudo systemctl unmask nginx     # undo the mask
```

Useful for preventing services from starting accidentally.

---

## Viewing and editing unit files

### `systemctl cat` — view the effective unit file

```bash
systemctl cat nginx             # show the unit file systemd is actually using
```

Shows you the effective unit file after all overrides are applied.

### `systemctl edit` — safe way to override unit files

```bash
sudo systemctl edit nginx       # create an override file in /etc/systemd/system/
sudo systemctl edit --full nginx # edit the full unit file
```

Instead of copying the entire unit file, `systemctl edit` creates a small drop-in override. Safer and cleaner for customizations.

### `systemctl show` — view all unit properties

```bash
systemctl show nginx            # show ALL properties of a unit
systemctl show nginx -p LoadState # show one specific property
```

When debugging, `systemctl show` exposes every detail systemd knows about a unit.

---

## Listing and inspecting units

```bash
systemctl list-units                        # all currently loaded units
systemctl list-units --type=service         # only services
systemctl list-units --state=failed         # only failed units
systemctl list-unit-files --type=service    # all service unit files with enabled/disabled status
```

---

## Viewing logs — `journalctl`

systemd captures log output from every managed service into a centralised
binary log called the **journal**. `journalctl` is how you read it.

```bash
journalctl                          # all logs (oldest first)
journalctl -r                       # reverse — newest first
journalctl -n 50                    # last 50 lines
journalctl -f                       # follow — live updates (like tail -f)
journalctl -u nginx                 # logs for one specific service
journalctl -u nginx -f              # follow logs for one service
journalctl --since "1 hour ago"     # logs from the last hour
journalctl --since "2025-06-09"     # logs from a specific date
journalctl -p err                   # only error-level messages
journalctl -b                       # logs from the current boot only
journalctl -b -1                    # logs from the previous boot
journalctl -u nginx -e              # jump to the end of the log
journalctl -u nginx --since today   # logs from today only
journalctl -u nginx -o json         # output as JSON (useful for parsing)
journalctl --disk-usage             # show how much space logs are using
journalctl --vacuum-size=100M       # reduce log size to 100MB
```

> `journalctl -u servicename -f` is the main debugging tool when a service
> fails or behaves unexpectedly — watch logs in real time as you restart
> the service.

---

## Writing a basic unit file

A unit file is a plain text config file that tells systemd how to manage
a service. Minimal working example:

```ini
[Unit]
Description=My simple script
After=network.target

[Service]
ExecStart=/usr/local/bin/my-script.sh
Restart=on-failure
User=codespace

[Install]
WantedBy=multi-user.target
```

### Section by section

**`[Unit]`** — metadata and dependencies

- `Description` — human-readable name shown in `systemctl status`
- `After` — start only after this unit is ready (ordering, not a hard dependency)

**`[Service]`** — how to run the service

- `ExecStart` — full command to run (must be an absolute path)
- `Restart` — when to auto-restart (`on-failure`, `always`, `never`)
- `User` — which user account to run the process as

**`[Install]`** — when to activate at boot

- `WantedBy=multi-user.target` — standard for most server services

### Deploying a custom unit file

```bash
sudo cp my-script.service /etc/systemd/system/
sudo systemctl daemon-reload          # tell systemd to re-read unit files
sudo systemctl enable --now my-script
sudo systemctl status my-script
```

> Always run `daemon-reload` after creating or editing a unit file —
> systemd does not pick up file changes automatically.

---

## Timers — systemd's cron replacement

Systemd timers are replacing cron on modern Linux distributions. They're more flexible and integrated with systemd's logging.

```bash
systemctl list-timers           # list all active timers
```

Basic timer unit example:

```ini
[Unit]
Description=Run backup daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

---

## Targets — systemd's runlevels

A **target** is a group of units that together represent a system state.
They replace the concept of runlevels from older Unix systems.

| Target              | Meaning                                        |
| ------------------- | ---------------------------------------------- |
| `poweroff.target`   | System off                                     |
| `rescue.target`     | Single-user emergency mode                     |
| `multi-user.target` | Full multi-user, no GUI — standard for servers |
| `graphical.target`  | Multi-user with desktop GUI                    |
| `reboot.target`     | Reboot                                         |

```bash
systemctl get-default                         # see the default boot target
sudo systemctl set-default multi-user.target  # boot without GUI (server mode)
sudo systemctl isolate rescue.target          # switch to rescue mode now
```

> `WantedBy=multi-user.target` in your unit file means: "add me to the boot
> sequence when `multi-user.target` is activated" — which is every normal
> server boot.

---

## System control — `reboot`, `poweroff`, `suspend`

These are the proper systemd commands for system control.

```bash
sudo systemctl reboot           # reboot the system
sudo systemctl poweroff         # power off
sudo systemctl suspend          # suspend to RAM
```

---

## Boot performance — `systemd-analyze`

Essential for optimizing boot times on servers.

```bash
systemd-analyze                 # show boot time
systemd-analyze blame           # show which services take the longest to start
systemd-analyze critical-chain  # show the critical startup path
```

---

## Quick reference

| What you want           | Command                               |
| ----------------------- | ------------------------------------- |
| Start a service         | `sudo systemctl start name`           |
| Stop a service          | `sudo systemctl stop name`            |
| Restart a service       | `sudo systemctl restart name`         |
| Reload config (no stop) | `sudo systemctl reload name`          |
| Check service status    | `systemctl status name`               |
| Enable at boot          | `sudo systemctl enable name`          |
| Disable at boot         | `sudo systemctl disable name`         |
| Enable + start now      | `sudo systemctl enable --now name`    |
| Mask a service          | `sudo systemctl mask name`            |
| Unmask a service        | `sudo systemctl unmask name`          |
| Check if enabled        | `systemctl is-enabled name`           |
| Check if running        | `systemctl is-active name`            |
| View unit file          | `systemctl cat name`                  |
| Edit unit override      | `sudo systemctl edit name`            |
| List all services       | `systemctl list-units --type=service` |
| List failed units       | `systemctl list-units --state=failed` |
| View all logs           | `journalctl`                          |
| View service logs       | `journalctl -u name`                  |
| Follow service logs     | `journalctl -u name -f`               |
| Last 50 log lines       | `journalctl -n 50`                    |
| Logs from this boot     | `journalctl -b`                       |
| Error logs only         | `journalctl -p err`                   |
| Log disk usage          | `journalctl --disk-usage`             |
| Reload unit files       | `sudo systemctl daemon-reload`        |
| Get default target      | `systemctl get-default`               |
| List timers             | `systemctl list-timers`               |
| Show boot time          | `systemd-analyze`                     |
| Show slow services      | `systemd-analyze blame`               |
| Reboot system           | `sudo systemctl reboot`               |
| Power off system        | `sudo systemctl poweroff`             |

---

## Key mental models

1. systemd is PID 1 — the root of everything after the kernel hands off control.

2. A unit is anything systemd manages — services, mounts, timers, sockets. The service unit is the most common.

3. `start`/`stop` affects right now. `enable`/`disable` affects boot. They are independent — use `enable --now` to do both.

4. Unit files in `/etc/systemd/system/` override those in `/lib/systemd/system/`. Always put custom files in `/etc/`.

5. After editing any unit file, always run `daemon-reload` before restarting the service.

6. The journal is systemd's centralised log. `journalctl -u name -f` is your first stop when a service misbehaves.

7. `multi-user.target` is the standard boot target for servers — no GUI, full networking, all services.

8. Masking a unit (`systemctl mask`) is stronger than disabling — it prevents the service from starting even manually.

9. `systemctl edit` is the safe way to override unit files — it creates drop-ins instead of copying the whole file.

10. Timers are systemd's answer to cron — more flexible, integrated with logging, and easier to manage.
