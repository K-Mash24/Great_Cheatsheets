# 🌐 Networking Cheatsheet Directory

A comprehensive collection of networking fundamentals covering models, protocols, packet structures, and port references.

**Last Updated:** May 2026 | **Status:** ✅ Complete

---

## 📁 Contents

| File | Topic | Size | Description |
|------|-------|------|-------------|
| [`01.OSI_Model.md`](#1-osi-model) | OSI Model | 4.2 KB | Seven-layer reference model for network communication |
| [`02.TCP-IP_model.md`](#2-tcpip-model) | TCP/IP Model | 4.1 KB | Practical four-layer model that runs the internet |
| [`03.Packets_encapsulation.md`](#3-packets--encapsulation) | Data Encapsulation | 4.7 KB | How layers wrap data and PDU types at each level |
| [`04.Protocols'-Ports.md`](#4-protocols--ports) | Protocols & Ports | 6.7 KB | Common protocols and well-known port reference |
| [`OSI-TCP\IP model.svg`](#visual-reference) | Visual Diagram | SVG | OSI to TCP/IP layer mapping graphic |

---

## 🎓 Quick Start

### For Beginners
1. Start with **OSI_Model** — understand the 7-layer framework
2. Read **TCP-IP_model** — see how it maps to the real internet
3. Study **Packets_encapsulation** — visualize how data flows
4. Reference **Protocols-Ports** — memorize common ports

### For Quick Lookup
- Need to remember what port HTTP uses? → Check **Protocols-Ports**
- Confused about layers? → Check **OSI_Model** PDU table
- How does data travel? → Check **Packets_encapsulation** diagram

### By Topic

| Need to Know | File |
|--------------|------|
| What are the 7 layers? | `01.OSI_Model.md` |
| How does TCP/IP differ from OSI? | `02.TCP-IP_model.md` |
| How is data packaged? | `03.Packets_encapsulation.md` |
| Port numbers & protocols | `04.Protocols'-Ports.md` |
| Visual layer mapping | `OSI-TCP\IP model.svg` |

---

## 📖 File Descriptions

### 1. OSI Model

**Topic:** Seven-layer reference framework  
**Best for:** Understanding networking theory, exam prep

**Covers:**
- **Layer 7 — Application:** HTTP/HTTPS, FTP, SSH, DNS, SMTP
- **Layer 6 — Presentation:** TLS/SSL, encryption, compression, encoding
- **Layer 5 — Session:** Connection lifecycle, session management
- **Layer 4 — Transport:** TCP, UDP, ports, segments
- **Layer 3 — Network:** IP addresses, routing, packets, ICMP
- **Layer 2 — Data Link:** MAC addresses, frames, Ethernet, ARP
- **Layer 1 — Physical:** Raw bits, cables, signals, hardware

**Key Sections:**
- PDU (Protocol Data Unit) summary table
- Key protocols by layer
- Mnemonic: "All People Seem To Need Data Processing"

**Mnemonic for Layer Names:**
```
Layer 7: Application
Layer 6: Presentation
Layer 5: Session
Layer 4: Transport ⭐
Layer 3: Network ⭐
Layer 2: Data Link
Layer 1: Physical

→ "All People Seem To Need Data Processing"
```

---

### 2. TCP/IP Model

**Topic:** Practical internet model (4 layers)  
**Best for:** Real-world application, how the internet actually works

**Covers:**
- **Layer 4 — Application:** HTTP, HTTPS, DNS, SMTP, FTP, SSH, TLS (combines OSI 7+6+5)
- **Layer 3 — Transport:** TCP, UDP (same as OSI layer 4)
- **Layer 2 — Internet:** IP, ICMP (same as OSI layer 3)
- **Layer 1 — Network Access:** Ethernet, Wi-Fi, ARP, hardware (combines OSI 1+2)

**Key Sections:**
- OSI → TCP/IP mapping visualization
- Why TCP/IP collapses layers
- Key distinctions from OSI model
- Protocol reference table

**Why TCP/IP Differs:**
The TCP/IP model is **practical**, not theoretical. It reflects how modern software actually works:
- Session management and data formatting aren't separate concerns
- Physical and data link are treated as one layer
- The transport layer (TCP/UDP) doesn't change

---

### 3. Packets & Encapsulation

**Topic:** How data is wrapped at each layer  
**Best for:** Understanding data flow, troubleshooting

**Covers:**
- **Core Definitions:**
  - Packet — data unit at Layer 3 (Network)
  - Encapsulation — process of wrapping with headers
  - Decapsulation — reverse process on receiving end
  - PDU — Protocol Data Unit names at each layer
  - FCS — Frame Check Sequence (error detection)

- **Visual Flow:**
  - Sender: How data gets wrapped down the stack
  - Receiver: How headers are stripped up the stack
  - Each layer reads only its own header

**Key Concept — Nested Boxes Analogy:**
```
Data (HTTP request)
  ↓ wrapped in
TCP header (port number)
  ↓ wrapped in
IP header (destination IP)
  ↓ wrapped in
MAC header (next hop)
  ↓ transmitted as
Physical signals (bits)
```

**PDU Reference:**
| Layer | PDU | Name |
|-------|-----|------|
| 7–5 | Data | Application/Presentation/Session |
| 4 | Segment | Transport |
| 3 | Packet | Network |
| 2 | Frame | Data Link |
| 1 | Bit | Physical |

---

### 4. Protocols & Common Ports

**Topic:** Protocol reference and port numbers  
**Best for:** Port memorization, protocol lookup

**Covers:**
- **Port Number Ranges:**
  - 0–1023: Well-known (HTTP, SSH, DNS, etc.)
  - 1024–49151: Registered (databases, apps)
  - 49152–65535: Ephemeral (temporary OS assignments)

- **Protocols by Category:**
  - **Web:** HTTP (80), HTTPS (443), HTTP alt (8080)
  - **Email:** SMTP (25), POP3 (110), IMAP (143), SMTPS (465)
  - **Infrastructure:** DNS (53), DHCP (67/68), MySQL (3306), PostgreSQL (5432)
  - **File Transfer:** FTP (20/21)
  - **Security:** SSH (22), Telnet (23), RDP (3389)

- **Critical Distinctions:**
  - HTTP (80) = unencrypted; HTTPS (443) = encrypted with TLS
  - SSH (22) = encrypted; Telnet (23) = plain text (never use!)
  - POP3 = download & delete; IMAP = read & leave on server
  - DNS uses both TCP and UDP
  - FTP requires TWO ports (21 command, 20 data)
  - DHCP uses UDP (client has no IP yet)

**Full Port Reference Table:**
Complete sortable table of all 18 essential ports for exam prep

---

### Visual Reference

**File:** `OSI-TCP\IP model.svg`

A visual diagram showing:
- How OSI layers map to TCP/IP layers
- Protocol examples at each layer
- Layer relationships and dependencies

---

## 🔑 Key Concepts to Remember

### PDU Names (Very Important!)
- Layer 7–5: **Data**
- Layer 4: **Segment**
- Layer 3: **Packet**
- Layer 2: **Frame**
- Layer 1: **Bit**

### Port Memorization Strategy

**Essential 18 Ports (Must Know):**
```
20   FTP data          |  80   HTTP
21   FTP control       |  443  HTTPS
22   SSH               |  3389 RDP
23   Telnet            |  3306 MySQL
25   SMTP              |  5432 PostgreSQL
53   DNS               |  8080 HTTP alt
67   DHCP server       |
68   DHCP client       |  110  POP3
                       |  143  IMAP
                       |  465  SMTPS
```

**Memory Tricks:**
- SSH = 22 (even number, secure)
- Telnet = 23 (odd number, insecure)
- SMTP = 25 (for sending mail)
- DNS = 53 (for name queries)
- HTTP = 80 (easy: 80 for web)
- HTTPS = 443 (harder: remember it's secure)

### OSI Layer Priorities (for SAA)

⭐ **Know These Well:**
- **Layer 4 (Transport):** TCP/UDP, ports, segments
- **Layer 3 (Network):** IP addresses, routing, packets

They're where most networking happens.

---

## 🧠 Learning Path

### Day 1: Foundation
1. Read **OSI_Model** intro + layer definitions
2. Review PDU names 5 times
3. Understand the 7 layers conceptually

### Day 2: Practical Model
1. Read **TCP-IP_model** section
2. Understand why layers are merged
3. Map OSI → TCP/IP mentally

### Day 3: Data Flow
1. Study **Packets_encapsulation** encapsulation diagram
2. Trace data from sender to receiver
3. Understand why each header matters

### Day 4: Protocols & Ports
1. Read **Protocols-Ports** by category
2. Memorize the 18 essential ports
3. Understand port ranges and use cases

### Day 5: Review & Practice
1. Review all PDU names
2. Memorize all 18 ports
3. Explain the OSI model to someone else

---

## 📊 Comparison Tables

### OSI vs TCP/IP

| Aspect | OSI | TCP/IP |
|--------|-----|--------|
| **Layers** | 7 | 4 |
| **Purpose** | Reference/teaching | Real-world working model |
| **Development** | Theoretical | Practical (internet standard) |
| **Transport** | Layer 4 | Layer 3 |
| **Internet** | Layer 3 | Layer 2 |
| **Physical** | Layers 1–2 | Layer 1 |

### When to Use Each Model

**Use OSI When:**
- Teaching networking fundamentals
- Troubleshooting (identify which layer is failing)
- Exam prep (certifications love OSI)

**Use TCP/IP When:**
- Actual network implementation
- Internet standards
- Understanding real-world protocols

---

## ✅ Common Exam Topics

### Top 10 Things to Know

1. **7 OSI Layers** — memorize order + names
2. **PDU Names** — Data, Segment, Packet, Frame, Bit
3. **4 TCP/IP Layers** — how they map to OSI
4. **Encapsulation** — how headers wrap data
5. **18 Port Numbers** — HTTP, HTTPS, SSH, DNS, FTP, SMTP, POP3, IMAP, MySQL, etc.
6. **Layer 4 Protocols** — TCP vs UDP differences
7. **IP Addressing** — Layer 3 responsibility
8. **MAC Addresses** — Layer 2 responsibility
9. **Encryption** — where TLS/SSL operates (Layer 6)
10. **Routing** — how Layer 3 forwards packets

---

## 🔗 Related Topics to Study Next

- **DNS in Depth** — Domain Name System (Layer 7/Application)
- **TCP vs UDP** — when to use each
- **IP Subnetting** — dividing networks
- **Network Troubleshooting** — ping, tracert, netstat
- **Firewalls & ACLs** — access control at Layers 3–4
- **VLANs** — virtual networks at Layer 2

---

## 💡 Pro Tips

1. **Draw the OSI Model** — sketch 7 boxes regularly to reinforce memory
2. **Practice Encapsulation** — trace a packet from browser to server
3. **Port Association** — link protocols to numbers (HTTP→80, SSH→22)
4. **Layer Responsibilities** — remember what each layer does
5. **Real-World Application** — apply concepts to your own internet usage

---

> **Remember:** The OSI model is theoretical and helps us understand networking. TCP/IP is what actually runs the internet. Both are important!

---

**Python Version:** N/A  
**Created:** May 2026  
**Difficulty Level:** Beginner to Intermediate
