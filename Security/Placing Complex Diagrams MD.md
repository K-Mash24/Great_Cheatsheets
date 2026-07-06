# Placing Complex Diagrams in GitHub Markdown Files

A practical guide to creating Mermaid diagrams that render correctly on GitHub.

---

## Table of Contents

1. [The Core Problem](#the-core-problem)
2. [The Golden Rules](#the-golden-rules)
3. [Diagram Templates](#diagram-templates)
   - [Symmetric Encryption Flow](#symmetric-encryption-flow)
   - [Asymmetric Encryption Flow](#asymmetric-encryption-flow)
   - [Hybrid Cryptosystem Flow](#hybrid-cryptosystem-flow)
   - [Forward Secrecy Comparison](#forward-secrecy-comparison)
4. [Common Error Messages & Solutions](#common-error-messages--solutions)
5. [Testing Your Diagrams](#testing-your-diagrams)
6. [GitHub Mermaid Version Check](#github-mermaid-version-check)
7. [Template for New Diagrams](#template-for-new-diagrams)

---

## The Core Problem

GitHub uses Mermaid to render diagrams from Markdown code blocks. However, Mermaid's parser is **strict** about syntax. The most common errors come from:

| Issue                    | Example                        | Why It Fails                                |
| ------------------------ | ------------------------------ | ------------------------------------------- |
| **Unquoted labels**      | `Server[Server (Bob)]`         | Parentheses confuse the parser              |
| **Nested quotes**        | `A[Plaintext: "4111"]`         | The `"` inside the label breaks the parser  |
| **Colons in labels**     | `A[Plaintext: "4111"]`         | Colons are interpreted as link syntax       |
| **Inline styling**       | `style EV fill:#ffcccc`        | `style` is fragile; `classDef` is preferred |
| **Missing arrow syntax** | `A -> B` (should be `A --> B`) | Incorrect arrow type                        |

---

## The Golden Rules

To make Mermaid diagrams work reliably on GitHub:

### Rule 1: Quote Everything with Special Characters

```mermaid
✅ subgraph Server["Server (Bob)"]
✅ A["Plaintext: '4111'"]
✅ Eaves["Eavesdropper: ❌ Cannot decrypt"]
```

### Rule 2: Use `classDef` Instead of `style`

```mermaid
✅ classDef warning fill:#ffcccc,stroke:#cc0000
✅ class Eaves warning

❌ style Eaves fill:#ffcccc,stroke:#cc0000
```

### Rule 3: Use Single Quotes Inside Double-Quoted Labels

```mermaid
✅ A["Plaintext: '4111'"]
✅ Message["Alice said: 'Hello'"]
```

### Rule 4: Keep Subgraph Names Explicit

```mermaid
✅ subgraph Alice["Alice (Customer)"]
✅ subgraph Network["Network"]

❌ subgraph Alice[Alice (Customer)]
```

### Rule 5: Use Proper Arrow Syntax

| Arrow  | Meaning      | Use Case                        |
| ------ | ------------ | ------------------------------- |
| `-->`  | Solid arrow  | Data flow, direct connection    |
| `-.->` | Dashed arrow | Indirect or optional connection |
| `==>`  | Thick arrow  | Emphasis or critical path       |

---

## Diagram Templates

### Symmetric Encryption Flow

```mermaid
flowchart LR
    subgraph Alice["Alice"]
        A["Plaintext: '4111'"]
        K1["Shared Key: K"]
        E["Encrypt AES"]
    end

    subgraph Network["Network"]
        C["Ciphertext: '9f2a...'"]
        EV["Eavesdropper sees gibberish"]
    end

    subgraph Bob["Bob"]
        D["Decrypt AES"]
        B["Plaintext: '4111'"]
        K2["Shared Key: K"]
    end

    A --> E
    K1 --> E
    E --> C
    C --> D
    K2 --> D
    D --> B
    C -.-> EV

    classDef eavesdrop fill:#ffcccc,stroke:#cc0000
    class EV eavesdrop
```

---

### Asymmetric Encryption Flow

```mermaid
flowchart LR
    subgraph Server["Server (Bob)"]
        Gen["Generate Key Pair"]
        PubKey["Public Key"]
        PrivKey["Private Key"]
        Decrypt["Decrypt RSA"]
        Plain1["Plaintext: '4111'"]
    end

    subgraph Alice["Alice (Customer)"]
        Encrypt["Encrypt RSA"]
        Plain2["Plaintext: '4111'"]
        Cipher["Ciphertext: '9f2a...'"]
    end

    subgraph Network["Network"]
        PubKeySent["Public Key"]
        CipherSent["Ciphertext: '9f2a...'"]
        Eaves["Eavesdropper: Has public key + ciphertext ❌ Cannot decrypt"]
    end

    Gen --> PubKey
    Gen --> PrivKey
    PubKey --> PubKeySent
    PubKeySent --> Alice
    Plain2 --> Encrypt
    PubKeySent --> Encrypt
    Encrypt --> Cipher
    Cipher --> CipherSent
    CipherSent --> Server
    CipherSent --> Eaves
    Cipher --> Decrypt
    PrivKey --> Decrypt
    Decrypt --> Plain1

    classDef eavesdrop fill:#ffcccc,stroke:#cc0000
    class Eaves eavesdrop
```

---

### Hybrid Cryptosystem Flow (Sequence Diagram)

```mermaid
sequenceDiagram
    participant Client as Client (Alice)
    participant Network as Network
    participant Server as Server (Bob)

    Note over Client,Server: Phase 1: Asymmetric Key Exchange

    Server->>Server: Generate RSA key pair<br/>(public + private)
    Server->>Client: Send public key
    Client->>Client: Generate random session key (Ks)
    Client->>Server: Encrypt Ks with server's public key
    Server->>Server: Decrypt Ks with private key

    Note over Client,Server: Phase 2: Symmetric Bulk Encryption

    loop Secure Session
        Client->>Server: Encrypt all data with Ks (AES)
        Server->>Client: Encrypt all responses with Ks (AES)
    end

    Note over Client,Server: Phase 3: Session Ends

    Client->>Client: Discard Ks
    Server->>Server: Discard Ks

    Note over Network: Eavesdropper recorded everything.<br/>Cannot decrypt: Ks was never transmitted in plaintext.
```

---

### Forward Secrecy Comparison

```mermaid
flowchart LR
    subgraph Attack["The Problem"]
        direction LR
        A["Attacker records<br/>encrypted session today"] --> B["Attacker steals<br/>private key later"]
        B --> C["Attacker decrypts<br/>ALL past sessions"]
    end

    subgraph Solution["Forward Secrecy"]
        direction LR
        D["Each session uses<br/>unique ephemeral key"] --> E["Session key<br/>discarded after use"]
        E --> F["Private key stolen later<br/>CANNOT decrypt past sessions"]
    end

    classDef attack fill:#ffcccc,stroke:#cc0000
    classDef solution fill:#ccffcc,stroke:#00cc00

    class Attack attack
    class Solution solution
```

---

## Common Error Messages & Solutions

| Error Message                                      | Likely Cause                      | Solution                                                   |
| -------------------------------------------------- | --------------------------------- | ---------------------------------------------------------- |
| `Expecting 'SGE', 'DOUBLECIRCLEEND', ... got 'PS'` | Parentheses in subgraph name      | Quote the subgraph: `subgraph Name["Name (with parens)"]`  |
| `Parse error on line X`                            | Unquoted label with special chars | Quote the node: `Node["Label with 'quotes' and : colons"]` |
| `Unknown diagram type`                             | Wrong flowchart type              | Use `flowchart LR` or `sequenceDiagram` at the top         |
| `style EV` not applied                             | Inline style syntax error         | Use `classDef` + `class` instead                           |
| `Empty diagram`                                    | Missing or broken syntax          | Check for missing arrows or incorrect syntax               |

---

## Testing Your Diagrams

### Method 1: GitHub Preview

1. Create a test file in your repository (e.g., `test-diagram.md`)
2. Paste your Mermaid code block
3. View it rendered on GitHub (not in the editor)

### Method 2: Use `info` Diagram

Check the Mermaid version and basic rendering:

````markdown
```mermaid
  info
```
````

### Method 3: Isolate the Problem

If a complex diagram fails:

1. Simplify: remove styling, subgraphs, and formatting
2. Test the minimal version
3. Add complexity back gradually

---

## GitHub Mermaid Version Check

To see the Mermaid version GitHub is using:

````markdown
```mermaid
  info
```
````

This renders as a small info card with the version number. If you're using a feature from a newer version than GitHub supports, it won't render.

---

## Template for New Diagrams

Copy this template when creating a new diagram:

````markdown
```mermaid
flowchart LR
    %% ============================================================
    %% 1. Define your subgraphs (groups of related nodes)
    %% ============================================================
    subgraph FirstGroup["First Group Name"]
        A["Node A with 'quotes'"]
        B["Node B with : colon"]
    end

    subgraph SecondGroup["Second Group Name"]
        C["Node C"]
        D["Node D"]
    end

    %% ============================================================
    %% 2. Define your nodes (individual elements)
    %% ============================================================
    E["External Node"]
    F["Important Node"]

    %% ============================================================
    %% 3. Define your connections (arrows)
    %% ============================================================
    A --> B
    B --> E
    C --> E
    D --> F
    E -.-> F

    %% ============================================================
    %% 4. Define your styling (classDefs)
    %% ============================================================
    classDef important fill:#ccffcc,stroke:#00cc00
    classDef warning fill:#ffcccc,stroke:#cc0000

    class F important
    class E warning
```
````

---

## Quick Reference Card

| Element              | Syntax                                  | Example                                        |
| -------------------- | --------------------------------------- | ---------------------------------------------- |
| Subgraph             | `subgraph Name["Label"]`                | `subgraph Server["Server (Bob)"]`              |
| Node                 | `ID["Label with 'quotes'"]`             | `A["Plaintext: '4111'"]`                       |
| Solid arrow          | `A --> B`                               | `PubKey --> Encrypt`                           |
| Dashed arrow         | `A -.-> B`                              | `C -.-> EV`                                    |
| Styling class        | `classDef name fill:color,stroke:color` | `classDef warning fill:#ffcccc,stroke:#cc0000` |
| Apply class          | `class ID className`                    | `class EV eavesdrop`                           |
| Sequence participant | `participant Name as Alias`             | `participant Client as Client (Alice)`         |
| Sequence note        | `Note over A,B: Text`                   | `Note over Client,Server: Phase 1`             |

---

**Last Updated:** 2026
