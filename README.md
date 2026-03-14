# ERP Operations Pipeline

Automated ELT pipeline that extracts D365-structured manufacturing data (work orders, BOMs, inventory) from a simulated ERP source, transforms it with dbt, and loads it into Azure Blob Storage — with CI/CD via GitHub Actions and automated
data quality validation.

---

## Architecture

[PostgreSQL - Simulated ERP Source]
- work_orders, bom, inventory, vendors
|
| Python extraction (incremental, updated_at filter)
|
[Azure Blob Storage - Raw Zone]
raw//YYYY/MM/DD/.parquet
        |
        | dbt transformations (DuckDB)
        |
[Warehouse Layer]
stg_work_orders / stg_inventory / stg_vendors
fct_production_summary
        |
        | GitHub Actions (daily 6am + on push)
        | pytest + dbt tests gate every run

---

## Stack

| Layer | Tool |
|---|---|
| Source DB | PostgreSQL 15 (Docker) |
| Extraction | Python 3.11, pandas, psycopg2 |
| Storage | Azure Blob Storage (Parquet) |
| Transformation | dbt Core + DuckDB |
| Testing | pytest, dbt tests |
| CI/CD | GitHub Actions |

---

## Key Design Decisions

**Incremental extraction** - only pulls rows updated since the last run using an `updated_at` filter. Avoids hammering the source database on every run - critical at production ERP scale.

**Parquet over CSV** - columnar storage format. Faster analytical queries, smaller file size, native support in DuckDB and Azure Synapse.

**dbt over raw SQL scripts** - modular, testable, version controlled transformations. Same patterns used by data teams at scale.

**Separate source and warehouse** - PostgreSQL is the source system, DuckDB is the analytical layer. Mirrors real production architecture where you never run analytics directly against the operational database.

---

## Running Locally

### Prerequisites
- Docker Desktop
- Python 3.11+
- Azure Storage account

### Setup

```bash
# Start the database
docker-compose up -d

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Seed with synthetic manufacturing data
python seed_data.py

# Run the pipeline
python extract.py
python load.py

# Run dbt transformations
cd erp_pipeline
dbt run --profiles-dir .
dbt test --profiles-dir .

Environment Variables

Create a .env file in the project root:

AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_CONTAINER_NAME=erp-raw

---
Data Model

Source Tables

- work_orders - production work orders with status, priority, quantities, dates
- bom - bill of materials with parent/child part relationships and revision control
- inventory - part inventory levels, reorder points, vendor assignments
- vendors - vendor performance data including on-time delivery rates

dbt Models

- stg_work_orders - cleaned work orders with overdue flag and qty remaining
- stg_inventory - inventory with stock buffer and at-risk flag
- stg_vendors - vendors with underperforming flag
- fct_production_summary - daily production KPIs including schedule attainment %, critical order count, parts at risk

---
CI/CD

GitHub Actions runs on every push to master and daily at 6am:

1. Spin up PostgreSQL service container
2. Seed database with synthetic data
3. Run pytest unit tests
4. Run Python extraction
5. Run dbt models and data quality tests
6. Upload Parquet files to Azure Blob Storage
