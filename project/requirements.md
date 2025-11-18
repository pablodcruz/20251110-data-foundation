# 🧱 The Data Ingestion Subsystem

## Application Overview

The **Data Ingestion Subsystem** is designed to collect and organize data from different sources into a unified, structured environment.
It is a foundational component of modern data engineering pipelines, responsible for ensuring data is **accurate, clean, and reliable** before downstream analytics or machine learning use.

This subsystem uses **Python** and **PostgreSQL** to read, validate, clean, and load data for later use in analytics or warehousing.

---

## 🎯 Functional Goals

The system will:

* Read data from 1 or multiple sources — such as **CSV**, **JSON**, or simple **APIs**.
* Validate that data conforms to the expected structure and format.
* Clean and standardize the data (handle missing or invalid values).
* Remove duplicates before insertion.
* Load validated data into PostgreSQL staging tables.
* Keep logs and reports for each ingestion run, including any rejected records.

---

## 🧩 Core Functional Scope (User Stories)

As a **data engineer**, I want to:

1. Read data from different sources (CSV, JSON, API).
2. Validate the data format and structure.
3. Clean and standardize columns and values.
4. Remove duplicate records based on primary keys.
5. Load the cleaned data into PostgreSQL tables.
6. Keep track of all rejected or invalid records for later inspection.

---

## 🗄️ Example Main Database Tables

| Table Name        | Purpose                                |
| ----------------- | -------------------------------------- |
| **stg_sales**     | Stores sales transaction data.         |
| **stg_customers** | Stores customer details.               |
| **stg_rejects**   | Stores records that failed validation. |

---

## ⚙️ Standard Functional Scope

The application will:

1. Be written in **Python** and connect to a **PostgreSQL** database.
2. Use **configuration files** (YAML or JSON) to define data sources, schemas, and rules.
3. Handle errors gracefully, continuing with valid records even if some fail.
4. Allow new data sources to be added without major code changes.
5. Log every step of the ingestion for auditing and debugging.

---

## ✅ Definition of Done

The **Data Ingestion Subsystem** will be considered complete when:

* It can successfully read and load data from a source (CSV, API, JSON, PDF etc) files into PostgreSQL.
* At least **80% of the code is covered by PyTest**.
* Database connections are safely opened and closed.
* (optional) All rejected rows are logged with reasons in `stg_rejects`.
* The final demo and code repository are available for review.

---

## 🧱 Non-Functional Expectations

* Design must be **simple, modular, and maintainable**.
* Code follows **PEP 8** and standard naming conventions.
* Use **parameterized queries** to prevent SQL injection.
* Configuration and credentials stored securely (e.g., `.env`).
* All code and logs version-controlled with Git.

---

## 🧭 System Architecture Overview

**Data Flow:**

```
Source (CSV/JSON/API)
    ↓
Reader Layer (pandas)
    ↓
Validation & Cleaning
    ↓
Duplicate Removal
    ↓
PostgreSQL Loader (UPSERT)
    ↓
Rejects Table + Structured Logs
```

**Core Layers:**

| Layer         | Responsibility                                                |
| ------------- | ------------------------------------------------------------- |
| **Reader**    | Reads CSV, JSON, or API data into memory (pandas DataFrame).  |
| **Validator** | Ensures schema conformity, checks nulls, enforces data rules. |
| **Cleaner**   | Fixes or drops invalid data, normalizes column names.         |
| **Loader**    | Loads valid data into staging tables using batch UPSERT.      |
| **Logger**    | Captures structured logs and rejects with detailed reasons.   |

---

## 📁 Optional, but Recommended Folder Structure

```
ingestion/
  src/
    config.py
    readers/ (csv_reader.py, json_reader.py, api_reader.py)
    validate.py
    clean.py
    load.py
    rules.py
    main.py
  config/
    sources.yml
  data/
    customers.csv
    sales.json
  tests/
    test_validate.py
    test_load.py
  requirements.txt
  README.md
```

---

## ⚙️ Example Configuration File (YAML)

This configuration file defines all ingestion sources and validation rules.

```yaml
# config/sources.yml
defaults:
  db_url: postgresql+psycopg://user:pass@localhost:5432/ingest_db
  batch_size: 5000
  on_conflict: upsert           # options: append | upsert | fail

sources:
  - name: customers_csv
    type: csv
    path: data/customers.csv
    target_table: stg_customers
    pk: [customer_id]
    schema:
      customer_id: int
      first_name: str
      last_name: str
      email: str
      created_at: datetime
    rules:
      - rule: "email LIKE '%@%'"
      - rule: "created_at NOT NULL"
      - rule: "len(first_name) > 0"

  - name: sales_json
    type: json
    path: data/sales.json
    target_table: stg_sales
    pk: [sale_id]
    schema:
      sale_id: int
      customer_id: int
      amount: float
      currency: str
      ts: datetime
    rules:
      - rule: "amount >= 0"
      - rule: "currency IN ('USD','EUR','CAD')"
```

---

## 🗃️ Example Database Design

### Staging Tables

```sql
CREATE TABLE IF NOT EXISTS stg_customers (
  customer_id   BIGINT PRIMARY KEY,
  first_name    TEXT NOT NULL,
  last_name     TEXT NOT NULL,
  email         TEXT,
  created_at    TIMESTAMP,
  _loaded_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stg_sales (
  sale_id       BIGINT PRIMARY KEY,
  customer_id   BIGINT NOT NULL,
  amount        NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
  currency      TEXT NOT NULL,
  ts            TIMESTAMP NOT NULL,
  _loaded_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  FOREIGN KEY (customer_id) REFERENCES stg_customers(customer_id)
);

CREATE TABLE IF NOT EXISTS stg_rejects (
  source_name   TEXT NOT NULL,
  raw_payload   JSONB NOT NULL,
  reason        TEXT NOT NULL,
  rejected_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## 🔄 Loading Strategy

To ensure **idempotency**, the loader uses an **UPSERT** pattern:
* The upsert pattern is a database operation that combines insert and update functionality, allowing a new record to be inserted if it does not exist, or an existing record to be updated if it does.

```sql
INSERT INTO stg_sales (sale_id, customer_id, amount, currency, ts)
VALUES (:sale_id, :customer_id, :amount, :currency, :ts)
ON CONFLICT (sale_id) DO UPDATE
SET customer_id = EXCLUDED.customer_id,
    amount      = EXCLUDED.amount,
    currency    = EXCLUDED.currency,
    ts          = EXCLUDED.ts;
```

---

## 🧹 Validation & Cleaning Rules

| Step                | Action                                                      |
| ------------------- | ----------------------------------------------------------- |
| **Type Casting**    | Convert columns to schema types; drop rows that can’t cast. |
| **Required Fields** | Drop rows missing critical values.                          |
| **Domain Checks**   | Ensure numeric and categorical rules (e.g., amount ≥ 0).    |
| **Deduplication**   | Drop duplicates by PK before loading.                       |
| **Reject Logging**  | Store invalid rows in `stg_rejects` for inspection.         |

---

## 🪵 Structured Logging Examples

```
INFO ingest.start source=customers_csv rows=12034 path=data/customers.csv
INFO ingest.cleaned source=customers_csv valid=11890 rejected=144
INFO ingest.load source=customers_csv inserted=11750 updated=140 duration=3.2s
INFO ingest.end source=customers_csv status=success
```

Each run produces a concise summary of:

* total input rows
* valid vs rejected counts
* inserted vs updated records
* run duration and status

---

## 🧪 Testing Strategy (PyTest)

| Type                  | Focus                                                             |
| --------------------- | ----------------------------------------------------------------- |
| **Unit Tests**        | Type casting, rule evaluation, duplicate removal, SQL generation. |
| **Integration Tests** | Load sample CSV/JSON to Postgres and verify counts.               |
| **Property Tests**    | Validate numerical domains (e.g., all amounts ≥ 0).               |

> Use Docker or local Postgres for integration testing.

Target: **≥ 80% coverage**

---

## 🧠 Example Pseudocode Flow

```python
def run_source(cfg):
    df = read_input(cfg)                 # csv/json/api → DataFrame
    df = normalize_columns(df)           # trim/strip/lower headers
    df, rejects = apply_schema_casts(df, cfg.schema)
    df = enforce_required(df, cfg.schema)
    df, new_rejects = apply_rules(df, cfg.rules)
    rejects += new_rejects
    df = drop_duplicates(df, pk=cfg.pk)
    load_upsert(df, table=cfg.target_table, pk=cfg.pk, batch=cfg.batch_size)
    write_rejects(rejects, source_name=cfg.name)
    log_summary(cfg.name, len(df), len(rejects))
```

---

## 🧩 Definition of Done (Final)

* ✅ CSV and JSON data ingested into **PostgreSQL staging tables**.
* ✅ All **rejected rows captured** with reason and payload.
* ✅ Configuration-driven source definitions.
* ✅ Structured logging with run summary.
* ✅ **80%+ PyTest coverage**.
* ✅ Proper connection management.
* ✅ Clean modular design and naming conventions.
* ✅ Version-controlled repository with **README** and demo notebook.

---

## 🚀 Stretch Goals (Optional Enhancements)

| Area               | Feature                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------- |
| **Ingestion**      | Implement incremental loads using timestamp or surrogate key watermark.                                 |
| **Validation**     | Add schema validation with `pydantic` or data quality checks via `great_expectations`.                  |
| **Storage**        | Partition or cluster Postgres tables for large-scale analytics.                                         |
| **Deployment**     | Use **Docker Compose** for local Postgres + app environment.                                            |
| **Monitoring**     | Track load metrics (rows/sec, rejects/sec) and log to a dashboard.                                      |
| **Security**       | Move DB credentials and API keys to `.env` or secret manager.                                           |
| **Analytics**      | Create summary views or materialized tables for downstream use.                                         |
| **AI Integration** | Build a simple **model pipeline** (e.g., train a regression or classifier on cleaned data).             |
| **Feature Store**  | Extract and store **ML features** in Postgres for reuse in predictions.                                 |
| **Embedding Demo** | Generate vector embeddings from text columns using `sentence-transformers` or `OpenAI Embeddings` API.  |
| **RAG Experiment** | Add a **Retrieval-Augmented Generation** notebook that indexes sample data and queries it via LLM.      |
| **Auto Insights**  | Use a lightweight LLM (like `llama-cpp-python` or `OpenAI API`) to summarize or describe data patterns. |

---

## Resources

[Data Scenarios](https://github.com/ahmadvh/Data-Scenario)

## 🧭 Summary

The **Data Ingestion Subsystem** is a foundational, end-to-end data engineering project.
It simulates real-world ingestion pipelines — combining:

* **Python scripting** for data reading and validation,
* **SQL modeling** for data integrity and staging,
* **Logging and testing** for maintainability and observability.

By completing this project, we will gain a full picture of how **raw data becomes trustworthy, query-ready data**, setting them up for real data engineering, analytics, and cloud-based ELT systems.
