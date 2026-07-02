# 07 — Networking Commands

## Checklist
- ✅ Checking your network configuration — `ip addr`, `ip link`, `hostname -I`
- ✅ Viewing and managing routes — `ip route`
- ✅ ARP and neighbour tables — `arp`, `ip neigh`
- ✅ Testing connectivity — `ping`
- ✅ DNS lookups — `dig`, `nslookup`, `whois`
- ✅ Tracing routes — `traceroute`, `tracepath`
- ✅ Checking open ports & connections — `ss`, `netstat`
- ✅ Transferring data — `curl`, `wget`
- ✅ SSH — connecting to remote machines
- ✅ Network service management — `systemctl`

---

## Checking your network configuration — `ip addr`, `ip link`

### `ip addr` — show IP addresses and interfaces

```bash
ip addr
ip addr show eth0      # show one specific interface
```

Output:
```
1: lo: <LOOPBACK,UP,LOWER_UP>
    link/loopback 00:00:00:00:00:00
    inet 127.0.0.1/8

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    link/ether ab:cd:ef:12:34:56
    inet 10.0.2.15/24
```

| Term | Meaning |
|------|---------|
| `lo` | Loopback interface — the machine talking to itself. Always `127.0.0.1` |
| `eth0` | First Ethernet interface — your actual network connection |
| `inet` | IPv4 address assigned to that interface |
| `/24` | Subnet mask in CIDR notation |

### `ip link` — show interface status only

```bash
ip link
ip link show eth0
```

Shows whether each interface is `UP` or `DOWN` without IP address detail.
Useful for quickly checking if a network interface is active.

### `hostname -I` — quick IP address lookup

```bash
hostname -I            # show all IP addresses assigned to the machine
```

Fastest way to see your machine's IP(s) without sifting through `ip addr` output.

### The old command — `ifconfig`

Replaced by `ip addr` on modern Linux but still appears in older tutorials.
Know it exists, prefer `ip addr`.

---

## Viewing and managing routes — `ip route`

```bash
ip route                    # show the full routing table
ip route show default       # show only the default gateway
```

Output:
```
default via 10.0.2.1 dev eth0 proto dhcp
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
```

| Field | Meaning |
|-------|---------|
| `default via` | Your default gateway — where traffic goes when no specific route matches |
| `dev eth0` | Which interface the route uses |
| `src` | Source IP used for outgoing traffic |

> The routing table is how Linux decides where to send traffic. The default
> gateway is the exit point — all traffic not destined for a local subnet
> goes through it.

---

## ARP and neighbour tables — `arp`, `ip neigh`

**ARP** (Address Resolution Protocol) maps IP addresses to MAC (Media
Access Control) addresses on the local network.

### `arp` — the classic command

```bash
arp -n                    # show ARP table (IP → MAC mappings)
arp -d 192.168.1.1        # delete an ARP entry
```

Output:
```
Address         HWtype  HWaddress          Iface
192.168.1.1     ether   aa:bb:cc:dd:ee:ff  eth0
```

| Field | Meaning |
|-------|---------|
| `Address` | IP address of the device |
| `HWaddress` | MAC address of the device |
| `Iface` | Interface the device is reachable on |

### `ip neigh` — modern ARP replacement

```bash
ip neigh                    # show neighbour table (ARP cache)
ip neigh flush dev eth0     # clear ARP cache on an interface
```

`ip neigh` is the modern equivalent — same information, consistent syntax
with the rest of the `ip` command family.

---

## Testing connectivity — `ping`

`ping` sends a small packet to a target and measures whether a response
comes back and how long it takes. Uses **ICMP** (Internet Control Message
Protocol).

```bash
ping google.com           # ping until Ctrl+C
ping -c 4 google.com      # send exactly 4 packets then stop
ping 127.0.0.1            # ping yourself — tests networking stack is alive
ping 8.8.8.8              # ping Google's DNS server by IP
```

Output:
```
PING google.com (142.250.80.46): 56 bytes
64 bytes from 142.250.80.46: icmp_seq=0 ttl=115 time=12.4 ms
64 bytes from 142.250.80.46: icmp_seq=1 ttl=115 time=11.8 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
```

| Field | Meaning |
|-------|---------|
| `time=12.4 ms` | Round-trip time — how long the packet took to go and return |
| `ttl=115` | Time to Live — how many router hops the packet can survive |
| `0% packet loss` | All packets arrived — connection is clean |

> **`ping` failing doesn't always mean a host is down.** Many servers and
> firewalls deliberately block ICMP to prevent network mapping. A
> non-response to `ping` is not conclusive.

---

## DNS lookups — `dig`, `nslookup`, `whois`

These commands query DNS (Domain Name System) directly — resolving
hostnames to IPs, checking what DNS servers return, and debugging DNS issues.

### `dig` — the primary DNS lookup tool

```bash
dig google.com                  # full DNS query output
dig google.com +short           # just the IP address(es)
dig google.com MX +short        # look up mail servers (MX records)
dig google.com NS +short        # look up nameservers
dig @8.8.8.8 google.com         # query a specific DNS server (Google's)
```

Output:
```
;; ANSWER SECTION:
google.com.     300    IN    A    142.250.80.46

;; Query time: 8 msec
;; SERVER: 127.0.0.53#53
```

| Field | Meaning |
|-------|---------|
| `A` | Record type — maps a hostname to an IPv4 address |
| `300` | TTL in seconds — how long this answer can be cached |
| `SERVER` | Which DNS server answered the query |

### `nslookup` — simpler alternative

```bash
nslookup google.com
nslookup google.com 8.8.8.8     # query a specific DNS server
```

`dig` gives more detail and control. `nslookup` is quicker for simple
lookups. Both appear in the wild.

### `whois` — domain ownership lookup

```bash
whois example.com               # show domain registration info
```

Useful for investigating who owns a domain and when it was registered —
helpful in DNS troubleshooting and security investigation.

---

## Tracing routes — `traceroute`, `tracepath`

Show every router hop between you and a destination.

### `traceroute`

```bash
traceroute google.com
```

Output:
```
1  10.0.2.1       0.5 ms   ← your default gateway (first hop)
2  192.168.1.1    2.1 ms   ← your ISP's router
3  *  *  *                  ← hop that doesn't respond (firewall)
4  142.250.80.46  12.4 ms  ← destination
```

### `tracepath` — no root required

```bash
tracepath google.com
```

Achieves the same result as `traceroute` without needing root privileges.
Good fallback when `traceroute` isn't available or permission is denied.

> If a server is unreachable, `traceroute`/`tracepath` tells you exactly
> how far packets get before they stop. `* * *` means that hop didn't
> respond — common, not always a problem.

---

## Checking connections & open ports — `ss`, `netstat`

These commands show active network connections and which ports are
listening for incoming traffic.

### `ss` — the modern tool

```bash
ss -tuln                      # show listening TCP/UDP sockets
ss -tulnp                     # same + show which process owns the socket
ss -tun state established     # show only established connections
```

| Flag | Meaning |
|------|---------|
| `-t` | TCP connections |
| `-u` | UDP connections |
| `-l` | Listening sockets only |
| `-n` | Show port numbers, not service names |
| `-p` | Show process using the socket |

Output:
```
Netid  State   Local Address:Port
tcp    LISTEN  0.0.0.0:22         ← SSH listening on all interfaces (port 22)
tcp    LISTEN  127.0.0.1:5432     ← PostgreSQL listening locally only
```

`0.0.0.0` = accessible from outside. `127.0.0.1` = local only.

> The `-p` flag is invaluable — it shows exactly which process is listening
> on a given port, making it easy to track down what's using a port.

### `netstat` — the older equivalent

```bash
netstat -tuln     # same flags, same output style
```

`ss` is the modern replacement and faster, but `netstat` still appears
everywhere. Know both.

---

## Transferring data — `curl`, `wget`

### `curl` — transfer data to/from a URL

```bash
curl https://example.com                                      # print page HTML to screen
curl -o file.html https://example.com                         # save output to a file
curl -I https://example.com                                   # show HTTP headers only
curl -X POST -d '{"key":"value"}' https://api.example.com    # send a POST request
curl -L https://example.com                                   # follow redirects
curl -H "Header: value" URL                                   # add custom headers
curl -s https://api.example.com                               # silent mode (no progress bar)
curl -v https://example.com                                   # verbose output (debugging)
curl --max-time 10 URL                                        # timeout after 10 seconds
```

The Swiss army knife of HTTP from the command line — used constantly for
testing APIs, downloading files, and debugging web requests. `curl -v` is
your best friend when debugging HTTP issues.

### `wget` — download files

```bash
wget https://example.com/file.zip                   # download a file
wget -O output.zip https://example.com/file.zip     # download with a custom filename
wget -q https://example.com/file.zip                # quiet mode, no progress output
wget -r https://example.com                         # recursive download
```

| Tool | Best for |
|------|---------|
| `curl` | API testing, inspecting HTTP responses, sending data |
| `wget` | Downloading files, recursive site downloads |

---

## SSH — connecting to remote machines

**SSH** (Secure Shell) is how you connect to and control a remote Linux
machine securely over a network.

```bash
ssh user@hostname            # connect to a remote machine
ssh user@192.168.1.10        # connect by IP address
ssh -p 2222 user@hostname    # connect on a non-standard port
exit                         # disconnect from the remote session
```

On first connection, SSH asks you to confirm the remote machine's
fingerprint — verifying the server's identity. Type `yes` to accept.

### SSH keys — the right way to authenticate

Passwords work but SSH keys are the standard in practice — more secure,
no typing a password every time.

```bash
ssh-keygen -t ed25519 -C "your@email.com"    # generate a key pair
ssh-copy-id user@hostname                     # copy public key to the remote server
```

Once the public key is on the server, SSH authenticates automatically.

### Key files

| File | Purpose |
|------|---------|
| `~/.ssh/id_ed25519` | Your **private** key — never share this |
| `~/.ssh/id_ed25519.pub` | Your **public** key — goes on remote servers |
| `~/.ssh/known_hosts` | Fingerprints of servers you've connected to before |
| `~/.ssh/config` | Shortcuts for SSH connections |

### `~/.ssh/config` — connection shortcuts

```
Host myserver
    HostName 192.168.1.10
    User codespace
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

With this saved, `ssh myserver` replaces the full command. Essential when
managing multiple servers.

---

## Network service management — `systemctl`

When network changes don't take effect, restarting the networking service
is often the solution.

```bash
systemctl restart networking        # restart networking service
systemctl status NetworkManager     # check NetworkManager status
systemctl restart NetworkManager    # restart NetworkManager
```

> `systemctl` is covered in full in Section 9 — systemd & services.
> This is just the networking-specific use case.

---

## Quick reference

| What you want | Command |
|---------------|---------|
| Show IP addresses | `ip addr` |
| Show interface status | `ip link` |
| Quick IP address(es) | `hostname -I` |
| Show routing table | `ip route` |
| Show default gateway | `ip route show default` |
| Show ARP table | `arp -n` or `ip neigh` |
| Clear ARP cache | `ip neigh flush dev eth0` |
| Test connectivity | `ping -c 4 hostname` |
| DNS lookup (full) | `dig hostname` |
| DNS lookup (quick) | `dig hostname +short` |
| Query specific DNS server | `dig @8.8.8.8 hostname` |
| Domain ownership lookup | `whois domain.com` |
| Trace route to host | `traceroute hostname` |
| Trace route (no root) | `tracepath hostname` |
| Show listening ports | `ss -tuln` |
| Show listening ports + processes | `ss -tulnp` |
| Show established connections | `ss -tun state established` |
| Download/test URL | `curl https://url` |
| Save HTTP response | `curl -o file https://url` |
| Show HTTP headers only | `curl -I https://url` |
| Follow redirects | `curl -L https://url` |
| Verbose HTTP debugging | `curl -v https://url` |
| Download a file | `wget https://url` |
| Connect via SSH | `ssh user@hostname` |
| Generate SSH key pair | `ssh-keygen -t ed25519` |
| Copy public key to server | `ssh-copy-id user@hostname` |
| Restart networking service | `systemctl restart networking` |
| Check NetworkManager status | `systemctl status NetworkManager` |

---

## Key mental models

1. `ip addr` shows interfaces and IPs. `ip link` shows interface status only. `hostname -I` is the fastest way to just see your IPs.
2. `ip route` shows where traffic goes. The default gateway is where all outbound traffic is sent when no specific route matches.
3. ARP maps IPs to MAC addresses on your local network. `ip neigh` is the modern command; `arp -n` is the classic.
4. `ping` tests reachability using ICMP — but a non-response doesn't prove a host is down. Firewalls block ICMP routinely.
5. `dig` is the right tool for DNS debugging. `nslookup` is the simpler alternative. `whois` shows domain ownership.
6. `traceroute`/`tracepath` shows the path packets take hop by hop — used to find exactly where connectivity breaks. `tracepath` requires no root.
7. `ss -tuln` shows what's listening on which ports. `0.0.0.0` = external, `127.0.0.1` = local only. Add `-p` to see which process owns the port.
8. `curl` is for interacting with URLs and APIs. `wget` is for downloading files. `curl -v` is your best debugging tool for HTTP issues.
9. SSH keys are the standard authentication method — private key stays on your machine, public key goes on the server. `~/.ssh/config` saves you from typing long commands.
10. When network changes don't take effect, `systemctl restart networking` or `systemctl restart NetworkManager` often resolves it.