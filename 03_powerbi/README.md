# Step 3 — Power BI (BI layer)

> The semantic + presentation layer. Loads the dbt Gold marts as a star schema, adds calculated tables, calculated columns, and DAX measures, then renders the executive dashboard.

---

## What ships in this folder

| File | Purpose |
|---|---|
| [`RTM_FINAL_PROJECT.pbix`](RTM_FINAL_PROJECT.pbix) | The Power BI Desktop file (5.5 MB). Open this to view the dashboard, the data model, and all DAX. |
| [`PowerQuery_M_Script.m`](PowerQuery_M_Script.m) | The M code that loads the 4 star-schema CSVs. Paste each block into a new blank query in Power BI. |
| [`RTM_Theme.json`](RTM_Theme.json) | Looker-style theme (Google Material palette). View → Themes → Browse for themes → load this. |
| [`Data_Dictionary.md`](Data_Dictionary.md) | Field-level reference: loaded columns + DAX calc columns + DAX measures. |
| [`star_schema.html`](star_schema.html) | Mermaid-based ERD; open in any browser. |
| [`data/`](data/) | The 4 star-schema CSVs the .pbix loads. Regenerable via `python ../scripts/build_powerbi_data.py`. |

---

## Loading approach

```
01_snowflake/sample_data/sales_data_raw.csv
    ↓  (build_powerbi_data.py — mirrors dbt staging → intermediate → marts)
03_powerbi/data/
    ├── fct_sales.csv     (100,000 rows)
    ├── dim_customers.csv  (288 rows)
    ├── dim_products.csv   (64 rows)
    └── dim_locations.csv  (72 rows)
    ↓  (PowerQuery_M_Script.m — 4 simple star-schema loads, no derivations)
RTM_FINAL_PROJECT.pbix
    ├── Loaded model:    fct_sales + 3 dims
    ├── DAX layer:       Dim_Date (calc table)
    │                    Measure_ (calc table — container for measures)
    │                    Tabla Rutas CTS (calc table — route summary)
    │                    7 calculated columns on fct_sales / dim_locations
    │                    10+ DAX measures
    └── Visuals:         2 report pages, 43 visuals total
```

---

## Naming map: dbt → Power BI

The dbt model names are **preserved as-is** when loaded into Power BI. Three additional tables are created with DAX inside the .pbix.

| Origin | Table | Where it lives |
|---|---|---|
| dbt mart | `fct_sales` | loaded via M from `data/fct_sales.csv` |
| dbt mart | `dim_customers` | loaded via M from `data/dim_customers.csv` |
| dbt mart | `dim_products` | loaded via M from `data/dim_products.csv` |
| dbt mart | `dim_locations` | loaded via M from `data/dim_locations.csv` |
| **PBI-added** | `Dim_Date` | DAX calc table (`CALENDAR(2024-01-01, 2024-12-31) + ADDCOLUMNS(...)`) |
| **PBI-added** | `Measure_` | DAX calc table — empty container that holds all explicit measures |
| **PBI-added** | `Tabla Rutas CTS` | DAX calc table — route-grain summary via `SUMMARIZE` |

---

## PBI-added DAX layer — the showcase

The DAX layer is where the BI work happens. Three categories:

### Calculated columns (defined in DAX, computed at refresh)

On `dim_locations`:
- `RouteID` — compact route code (`MTY-On-Hyp`-style)
- `Territory` — regional rollup (CDMX / GDL / MTY / Bajío / Sureste-Norte)
- `Segmento CTS` — CTS classification per route

On `fct_sales`:
- `DropBucket` — `>= $1,000` = Healthy, `>= $500` = Optimize, else Critical
- `CTS Index Col` — per-line CTS proxy `(cost/revenue) × (1 + lead_time_days/100)`
- `RouteID Corto` — FK column to join `Tabla Rutas CTS`
- `Segmento CTS Col` — per-line CTS segment label

> Full DAX bodies in [`Data_Dictionary.md`](Data_Dictionary.md#3-pbi-added-calculated-columns).

### Active DAX measures (10 in `Measure_` table)

| # | Measure | Purpose |
|---|---|---|
| 1 | `CTSIndex` | Cost-to-Serve index = `(cost/revenue) × (1 + lead_time_days/100)` — the central KPI |
| 2 | `Average Gross %` | `SUM(margin) / SUM(revenue)` aggregated margin |
| 3 | `Anual Average Gross` | Annual rollup of `Average Gross %` |
| 4 | `Drop Size Promedio` | Average ticket per invoice |
| 5 | `Desviacion Margen PP` | Margin deviation in percentage points vs. baseline |
| 6 | `Etiqueta CTS` | Formatted card label (▲/▼ + value) |
| 7 | `Etiqueta Drop Size` | Formatted Drop Size card label |
| 8 | `Estado Drop Size` | Status indicator (high/low vs. target) |
| 9 | `Foco Prioritario` | `SWITCH`-based recommendation |
| 10 | `Insight Drop Size` | Auto-generated insight string |

> The .pbix also contains inactive (orphan) measures that exist in the model but are not placed on any visual. Open the .pbix or run `inspect_vpax.py` (see `docs/`) to enumerate them.

---

## Theme

[`RTM_Theme.json`](RTM_Theme.json) — Looker-style theme using Google's Material palette. Comprehensive coverage (cards, bars, columns, lines, donut, slicer, tables, pivot). Apply via View → Themes → Browse for themes.

---

## Inspect the DAX yourself

The .pbix is shipped — open it directly. For programmatic inspection:

- **DAX Studio** → File → Connect → Power BI → select the open file → View Metrics → exports model.bim and a `.vpax` (VertiPaq Analyzer) with every measure, column, table, and relationship.
- **Tabular Editor** → File → Open → File... → select the .pbix → browse the model tree.
- **Power BI Desktop** → Model view, click any column/measure to see its DAX in the formula bar.

If you export a fresh `.vpax`, drop it in this folder — the project's audit scripts (`inspect_vpax.py` in the previous version of this repo) can ingest it to produce an active-vs-orphan inventory.

---

## What comes next

This is the final consumer step. Reports/decks built on top of the .pbix are in [`../outputs/`](../outputs/):

- `RTM_Performance_Analysis.pdf` — full analytical report
- `RTM_Ejecutivo_2024.pdf` — Spanish executive summary
- `charts/` — light-theme PNGs
- `charts_tech/` — dark-theme PNGs

The narrative writeup is in [`../docs/rtm_analysis.md`](../docs/rtm_analysis.md).
