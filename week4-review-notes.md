# Week 4 — Cloud, Big Data & Data Engineering

## Learning Outcomes

By the end of this week you should be able to:

* Explain core **cloud computing** concepts, service models, and pricing approaches.
* Describe what **Big Data** is, why it matters, and its **components, architecture, benefits, and challenges**.
* Walk through the **data lifecycle** and different **types of data** and **file formats** used in analytics.
* Explain the role of **data warehouses**, **data lakes**, **OLTP vs OLAP**, **ODS**, and **data marts**.
* Discuss key **data modeling** concepts: **conceptual/logical/physical models**, **dimensional modeling**, **star/snowflake schemas**, and **SCD types**.
* Understand the basics of **data cleansing**, **BigQuery**, and how to **create datasets, tables, and queries**.
* Differentiate between **ETL vs ELT** and describe how modern **data pipelines** are built and orchestrated.

---

## ☁️ Cloud Computing Foundations

### Cloud Computing Definition

* **Cloud computing**: On-demand access to computing resources (servers, storage, databases, networking, analytics, ML) over the internet.
* Key traits:

  * **On-demand self-service** – spin up resources without human interaction.
  * **Broad network access** – available over the internet.
  * **Resource pooling** – shared infrastructure, multi-tenant.
  * **Rapid elasticity** – scale up/down quickly.
  * **Measured service** – pay for what you use.

### Cloud Computing Model Types (Deployment Models)

* **Public Cloud** – shared infrastructure managed by provider (AWS, Azure, GCP).
* **Private Cloud** – cloud tech dedicated to one organization.
* **Hybrid Cloud** – mix of public and private with integration.
* **Multi-Cloud** – multiple public clouds for redundancy / vendor flexibility.

### Cloud Computing Service Types

* **IaaS (Infrastructure as a Service)**

  * You manage: OS, runtime, apps.
  * Provider manages: hardware, networking, storage.
  * Example: EC2, GCE, Azure VMs.

* **PaaS (Platform as a Service)**

  * You manage: code & configuration.
  * Provider manages: OS, runtime, scaling.
  * Example: App Engine, Heroku, Azure App Service.

* **SaaS (Software as a Service)**

  * You just use the application.
  * Example: Salesforce, Gmail, Power BI Online.

### Cloud Challenges

* **Security & compliance** (data privacy, regulations).
* **Vendor lock-in** (hard to move workloads).
* **Cost management** (uncontrolled usage → surprise bills).
* **Operational complexity** (networking, IAM, monitoring).
* **Shared responsibility** – must understand what provider vs customer handles.

### Pricing Basics

* Pay-as-you-go: pay only for **compute, storage, and data transfer** used.
* **Reserved / committed use** discounts for long-term commitments.
* **Serverless**: pay per execution or per query (BigQuery, Lambda, Cloud Functions).
* Important interview angle: **optimize cost** via right sizing, autoscaling, shutting down idle resources, and choosing appropriate storage tiers.

### AWS / Azure / GCP (Data Services)

* **AWS**(Amazon)

  * DWH: Redshift
  * Data Lake: S3
  * ETL: Glue
  * Streaming: Kinesis

* **Azure**(Microsoft)

  * DWH: Synapse Analytics
  * Data Lake: ADLS
  * ETL/Orchestration: Data Factory

* **GCP**(Google)

  * DWH: **BigQuery**
  * Data Lake: Cloud Storage
  * Streaming: Pub/Sub + Dataflow
  * Orchestration: Cloud Composer (Airflow), Workflows

---

## 📦 Big Data Foundations

### Big Data Fundamentals

* Big Data is often characterized by the **3 Vs**:

  * **Volume** – massive amounts of data.
  * **Velocity** – speed of data generation/ingestion.
  * **Variety** – many formats (structured, semi-structured, unstructured).
* Goal: turn huge, messy data into **insights, products, and decisions**.

### Components of Big Data

* **Data sources** – apps, logs, IoT, transactions, social media, 3rd-party feeds.
* **Ingestion** – batch (files, DB dumps) & streaming (Kafka, Pub/Sub).
* **Storage** – data lakes, data warehouses, object storage.
* **Processing** – batch (Spark, Dataflow), streaming (Flink, Kafka Streams).
* **Analytics / ML** – BI tools, notebooks, ML frameworks.

### Big Data Architecture (High-Level)

* **Ingest → Store → Process → Serve → Consume**.
* Data moves from raw landing zones → cleaned layers → modeled layers for BI/ML.
* Modern pattern: **Medallion Architecture** (Bronze, Silver, Gold).

### Benefits of Big Data

* Better decisions through large-scale analytics.
* Personalization, recommendations, fraud detection.
* Operational optimization (monitoring, capacity planning).
* New products / revenue streams (data products, analytics services).

### Challenges of Big Data

* Storage & compute cost at scale.
* Data quality and consistency.
* Security & privacy (PII, regulations).
* Tool complexity and skills gap.
* Keeping schemas and pipelines stable as systems evolve.

---

## 🔄 Data Lifecycle & Data Types

### Data Lifecycle Stages

Think of data as moving through layers:

1. **Generation / Ingestion** – data created by systems, devices, users.
2. **Landing / Bronze** – raw, immutable, as-is.
3. **Validation & Data Quality** – schema checks, null checks, anomaly detection.
4. **Processing / Silver** – cleaned, standardized, deduped, conformed.
5. **Modeling / Gold** – business-ready tables (facts, dimensions, aggregates).
6. **Serving & Consumption** – BI dashboards, ML models, APIs, exports.
7. **Archival & Retention** – cold storage, backups, deletion for compliance.
8. **Governance & Lineage** – access control, data catalogs, audit logs across all stages.

### Types of Data

* **Structured** – tabular, fixed schema (SQL tables).
* **Semi-Structured** – flexible schema (JSON, Avro, XML, logs).
* **Unstructured** – text, images, audio, video.
* Interview point: engineers must know how to **store and process each type**.

### File Types in Data Engineering

* **CSV** – simple, human-readable; no schema; large files can be inefficient.
* **JSON** – great for nested/semi-structured data; common for APIs and logs.
* **Parquet / ORC** – columnar, compressed, good for large-scale data analytics, data lakes, or warehouse environments.
* **Avro** – row-based, schema-evolving, often used in Kafka and pipelines. Avro is better suited for write-intensive operations and scenarios requiring robust schema evolution

Know when you’d pick CSV vs Parquet vs JSON vs Avro.

---

## 🏛 Data Warehousing Architecture

### Data Warehousing Intro

* A **data warehouse (DWH)** is a central store optimized for **analytics** (OLAP).
* Integrates data from multiple sources for reporting, BI, and ML.

### Data Store Vendors

* Traditional: Teradata, Oracle, SQL Server.
* Cloud: BigQuery, Snowflake, Redshift, Synapse.
* Key differentiators: performance model, pricing, ecosystem, serverless vs cluster-based.

### OLTP vs OLAP

* **OLTP** (Online Transaction Processing)

  * Many small, concurrent writes.
  * Normalized schema.
  * Use case: banking, shopping carts.

* **OLAP** (Online Analytical Processing)

  * Fewer but complex, long-running read queries.
  * Denormalized / dimensional schemas.
  * Use case: dashboards, reports, analytics.

### DWH vs Data Lake

* **Data Lake**

  * Stores raw data of any type (schema-on-read).
  * Flexible, cheap storage (e.g., object storage).

* **Data Warehouse**

  * Stores structured, curated data (schema-on-write).
  * Optimized for SQL, BI, and analytics.

Many orgs use **lakehouse** patterns or combine both.

### DWH Architecture

* **Staging / Landing** – raw ingested data.
* **Integration layer** – cleaned / conformed tables.
* **Presentation layer** – star/snowflake schemas, data marts.
* Supports **governance, metadata, lineage**.

### Operational Data Store (ODS)

* A near-real-time, integrated store between OLTP and DWH.
* Used for **operational reporting** and as a buffer before the warehouse.

### Data Marts

* Subject-specific segments of the warehouse: sales mart, finance mart, marketing mart.
* Often designed as **star schemas** for specific teams.

---

## 📐 Data Modeling

### Modeling Overview

* Process of designing how data is structured and related.
* Good models make queries **fast**, **consistent**, and **understandable**.

### Conceptual / Logical / Physical Models

* **Conceptual** – high-level entities and relationships (business view).
* **Logical** – attributes, keys, relationships; tech-agnostic.
* **Physical** – actual implementation: table names, columns, indexes, partitions.

### Dimensional Modeling

* Optimized for analytics.
* Uses **fact tables** (measures) + **dimension tables** (context).
* Goal: fast queries, easy for BI, simple joins.

### Star Schema

* One central **fact** table linked to multiple **dimension** tables.
* Simple join pattern; great for BI tools and performance.

### Snowflake Schema

* Dimensions are further normalized into sub-dimensions.
* Reduces redundancy, can be more complex to query.
* Trade-off: normalization vs simplicity/performance.

### Slowly Changing Dimensions (SCD) & Types

* Dimensions whose attributes change over time (e.g., customer address).
* **SCD Types**:

  * **Type 0** – no change, keep original.
  * **Type 1** – overwrite old value (no history).
  * **Type 2** – add new row with effective dates (keep full history).
  * **Type 3+** – limited history via extra columns, etc.
* Important interview topic for **history and auditability**.

---

## 🛠 Data Engineering & BigQuery

### Data Cleansing

* Handling **nulls**, **duplicates**, **wrong types**, **inconsistent formatting**.
* Typical operations:

  * Trim whitespace, standardize category names.
  * Enforce data types (CAST / SAFE_CAST).
  * Drop or flag invalid records.
* Key idea: **“Garbage in, garbage out.”**

### BigQuery Overview

* Google Cloud’s **serverless data warehouse**.
* You pay for:

  * Storage
  * **Bytes scanned per query**
* Great for ELT, large-scale analytics, and columnar queries.

### Creating Datasets

* A **dataset** is a logical container for tables and views.
* Typically separated by domain, environment, or layer (bronze/silver/gold).

### Create and Use Tables

* Ways to create tables:

  * From **UI** (upload CSV/JSON).
  * With **CREATE TABLE** or **CREATE TABLE AS SELECT (CTAS)**.
  * From **external sources** (Cloud Storage, external tables).

* Know basics:

  * Define schema (columns, types, nullable).
  * Use **partitioning** and **clustering** for performance & cost control.

### BigQuery Queries

* Standard SQL: `SELECT`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`.
* Analytics features:

  * **Window functions** (`OVER (PARTITION BY ... ORDER BY ...)`).
  * **ARRAY / STRUCT** types.
  * **PIVOT / UNPIVOT**.

### Advanced Queries

* **CTEs** (`WITH` clauses) for readable, multi-step transformations.
* **Analytic functions** for rolling averages, rankings, sessions.
* **Correlated subqueries** and **recursive CTEs** for hierarchies.
* Optimization points:

  * Select only needed columns.
  * Filter early using partitions.
  * Avoid unnecessary cross joins.

### Denormalization

* Intentionally combining tables (facts + common dimensions) to reduce joins.
* Very common in BigQuery because:

  * Columnar storage → reading only necessary columns is cheap.
* Use for **Gold tables**, ML feature tables, and dashboards.
* Be aware of trade-offs: duplication, update complexity.

### BigQuery Connections

* Secure ways for BigQuery to access **external systems**:

  * Cloud SQL, Cloud Storage, S3, Salesforce, external APIs, etc.
* In Sandbox you mostly work with:

  * Uploading files
  * External tables on Cloud Storage (conceptually)

---

## 🔁 ETL, ELT & Building Pipelines

### ETL Overview (Extract–Transform–Load)

* **Extract** from sources → **Transform** in an ETL server → **Load** into DWH.
* Historically used when warehouses were expensive/limited.
* Still relevant for:

  * Heavy pre-load validation
  * Compliance-sensitive data
  * Legacy on-prem systems.

### ELT Overview (Extract–Load–Transform)

* **Extract** and **Load** raw data into the warehouse first (Bronze).
* **Transform** using DWH compute (SQL in BigQuery).
* Today’s standard pattern in cloud environments.
* Maps nicely to **Medallion Architecture**:

  * Bronze: raw
  * Silver: cleaned
  * Gold: modeled / business-ready

### Building ETL/ELT Processes

Key concepts you should be ready to talk about:

* **Pipeline stages**: ingest → bronze → silver → gold → serve.
* **Batch vs streaming**:

  * Batch: scheduled daily/hourly (reports, aggregates).
  * Streaming: near real-time (fraud detection, clickstream, IoT).
* **Orchestration**:

  * Tools: Airflow, Prefect, Dagster, Cloud Composer.
  * DAGs: tasks with dependencies (extract → load → transform).
* **Error handling & monitoring**:

  * Detect schema drift, null explosions, job failures.
  * Use logs, metrics, and alerts (Slack/email).
* **Testing & data quality**:

  * Unit tests for transformation logic (pytest).
  * Data quality checks: row counts, nulls, referential integrity, freshness.
  * Great Expectations or dbt tests in more advanced setups.
* **CI/CD for pipelines**:

  * Validate SQL with dry runs.
  * Run tests on every commit.
  * Deploy DAGs/configs from version control.

---

## 🎤 Interview Prep — Questions to Practice

You should be able to explain each one out loud:

1. What is the difference between **OLTP** and **OLAP**?
2. How would you explain a **data warehouse** vs a **data lake** to a non-technical stakeholder?
3. Describe the **Medallion Architecture** (Bronze/Silver/Gold).
4. When would you use **denormalization** in a data warehouse?
5. What is an **SCD Type 2** dimension and why is it used?
6. Explain **ETL vs ELT** and why ELT is preferred in modern cloud platforms.
7. What are **partitioned tables** in BigQuery and why are they important?
8. Describe a simple **end-to-end pipeline** you might build with Python + BigQuery.
9. What are some **challenges of Big Data** (technical and organizational)?
10. How would you handle **data quality** in a real pipeline?

---
