# Step 1 — Snowflake (raw layer)

> The landing zone for transactional invoice data. Nothing is transformed here; this layer is the **source of truth** for everything downstream.

---

## What lives here

A single raw table:

| Object | Type | Rows | Grain |
|---|---|---|---|
| `FMCG_RTM.raw.sales_data_raw` | Landing table | 100,000 | One row per invoice line |

The data covers a full calendar year (2024-01-01 → 2024-12-30) of a Mexican FMCG retail operation: invoices, store metadata (city, channel, format), product attributes (brand, category, prices), and customer metadata (age, gender, loyalty).

---

## Schema (21 columns)

The full `CREATE TABLE` statement with types and column-level comments lives at:

- [`ddl/sales_data_raw.sql`](ddl/sales_data_raw.sql)

| Group | Columns |
|---|---|
| **Invoice** | `invoice_id`, `invoice_date` |
| **Store** | `city`, `store_format`, `channel`, `payment_mode` |
| **Product** | `category`, `brand`, `cost_price`, `selling_price`, `stock_on_hand`, `reorder_level`, `lead_time_days` |
| **Transaction** | `units`, `revenue`, `cost`, `margin`, `Margin_%` |
| **Customer** | `customer_age`, `customer_gender`, `loyalty_flag` |

> **Data quality known at this layer:** `customer_age` has ~15% nulls in source; `customer_gender` contains the legacy value `'O'` that gets remapped to `'M'` in staging. See `02_dbt/models/staging/stg_sales_data.sql` for full cleaning logic.

---

## How data lands here

In a real pipeline this table is populated by a periodic **`COPY INTO`** from a Snowflake stage (S3, GCS, or internal). The DDL file at `ddl/sales_data_raw.sql` includes a commented `COPY INTO` example.

For reproducibility of this portfolio project, two source files are provided:

| File | Rows | Use |
|---|---|---|
| `sample_data/sales_data_raw.csv` | 100,000 | full source feed — what the pipeline runs on |
| `sample_data/sales_data_sample.csv` | 50 | quick-look sample for reviewers + smoke tests |

---

## Run without Snowflake — local DuckDB fallback

You don't need a Snowflake account to reproduce the full pipeline. The Python entrypoint at [`../scripts/build_powerbi_data.py`](../scripts/build_powerbi_data.py) reads `sample_data/sales_data_raw.csv` directly via DuckDB and applies the **exact same SQL transformations as the dbt models** — producing the 4 star-schema CSVs Power BI consumes.

```bash
# From the project root:
python scripts/build_powerbi_data.py
```

That's the recommended path for reviewers. The Snowflake DDL is provided so that the production deployment story is also explicit.

---

## What comes next

The dbt project in [`../02_dbt/`](../02_dbt/) reads from `FMCG_RTM.raw.sales_data_raw` and produces the Bronze → Silver → Gold transformations. See [`../02_dbt/README.md`](../02_dbt/README.md) for the model DAG.
