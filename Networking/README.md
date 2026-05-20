# Pillar 1 — Networking Fundamentals

## Purpose

This pillar builds genuine networking foundations from first principles before
touching any cloud infrastructure or AWS services. Networking underpins every
system you will design, operate, and troubleshoot as a Solutions Architect and
DevOps engineer — understanding it deeply, not superficially, is the goal.

Every concept here was studied independently of cloud tooling. The knowledge
transfers directly to AWS (VPCs, subnets, route tables, security groups, DNS,
load balancers) and to the full DevOps roadmap (service discovery, container
networking, Kubernetes networking, infrastructure as code).

---

## Learning objectives

By completing this pillar you should be able to:

- Explain the OSI and TCP/IP models from memory and identify which protocols
  and devices operate at each layer
- Read and write IPv4 addresses in both decimal and binary, and identify
  address classes, private ranges, and special addresses
- Perform subnetting calculations by hand — network address, broadcast
  address, usable host range, and host count — for any given CIDR block
- Design a VLSM addressing scheme for a network with mixed host requirements
- Explain how routers forward packets using routing tables and longest prefix
  match, and how switches use MAC address tables for local delivery
- Describe how NAT and PAT allow private networks to share a public IP address
- Trace a DNS query from browser cache through recursive resolver, root server,
  TLD server, and authoritative name server to final answer
- Differentiate TCP and UDP, explain the three-way handshake, and identify
  appropriate use cases for each protocol
- Define stateless and stateful firewalls, explain ACL rule evaluation, and
  describe network zone design including the DMZ
- Identify common network attacks (SYN flood, ARP spoofing, MITM, DDoS) and
  explain the mechanism behind each

---

## Files in this pillar

| File                          | Topic                          | Section |
|-------------------------------|--------------------------------|---------|
| `01-osi-model.md`             | OSI model — all seven layers   | 1       |
| `02-tcpip-model.md`           | TCP/IP model and OSI mapping   | 1       |
| `03-packets-encapsulation.md` | Packets and encapsulation      | 1       |
| `04-protocols-ports.md`       | Protocols and port numbers     | 1       |
| `05-ip-addressing.md`         | IPv4 structure, binary, IPv6   | 2       |
| `06-subnetting-cidr.md`       | Subnetting, CIDR, VLSM         | 3       |
| `07-routing-switching.md`     | Routing, switching, NAT, PAT   | 4       |
| `08-dns.md`                   | DNS hierarchy and resolution   | 5       |
| `09-tcp-udp.md`               | TCP, UDP, sockets, flow control| 6       |
| `10-network-security.md`      | Firewalls, ACLs, attacks       | 7       |

---

## Progress checklist

### Section 1 — How the internet is structured
- [x] OSI model (layers 3, 4, and 7 are priority)
- [x] TCP/IP model and how it maps to OSI
- [x] What a packet is and encapsulation
- [x] Protocols and common port numbers

### Section 2 — IP addressing
- [x] IPv4 address structure (32-bit, 4 octets)
- [x] Binary and decimal conversion
- [x] Public vs private IP ranges (RFC 1918)
- [x] Special addresses (loopback, broadcast, APIPA)
- [x] IPv6 basics

### Section 3 — Subnetting and CIDR
- [x] What a subnet is
- [x] Subnet masks
- [x] CIDR notation
- [x] Network and broadcast addresses
- [x] Calculating host counts
- [x] Subnetting by hand
- [x] VLSM (variable length subnet masking)
- [x] Supernetting and route summarisation

### Section 4 — Routing and switching
- [x] What a router does vs a switch
- [x] Routing tables
- [x] Default gateway
- [x] Static vs dynamic routing
- [x] NAT and PAT
- [x] Switches, MAC addresses, and ARP

### Section 5 — DNS
- [x] What DNS does
- [x] DNS hierarchy (root → TLD → authoritative)
- [x] DNS record types (A, AAAA, CNAME, MX, NS, TXT)
- [x] DNS resolution walkthrough
- [x] Practical DNS tools (dig, nslookup)

### Section 6 — Transport layer (TCP and UDP)
- [x] TCP — reliable delivery and 3-way handshake
- [x] UDP — connectionless, when to use it
- [x] TCP vs UDP use cases
- [x] Ports and sockets
- [x] TCP flow control and congestion

### Section 7 — Network security basics
- [x] Firewalls — stateless vs stateful
- [x] Access control lists (ACLs)
- [x] Network zones and DMZ
- [x] Common network layer attacks
- [x] Wireshark basics

---

## Key concepts to revise before moving on

The following are the highest-yield concepts from this pillar — revisit these
before beginning Pillar 2 or sitting the SAA exam:

- **OSI layers 3, 4, 7** — know the protocols at each layer cold
- **Subnetting by hand** — given any CIDR block, calculate network address,
  broadcast address, usable range, and host count without assistance
- **VLSM** — allocate subnets of different sizes from a single address space
- **TCP three-way handshake** — SYN, SYN-ACK, ACK and what each step achieves
- **DNS resolution** — the full path from browser cache to authoritative server
- **NAT/PAT** — how private addresses share a single public IP using port numbers
- **Stateful vs stateless firewall** — the difference and why it matters
- **RFC 1918 ranges** — `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`

---

## Labs and scripts

| Path                               | Contents                            |
|------------------------------------|-------------------------------------|
| `labs/subnet-practice.md`          | Subnetting worked problems          |
| `labs/dns-dig-walkthrough.md`      | Terminal session — dig and nslookup |
| `labs/wireshark-observations.md`   | Wireshark capture notes             |
| `scripts/subnet_calc.py`           | Subnet calculator script            |

---

## Commit history for this pillar

```
networking: add OSI model notes (section 1)
networking: add TCP/IP model notes (section 1)
networking: add packets and encapsulation notes (section 1)
networking: add protocols and port numbers notes (section 1)
networking: add IP addressing notes (section 2)
networking: add subnetting and CIDR notes (section 3)
networking: add routing and switching notes (section 4)
networking: add DNS notes (section 5)
networking: add TCP and UDP notes (section 6)
networking: add network security basics notes (section 7)
```

---

## What comes next

**Pillar 2 — Linux and CLI proficiency**

The networking foundations built here connect directly to Linux. You will use
the command line to inspect network interfaces (`ip addr`, `ifconfig`), trace
routes (`traceroute`), query DNS (`dig`, `nslookup`), analyse traffic
(Wireshark, `tcpdump`), and configure firewall rules (`iptables`, `ufw`).
Linux is where the theory becomes hands-on.
