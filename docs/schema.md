# Schema Reference — DBT-MEXICO-FMCG-RTM-PROJECT

> Single source of truth for the schema across all 3 layers (Snowflake → dbt → Power BI). Per-table column lists are derived directly from the SQL / model definitions.

**Last verified:** 2026-05-15 against `02_dbt/models/` + `03_powerbi/data/` CSVs.

---

## Layer overview

```
┌────────────────────┐   ┌─────────────────────┐   ┌────────────────────┐
│  1. Snowflake      │   │  2. dbt             │   │  3. Power BI       │
│  (raw)             │ → │  (Bronze/Silver/    │ → │  (BI semantic +    │
│                    │   │   Gold marts)       │   │   DAX layer)       │
└────────────────────┘   └─────────────────────┘   └────────────────────┘
   1 table                  6 models                  4 loaded tables
   21 columns                                         + 3 calc tables
                                                      + 7 calc columns
                                                      + 10+ DAX measures
```

---

## Layer 1 — Snowflake (raw)

### `FMCG_RTM.raw.sales_data_raw`

**Grain:** one row per invoice line. **Rows:** 100,000. **Period:** 2024-01-01 → 2024-12-30.

| # | Column | Snowflake type | Notes |
|---|---|---|---|
| 1 | `invoice_id` | `NUMBER(18,0)` NOT NULL | Source transaction id |
| 2 | `invoice_date` | `TIMESTAMP_NTZ` | Date portion drives the calendar |
| 3 | `city` | `VARCHAR(64)` | 8 cities (CDMX, Guadalajara, Monterrey, Puebla, Querétaro, Leon, Merida, Tijuana) |
| 4 | `store_format` | `VARCHAR(32)` | Hyper / Super / Express |
| 5 | `category` | `VARCHAR(64)` | 8 product categories |
| 6 | `brand` | `VARCHAR(64)` | 8 brands |
| 7 | `channel` | `VARCHAR(32)` | Online / Offline / Omnichannel |
| 8 | `payment_mode` | `VARCHAR(32)` | Card / Cash / Wallet / UPI |
| 9 | `units` | `NUMBER(10,0)` | Units sold |
| 10 | `cost_price` | `NUMBER(20,10)` | Unit cost, MXN, unrounded |
| 11 | `selling_price` | `NUMBER(20,10)` | Unit price, MXN, unrounded |
| 12 | `revenue` | `NUMBER(20,10)` | `units × selling_price` |
| 13 | `cost` | `NUMBER(20,10)` | `units × cost_price` |
| 14 | `margin` | `NUMBER(20,10)` | `revenue − cost` |
| 15 | `Margin_%` | `NUMBER(20,18)` | `margin / revenue`, 0–1 range |
| 16 | `stock_on_hand` | `NUMBER(10,0)` | Inventory snapshot at invoice time |
| 17 | `reorder_level` | `NUMBER(10,0)` | Stock threshold for reorder |
| 18 | `lead_time_days` | `NUMBER(10,0)` | Replenishment lead time |
| 19 | `customer_age` | `NUMBER(10,1)` | Nullable; ~15% nulls in source |
| 20 | `customer_gender` | `VARCHAR(8)` | `M` / `F` / `O` (`O` is remapped to `M` in staging) |
| 21 | `loyalty_flag` | `NUMBER(1,0)` | `1` = member, `0` = non-member |

DDL: [`../01_snowflake/ddl/sales_data_raw.sql`](../01_snowflake/ddl/sales_data_raw.sql).

---

## Layer 2 — dbt (Bronze / Silver / Gold)

### Bronze — `stg_sales_data` (staging)

**File:** [`../02_dbt/models/staging/stg_sales_data.sql`](../02_dbt/models/staging/stg_sales_data.sql)
**Materialization:** `view` · **Schema:** `staging` · **Grain:** 1 row per invoice line · **Rows:** 100,000

Pass-through of source columns with:
- `CAST(invoice_date AS DATE)`
- `ROUND()` on currency columns to 2-decimal MXN (4-decimal on `margin_pct`)
- `COALESCE(customer_age, 0)` (note: a 0 means "unknown")

Column list = same 21 columns as source.

### Silver — `int_route_performance` (intermediate)

**File:** [`../02_dbt/models/intermediate/int_route_performance.sql`](../02_dbt/models/intermediate/int_route_performance.sql)
**Materialization:** `view` · **Schema:** `intermediate` · **Grain:** 1 row per invoice line · **Rows:** 100,000

Adds business logic on top of Bronze:

| Column | Logic |
|---|---|
| `customer_gender` | `SWITCH`: `'O'` → `'M'`; `'M'`/`'F'` kept; else `'N/A'` |
| `loyalty_status` | `1` → `'member'`, else `'non-member'` |
| `avg_ticket_price` | `ROUND(revenue / units, 2)` |
| `profit_segment` | `>= 20%` → `high profit`, `>= 10%` → `medium profit`, else `low profit` |

All other columns inherited from staging.

### Gold — marts

#### `dim_customers`

**File:** [`../02_dbt/models/marts/dim_customers.sql`](../02_dbt/models/marts/dim_customers.sql)
**Materialization:** `view` · **Schema:** `marts` · **Grain:** 1 row per (age × gender × loyalty) · **Rows:** 288

| # | Column | Type | Notes |
|---|---|---|---|
| 1 | `customers_key` | text | MD5 PK via `dbt_utils.generate_surrogate_key(['customer_age','customer_gender','loyalty_status'])` |
| 2 | `customer_age` | int | `0` = unknown |
| 3 | `customer_gender` | text | `M` / `F` / `N/A` |
| 4 | `loyalty_status` | text | `member` / `non-member` |

> **Naming note:** functionally a customer-*profile* dim, not a per-customer dim. A more accurate name would be `dim_customer_profile`.

#### `dim_products`

**File:** [`../02_dbt/models/marts/dim_products.sql`](../02_dbt/models/marts/dim_products.sql)
**Materialization:** `view` · **Schema:** `marts` · **Grain:** 1 row per (brand × category) · **Rows:** 64

| # | Column | Type | Notes |
|---|---|---|---|
| 1 | `product_key` | text | MD5 PK via `dbt_utils.generate_surrogate_key(['brand','category'])` |
| 2 | `brand` | text | 8 brands |
| 3 | `category` | text | 8 categories |
| 4 | `cost_price` | number | **AVG** of per-line cost prices across this brand × category |
| 5 | `selling_price` | number | **AVG** of per-line selling prices |
| 6 | `stock_on_hand` | int | **AVG** of per-line stock snapshots |
| 7 | `reorder_level` | int | **AVG** of per-line reorder thresholds |
| 8 | `lead_time_days` | number | **AVG** of per-line lead times |

> **Grain caveat:** the raw data carries `cost_price`, `selling_price`, `stock_on_hand`, `reorder_level`, and `lead_time_days` per invoice line (they vary across the year for the same brand/category). `dim_products` AVG-rolls them to brand × category grain so the dim preserves a proper many-to-one relationship with `fct_sales` (64 rows, not 100k). For exact per-line values, query `fct_sales` joined with `stg_sales_data`.

#### `dim_locations`

**File:** [`../02_dbt/models/marts/dim_locations.sql`](../02_dbt/models/marts/dim_locations.sql)
**Materialization:** `view` · **Schema:** `marts` · **Grain:** 1 row per (city × channel × format) — a "route" · **Rows:** 72

| # | Column | Type | Notes |
|---|---|---|---|
| 1 | `location_key` | text | MD5 PK via `dbt_utils.generate_surrogate_key(['city','channel','store_format'])` |
| 2 | `city` | text | 8 cities; `COALESCE` to `'Desconocido'` |
| 3 | `channel` | text | Offline / Online / Omnichannel; `COALESCE` to `'No Definido'` |
| 4 | `store_format` | text | Express / Super / Hyper; `COALESCE` to `'General'` |

#### `fct_sales`

**File:** [`../02_dbt/models/marts/fct_sales.sql`](../02_dbt/models/marts/fct_sales.sql)
**Materialization:** `view` · **Schema:** `marts` · **Grain:** 1 row per invoice line · **Rows:** 100,000

| # | Column | Type | Notes |
|---|---|---|---|
| 1 | `customers_key` | text | FK → `dim_customers` |
| 2 | `product_key` | text | FK → `dim_products` |
| 3 | `location_key` | text | FK → `dim_locations` |
| 4 | `invoice_id` | int | Source identifier |
| 5 | `invoice_date` | date | FK → `Dim_Date` (PBI-side) |
| 6 | `units` | int | Units sold |
| 7 | `revenue` | number | MXN |
| 8 | `cost` | number | MXN |
| 9 | `margin` | number | `revenue − cost` |
| 10 | `margin_pct` | number | 0–1 range |
| 11 | `avg_ticket_price` | number | `revenue / units` |
| 12 | `profit_segment` | text | `high` / `medium` / `low profit` |
| 13 | `payment_mode` | text | Card / Cash / Wallet / UPI |

---

## Layer 3 — Power BI

The 4 Gold marts above are loaded into Power BI as-is (preserving names). PBI adds three categories of objects on top.

### 3a. Loaded → identical to Gold

| dbt mart | PBI loaded table |
|---|---|
| `fct_sales` | `fct_sales` |
| `dim_customers` | `dim_customers` |
| `dim_products` | `dim_products` |
| `dim_locations` | `dim_locations` |

Loading is done via the M-script: [`../03_powerbi/PowerQuery_M_Script.m`](../03_powerbi/PowerQuery_M_Script.m).

### 3b. PBI-added calculated tables

| Table | Type | Purpose |
|---|---|---|
| `Dim_Date` | DAX `CALENDAR(...)` + `ADDCOLUMNS` | Marked-as-date-table calendar 2024-01-01 → 2024-12-31 |
| `Measure_` | DAX `Row("Column", BLANK())` | Empty container holding all explicit measures |
| `Tabla Rutas CTS` | DAX `ADDCOLUMNS(SUMMARIZE(...))` | Route-grain summary used by route-level visuals |

### 3c. PBI-added calculated columns

**On `dim_locations`:** `RouteID`, `Territory`, `Segmento CTS`
**On `fct_sales`:** `DropBucket`, `CTS Index Col`, `RouteID Corto`, `Segmento CTS Col`

Full DAX bodies in [`../03_powerbi/Data_Dictionary.md`](../03_powerbi/Data_Dictionary.md#3-pbi-added-calculated-columns).

### 3d. Active DAX measures (10 in `Measure_`)

`CTSIndex` · `Average Gross %` · `Anual Average Gross` · `Drop Size Promedio` · `Desviacion Margen PP` · `Etiqueta CTS` · `Etiqueta Drop Size` · `Estado Drop Size` · `Foco Prioritario` · `Insight Drop Size`

Detail + business purpose in [`../03_powerbi/Data_Dictionary.md`](../03_powerbi/Data_Dictionary.md#4-active-dax-measures-in-measure_-table).

> The .pbix also contains inactive (orphan) measures that exist in the model but are not bound to any visual. They're preserved for DAX-portfolio purposes — open in DAX Studio to enumerate.

---

## Relationships (Power BI model)

| From | To | Cardinality | Active |
|---|---|---|---|
| `fct_sales[customers_key]` | `dim_customers[customers_key]` | `*:1` | yes |
| `fct_sales[product_key]` | `dim_products[product_key]` | `*:1` | yes |
| `fct_sales[location_key]` | `dim_locations[location_key]` | `*:1` | yes |
| `fct_sales[invoice_date]` | `Dim_Date[Date]` | `*:1` | yes |
| `fct_sales[RouteID Corto]` | `Tabla Rutas CTS[RouteID Corto]` | `*:1` | yes |

ERD: [`../03_powerbi/star_schema.html`](../03_powerbi/star_schema.html).

---

## Production materialization recommendations

The current `dbt_project.yml` materializes every layer as `view` — convenient for development, not optimal for production. Suggested overrides for a production deployment:

| Layer | Current | Recommended | Why |
|---|---|---|---|
| `staging` | view | view | Light pass-through, no need to materialize |
| `intermediate` | view | view (or `ephemeral`) | Same; ephemeral inlines into downstream |
| `marts` (dims) | view | `table` | 64–288 rows; cheap to rebuild, instant reads |
| `marts.fct_sales` | view | `incremental` with `unique_key='invoice_id'`, `merge` strategy, `cluster_by=['invoice_date','location_key']` | Append-only, grows over time; avoid full rebuild |

---

## Cross-reference index

- DDL → [`../01_snowflake/ddl/sales_data_raw.sql`](../01_snowflake/ddl/sales_data_raw.sql)
- dbt project + how-to-run → [`../02_dbt/README.md`](../02_dbt/README.md)
- PBI model reference → [`../03_powerbi/Data_Dictionary.md`](../03_powerbi/Data_Dictionary.md)
- PBI DAX layer story → [`../03_powerbi/README.md`](../03_powerbi/README.md)
- Star schema ERD → [`../03_powerbi/star_schema.html`](../03_powerbi/star_schema.html)
