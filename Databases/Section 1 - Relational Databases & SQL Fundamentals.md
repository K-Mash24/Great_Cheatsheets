# Pillar 5 — Databases & Storage

## Section 1: Relational Databases & SQL Fundamentals

### Section Checklist

- [x] What a database is and why it exists
- [x] The relational model (tables, rows, columns, data types)
- [x] Primary keys — purpose and properties
- [x] SQL command families (DDL, DML, DQL, DCL)
- [x] CREATE TABLE syntax
- [x] INSERT syntax
- [x] SELECT syntax and core clauses (WHERE, ORDER BY, LIMIT)
- [x] Hands-on SQLite practice in Codespace
- [x] DevOps connection noted

---

### 1.1 What is a Database, Really?

A database is **organized, persistent storage** — a system that keeps data on disk (so it survives a restart) and lets you retrieve, add, change, or delete it in controlled ways.

You could store data in a plain text file, but databases solve three problems text files don't:

1. **Structure** — enforced schema (a defined shape for the data), instead of freeform text.
2. **Concurrency** — many users/programs reading and writing at once, safely, without corrupting data.
3. **Querying** — asking complex questions ("all orders over $50 from Nairobi customers") without custom parsing code.

**Concrete example of the concurrency problem:**

If two users update the same text file simultaneously, one update overwrites the other. If User A reads a balance, User B updates it, then User A writes back the old value, the update is lost. Databases solve this with **transactions** (covered in Section 5).

**Concrete example of the querying problem:**

A CSV file with 10,000 customer rows. To find "all customers in Nairobi who joined after 2020", you'd need to write custom Python code to parse and filter. A database does the same with a single line of SQL.

---

### 1.2 The Relational Model

A **relational database** organizes data into **tables** (aka relations):

- **Row** = one record (one instance of a thing).
- **Column** = one attribute (a property every record has).
- Each column has an enforced **data type** (integer, text, date, boolean, etc.).

```mermaid
graph TD
    A[Table: customers] --> B[Row: one customer record]
    A --> C[Column: customer_id - integer]
    A --> D[Column: name - text]
    A --> E[Column: email - text]
    B --> F["Row = 1, Keith, keith@email.com"]
```

**Example — `customers` table:**

| customer_id | name  | email           |
| ----------- | ----- | --------------- |
| 1           | Keith | keith@email.com |
| 2           | Amara | amara@email.com |

**Common SQLite data types:**

| Type | Description | Example |
|------|-------------|---------|
| `INTEGER` | Whole numbers | `42`, `-5`, `0` |
| `TEXT` | Strings | `"Keith"`, `"hello"` |
| `REAL` | Decimal numbers | `3.14`, `-0.5` |
| `BLOB` | Binary data | Images, files |
| `NULL` | Missing/unknown value | `NULL` |

---

### 1.3 The Primary Key

A **primary key (PK)** is a column (or set of columns) that **uniquely identifies each row**. Rules:

- Must be unique across all rows.
- Can never be null (empty).

**Why not use "name" as a key?**
- Names collide (two people named Keith).
- Names can change (legal name change).
- Names can be blank.

A good primary key is **stable, unique, and never changes** — which is why systems typically use auto-incrementing integers or generated IDs instead of "real world" data.

**Foreign key teaser** (covered in Section 2): A **foreign key** is a column that references the primary key of another table. It's how tables are connected — e.g., `orders.customer_id` references `customers.customer_id`.

---

### 1.4 SQL — Structured Query Language

**SQL (Structured Query Language)** is used to communicate with a relational database. It is **declarative** — you describe _what_ you want, not _how_ to retrieve it.

| Family                           | Purpose                 | Example commands                            |
| -------------------------------- | ----------------------- | ------------------------------------------- |
| DDL — Data Definition Language   | Define/change structure | `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` |
| DML — Data Manipulation Language | Change data             | `INSERT`, `UPDATE`, `DELETE`                |
| DQL — Data Query Language        | Read data               | `SELECT`                                    |
| DCL — Data Control Language      | Permissions             | `GRANT`, `REVOKE`                           |

**Brief examples:**
- **DDL:** `CREATE TABLE customers (id INTEGER, name TEXT);`
- **DML:** `INSERT INTO customers VALUES (1, 'Keith');`
- **DQL:** `SELECT * FROM customers;`
- **DCL:** `GRANT SELECT ON customers TO read_only_user;`

---

### 1.5 Creating a Table (DDL)

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);
```

- `customer_id INTEGER PRIMARY KEY` — integer column, uniquely identifies each row.
- `name TEXT NOT NULL` — text column, cannot be left empty.
- `email TEXT UNIQUE` — text column, no two rows may share a value.

> **⚠️ Callout — NOT NULL vs UNIQUE vs PRIMARY KEY**
>
> - `NOT NULL` — value required, duplicates allowed.
> - `UNIQUE` — duplicates forbidden, empty/null generally allowed.
> - `PRIMARY KEY` — required **and** unique, combined. Every table should have exactly one.

---

### 1.6 Inserting Data (DML)

```sql
INSERT INTO customers (customer_id, name, email)
VALUES (1, 'Keith', 'keith@email.com');
```

**If you insert without specifying columns:**

```sql
INSERT INTO customers VALUES (2, 'Amara', 'amara@email.com');
```

This works only if the order matches the table's column order exactly. **Explicitly naming columns is safer and more readable.**

---

### 1.7 Querying Data (DQL) — `SELECT`

```sql
SELECT name, email
FROM customers
WHERE customer_id = 1;
```

Reads as: "Select the `name` and `email` columns, from the `customers` table, where `customer_id` equals 1."

| Clause     | Purpose       | Example                 |
| ---------- | ------------- | ----------------------- |
| `SELECT`   | which columns | `SELECT name, email`    |
| `FROM`     | which table   | `FROM customers`        |
| `WHERE`    | filter rows   | `WHERE customer_id = 1` |
| `ORDER BY` | sort results  | `ORDER BY name ASC`     |
| `LIMIT`    | cap row count | `LIMIT 10`              |

**`SELECT *`** = all columns. Fine for exploring, but real applications should name only needed columns.

**`ORDER BY` examples:**

```sql
-- Ascending (default)
SELECT * FROM customers ORDER BY name;

-- Descending
SELECT * FROM customers ORDER BY name DESC;

-- Multiple columns
SELECT * FROM customers ORDER BY name ASC, customer_id DESC;
```

**`LIMIT` example:**

```sql
SELECT * FROM customers LIMIT 5;  -- only returns 5 rows
```

---

### 1.8 Hands-On Practice (Codespace Terminal)

SQLite is a full relational database engine in a single file — no server setup needed.

```bash
# Check installation
sqlite3 --version

# Create and open a new database file
sqlite3 practice.db
```

Inside the `sqlite3` prompt:

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

INSERT INTO customers (customer_id, name, email)
VALUES (1, 'Keith', 'keith@email.com');

INSERT INTO customers (customer_id, name, email)
VALUES (2, 'Amara', 'amara@email.com');

SELECT * FROM customers;
```

#### Progressive Exercises

1. Insert a third customer of your choice.
2. Select only the `name` column for all customers.
3. Select the customer where `customer_id = 2`.
4. Try inserting a customer with a `NULL` name — what happens?
5. Try inserting two customers with the same email — what happens?
6. Use `ORDER BY name DESC` to sort customers in reverse alphabetical order.
7. Use `LIMIT 1` to select just the first customer in the table.

<details>
<summary>Answers</summary>

```sql
-- 1
INSERT INTO customers (customer_id, name, email) VALUES (3, 'Zainab', 'zainab@email.com');

-- 2
SELECT name FROM customers;

-- 3
SELECT * FROM customers WHERE customer_id = 2;

-- 4 — ERROR: "NOT NULL constraint failed: customers.name"
INSERT INTO customers (customer_id, name, email) VALUES (4, NULL, 'test@email.com');

-- 5 — ERROR: "UNIQUE constraint failed: customers.email"
INSERT INTO customers (customer_id, name, email) VALUES (5, 'Test', 'keith@email.com');

-- 6
SELECT * FROM customers ORDER BY name DESC;

-- 7
SELECT * FROM customers LIMIT 1;
```

</details>

Exit with `.quit`.

---

### 1.9 DevOps Connection

Almost every deployed application — web apps, APIs, CI/CD metadata stores — sits on a relational database. Understanding schemas and constraints here directly prepares for:

- **Schema migrations** — tools like Alembic, Flyway, or Liquibase manage database changes alongside application code.
- **Application configuration** — database connection strings, pooling settings, and timeouts are standard CI/CD variables.
- **Infrastructure as Code** — Terraform and CloudFormation often provision managed databases (RDS, Cloud SQL) with schema definitions.

---

**Next section:** Section 2 — Joins & Relationships