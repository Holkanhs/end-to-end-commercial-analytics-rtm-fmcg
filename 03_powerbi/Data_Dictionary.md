# Power BI Data Dictionary

> Field-level reference for the Power BI semantic model. Documents both the **loaded tables** (the dbt Gold marts) and the **PBI-added objects** (calculated tables, calculated columns, and measures).

**Source:** the 4 CSVs in [`data/`](data/) produced by [`../scripts/build_powerbi_data.py`](../scripts/build_powerbi_data.py).
**Loaded into Power BI:** via the 4 queries defined in [`PowerQuery_M_Script.m`](PowerQuery_M_Script.m).
**Period:** 2024-01-01 → 2024-12-30.

---

## 1. Loaded tables (from dbt marts)

### `fct_sales` — fact table

**Grain:** one row per invoice line. **Rows:** 100,000.

| # | Column | Type | Description |
|---|---|---|---|
| 1 | `customers_key` | text | MD5 surrogate FK → `dim_customers` |
| 2 | `product_key` | text | MD5 surrogate FK → `dim_products` |
| 3 | `location_key` | text | MD5 surrogate FK → `dim_locations` |
| 4 | `invoice_id` | int | Source transaction identifier |
| 5 | `invoice_date` | date | Date of the invoice (joins `Dim_Date[Date]`) |
| 6 | `units` | int | Units sold |
| 7 | `revenue` | number | Gross revenue in MXN (`units × selling_price`) |
| 8 | `cost` | number | Total COGS in MXN |
| 9 | `margin` | number | `revenue − cost` |
| 10 | `margin_pct` | number | `margin / revenue`, 0–1 range |
| 11 | `avg_ticket_price` | number | `revenue / units` |
| 12 | `profit_segment` | text | `high profit` / `medium profit` / `low profit` |
| 13 | `payment_mode` | text | `Card` / `Cash` / `Wallet` / `UPI` |

### `dim_customers` — customer-profile dimension

**Grain:** one row per (age × gender × loyalty) combination. **Rows:** 288.

| # | Column | Type | Description |
|---|---|---|---|
| 1 | `customers_key` | text | MD5 PK |
| 2 | `customer_age` | int | Age in years; `0` = unknown |
| 3 | `customer_gender` | text | `M` / `F` / `N/A` (`O` is remapped to `M` in staging) |
| 4 | `loyalty_status` | text | `member` / `non-member` |

> **Naming note:** this is functionally a customer-*profile* dimension, not a per-customer dim — the key is built from low-cardinality attributes. A more accurate name would be `dim_customer_profile`.

### `dim_products` — product dimension

**Grain:** one row per (brand × category). **Rows:** 64.

| # | Column | Type | Description |
|---|---|---|---|
| 1 | `product_key` | text | MD5 PK |
| 2 | `brand` | text | 8 brands: Alpura, Bimbo, Lala, Marinela, Nestle, PepsiCo, Sigma, Unilever |
| 3 | `category` | text | 8 categories: Beverages, Dairy, Fruits, Grocery, Home Care, Personal Care, Snacks, Vegetables |
| 4 | `cost_price` | number | Average unit cost (MXN) across all invoices for this brand × category |
| 5 | `selling_price` | number | Average unit selling price (MXN) — same rollup |
| 6 | `stock_on_hand` | int | Average stock snapshot — same rollup |
| 7 | `reorder_level` | int | Average reorder threshold — same rollup |
| 8 | `lead_time_days` | number | Average replenishment lead time (days) — same rollup |

> **Grain note:** the 5 numeric columns are **AVG rollups** across all invoice lines for that brand × category — they represent "typical" values, not exact per-SKU values. The raw data carries them per line, not per SKU, so this rollup is the only way to keep `dim_products` at proper dim grain (64 rows) rather than fact grain (100k rows). For exact per-line values, query `fct_sales` directly or join back to `stg_sales_data`.

### `dim_locations` — store / route dimension

**Grain:** one row per (city × channel × store_format) = one "route". **Rows:** 72.

| # | Column | Type | Description |
|---|---|---|---|
| 1 | `location_key` | text | MD5 PK |
| 2 | `city` | text | 8 cities: Ciudad de Mexico, Guadalajara, Monterrey, Puebla, Queretaro, Leon, Merida, Tijuana |
| 3 | `channel` | text | Offline / Online / Omnichannel |
| 4 | `store_format` | text | Express / Super / Hyper |

---

## 2. PBI-added calculated tables

Three tables exist only inside the .pbix — created via DAX, not loaded from CSV.

| Table | Type | Purpose |
|---|---|---|
| `Dim_Date` | DAX calculated table | Calendar 2024-01-01 → 2024-12-31 with Year, Quarter, MonthNo, MonthName (es-MX), YearMonth, DayOfWeek, IsWeekend. Marked as Date Table. |
| `Measure_` | DAX calculated table | Empty container (`Row("Column", BLANK())`) that holds all explicit measures. Common pattern to keep measures separate from data tables in the Fields pane. |
| `Tabla Rutas CTS` | DAX calculated table | Route-grain summary: `ADDCOLUMNS(SUMMARIZE(fct_sales, ...))` producing per-route revenue, CTS, segment. Used by route-level visuals. |

---

## 3. PBI-added calculated columns

Defined in DAX inside the .pbix (not in dbt or M). All are "active" — used by visuals.

### On `dim_locations`

| Column | DAX (approximate) | Purpose |
|---|---|---|
| `RouteID` | `LEFT(city,3) & "-" & LEFT(channel,2) & "-" & LEFT(store_format,2)` | Compact route code for axes |
| `Territory` | `SWITCH(TRUE(), city="Ciudad de Mexico", "CDMX", city="Guadalajara", "GDL", city="Monterrey", "MTY", city IN {"Puebla","Queretaro","Leon"}, "Bajío", "Sureste/Norte")` | Regional rollup for heatmaps |
| `Segmento CTS` | `VAR Index = CALCULATE([CTSIndex]) RETURN IF(Index >= 0.88, "Crítico", IF(Index >= 0.875, "Medio", "OK"))` | Route CTS classification |

### On `fct_sales`

| Column | DAX (approximate) | Purpose |
|---|---|---|
| `DropBucket` | `SWITCH(TRUE(), revenue >= 1000, "Healthy >$1,000", revenue >= 500, "Optimize $500-$1K", "Critical <$500")` | Drop-size bucket for donut/distribution visuals |
| `CTS Index Col` | `DIVIDE(cost, revenue, 0) * (1 + DIVIDE(RELATED(dim_products[lead_time_days]), 100, 0))` | Per-line CTS proxy |
| `RouteID Corto` | `LEFT(RELATED(dim_locations[city]),3) & "-" & LEFT(RELATED(dim_locations[channel]),2) & "-" & ...` | Foreign-key join column to `Tabla Rutas CTS` |
| `Segmento CTS Col` | `VAR Index = DIVIDE(cost, revenue, 0) * ... RETURN IF(...)` | Per-line CTS segment label |

> **Verify exact DAX:** open the .pbix in Power BI Desktop (Model view → click column → Formula bar) or DAX Studio (View Metrics → export model.bim).

---

## 4. Active DAX measures (in `Measure_` table)

10 measures used by visuals. Names + business purpose; exact bodies live inside the .pbix.

| Measure | Purpose | Type |
|---|---|---|
| `CTSIndex` | Cost-to-Serve index = `(cost/revenue) × (1 + lead_time_days/100)`. Core KPI. | Numeric |
| `Average Gross %` | Aggregate gross margin %. `DIVIDE(SUM(margin), SUM(revenue))`. | Numeric % |
| `Anual Average Gross` | Annual rollup of `Average Gross %`. | Numeric % |
| `Drop Size Promedio` | Average ticket / drop size per invoice. | Numeric (MXN) |
| `Desviacion Margen PP` | Margin deviation in percentage points vs. baseline (likely prior period). | Numeric (pp) |
| `Etiqueta CTS` | Formatted text label for the CTS card (▲/▼ + value). | Text |
| `Etiqueta Drop Size` | Formatted text label for the Drop Size card. | Text |
| `Estado Drop Size` | Status indicator (high/low/target) for drop size. | Text |
| `Foco Prioritario` | `SWITCH`-based recommendation: which lever needs attention. | Text |
| `Insight Drop Size` | Auto-generated insight string for the drop-size visual. | Text |

> The .pbix also contains inactive (orphan) measures — they exist in the model but are not placed on any visual. See [`../docs/schema.md`](../docs/schema.md) → "Measure inventory" for the full audit (active vs. orphan).

---

## 5. Pre-aggregated reference values (QA)

Computed from the full dataset; useful for sanity-checking visuals.

| Metric | Value |
|---|---|
| Rows in `fct_sales` | 100,000 |
| Total revenue | $118,005,404 MXN |
| Mean `margin_pct` | 19.34% |
| Mean `avg_ticket_price` | $393.32 MXN |
| Distinct routes (city × channel × format) | 72 |
| Distinct invoices | 100,000 (1 line per invoice in this dataset) |

---

## 6. Known caveats

- `customer_age = 0` indicates **unknown** — exclude or bucket as "n/d" in visuals.
- Single-year dataset (2024). YoY measures will be blank until a prior-year extract is added.
- `lead_time_days` is per-line, not per-SKU; aggregate with `AVERAGE`, never `SUM`.
- `DropBucket` uses `>=` operators (`>= $1,000` = Healthy, `>= $500` = Optimize). Numeric boundaries are inclusive at the lower edge.
