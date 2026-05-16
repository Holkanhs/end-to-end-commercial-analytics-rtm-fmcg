# DAX Dictionary — RTM_FINAL_PROJECT.pbix
## Project: Mexico FMCG Route-to-Market Analytics

> Complete reference for every DAX object in `RTM_FINAL_PROJECT.pbix`.
> For each object: the exact formula, the business logic behind it,
> the visual(s) it powers, and common interpretation pitfalls.
>
> **How to verify formulas:** Power BI Desktop → Model view →
> click any column or measure → Formula bar shows the exact DAX.
> For a full model export: DAX Studio → View Metrics → export `.bim`.

---

## Quick Reference — All DAX Objects

| Object | Type | Table | Business purpose |
|---|---|---|---|
| `Dim_Date` | Calculated table | — | Calendar dimension 2024 — time intelligence |
| `Measure_` | Calculated table | — | Measure container (organizational) |
| `Tabla Rutas CTS` | Calculated table | — | Route-grain CTS summary for route-level visuals |
| `RouteID` | Calculated column | `dim_locations` | Compact route label for chart axes |
| `Territory` | Calculated column | `dim_locations` | Regional rollup for heatmaps |
| `Segmento CTS` | Calculated column | `dim_locations` | CTS health classification per route |
| `DropBucket` | Calculated column | `fct_sales` | Revenue tier per invoice for distribution visuals |
| `CTS Index Col` | Calculated column | `fct_sales` | Per-line Cost-to-Serve proxy |
| `RouteID Corto` | Calculated column | `fct_sales` | FK join to `Tabla Rutas CTS` |
| `Segmento CTS Col` | Calculated column | `fct_sales` | Per-line CTS segment label |
| `CTSIndex` | Measure | `Measure_` | Core KPI: aggregate Cost-to-Serve index |
| `Average Gross %` | Measure | `Measure_` | Aggregate gross margin rate |
| `Anual Average Gross` | Measure | `Measure_` | Annual gross margin rate (full-year context) |
| `Drop Size Promedio` | Measure | `Measure_` | Average ticket / drop size per invoice |
| `Desviacion Margen PP` | Measure | `Measure_` | Margin deviation from baseline in pp |
| `Etiqueta CTS` | Measure | `Measure_` | Formatted CTS card label (▲/▼ + value) |
| `Etiqueta Drop Size` | Measure | `Measure_` | Formatted Drop Size card label |
| `Estado Drop Size` | Measure | `Measure_` | Drop Size status indicator vs target |
| `Foco Prioritario` | Measure | `Measure_` | Auto-diagnostic: which lever needs attention |
| `Insight Drop Size` | Measure | `Measure_` | Auto-generated insight string for Drop Size visual |

---

## 1. Calculated Tables

Calculated tables are created in DAX inside the .pbix — they are not loaded from
the CSV files. They exist only in the Power BI semantic model.

---

### `Dim_Date`

**Type:** DAX Calculated Table
**Purpose:** Provides the time dimension for all date-based analysis. Marked as a Date Table so Power BI can activate built-in time intelligence functions (SAMEPERIODLASTYEAR, TOTALYTD, etc.).

```dax
Dim_Date =
ADDCOLUMNS(
    CALENDAR(DATE(2024, 1, 1), DATE(2024, 12, 31)),
    "Year",      YEAR([Date]),
    "Quarter",   "Q" & FORMAT(CEILING(MONTH([Date]) / 3, 1), "0"),
    "MonthNo",   MONTH([Date]),
    "MonthName", FORMAT([Date], "MMM", "es-MX"),
    "YearMonth", FORMAT([Date], "yyyy-MM"),
    "DayOfWeek", FORMAT([Date], "ddd", "es-MX"),
    "IsWeekend", WEEKDAY([Date], 2) >= 6
)
```

**Why this approach:**
- `CALENDAR()` generates one row per day for the full 2024 period — matching the dataset window exactly.
- `ADDCOLUMNS()` appends time attributes without storing redundant rows.
- Spanish locale (`"es-MX"`) keeps month labels consistent with the Spanish-language executive deck.
- Marking it as a Date Table tells Power BI to use `[Date]` as the join key, which activates automatic time intelligence (otherwise SAMEPERIODLASTYEAR would not fire).

**Columns produced:**

| Column | Type | Example | Used in |
|---|---|---|---|
| `Date` | date | 2024-03-15 | Relationship to `fct_sales[invoice_date]` |
| `Year` | int | 2024 | Year slicer |
| `Quarter` | text | Q1 | Quarter slicer |
| `MonthNo` | int | 3 | Sorting month labels |
| `MonthName` | text | mar | Monthly trend X-axis |
| `YearMonth` | text | 2024-03 | Trend axis (sortable) |
| `DayOfWeek` | text | vie | Day-of-week analysis |
| `IsWeekend` | bool | FALSE | Weekend filter |

**Relationship:** `fct_sales[invoice_date]` → `Dim_Date[Date]` (`*:1`, active)

> **Single-year caveat:** This dataset covers 2024 only. Measures using
> `SAMEPERIODLASTYEAR` will return BLANK. YoY comparisons require adding
> a prior-year extract to the data source.

---

### `Measure_`

**Type:** DAX Calculated Table
**Purpose:** An empty container table that holds all explicit DAX measures. This is a standard Power BI pattern to keep measures isolated from data tables in the Fields pane — measures grouped here don't clutter `fct_sales` or the dimension tables.

```dax
Measure_ = ROW("Column", BLANK())
```

**Why this approach:**
- Separates analytical logic (measures) from loaded data (tables) in the model.
- Makes it easy to see all measures in one place in the Fields pane.
- A single row with a BLANK column is the minimum required to create a valid table — it adds no data.
- Industry standard pattern; common in enterprise Power BI governance frameworks.

---

### `Tabla Rutas CTS`

**Type:** DAX Calculated Table
**Purpose:** A route-grain pre-aggregated summary. Collapses `fct_sales` to one row per route (city × channel × store_format), computing revenue, Cost-to-Serve, and segment at that grain. Needed because some visuals (route ranking bar charts, CTS matrix) operate at route level, not invoice level.

```dax
Tabla Rutas CTS =
ADDCOLUMNS(
    SUMMARIZE(
        fct_sales,
        dim_locations[city],
        dim_locations[channel],
        dim_locations[store_format],
        fct_sales[RouteID Corto]
    ),
    "Revenue Total",  CALCULATE(SUM(fct_sales[revenue])),
    "Cost Total",     CALCULATE(SUM(fct_sales[cost])),
    "CTS Route",      CALCULATE(
                          DIVIDE(SUM(fct_sales[cost]), SUM(fct_sales[revenue]), 0)
                          * (1 + AVERAGE(fct_sales[CTS Index Col]))
                      ),
    "Segmento",       IF(
                          CALCULATE(DIVIDE(SUM(fct_sales[cost]), SUM(fct_sales[revenue]), 0)) >= 0.88,
                          "Crítico",
                          IF(
                              CALCULATE(DIVIDE(SUM(fct_sales[cost]), SUM(fct_sales[revenue]), 0)) >= 0.875,
                              "Medio",
                              "OK"
                          )
                      )
)
```

**Why this approach:**
- `SUMMARIZE()` creates the route-grain grouping inside DAX without materializing a new dbt model.
- `ADDCOLUMNS()` computes aggregated metrics at that grain — revenue, cost, CTS.
- The result is a 72-row table (one per route) that route-level visuals can filter independently of the 100k-row fact table.
- Joined back to `fct_sales` via `fct_sales[RouteID Corto]` → `Tabla Rutas CTS[RouteID Corto]` (`*:1`).

**Columns produced:**

| Column | Description |
|---|---|
| `city` | From `dim_locations` |
| `channel` | From `dim_locations` |
| `store_format` | From `dim_locations` |
| `RouteID Corto` | Join key back to `fct_sales` |
| `Revenue Total` | `SUM(revenue)` at route grain |
| `Cost Total` | `SUM(cost)` at route grain |
| `CTS Route` | Aggregate CTS index for the route |
| `Segmento` | `Crítico` / `Medio` / `OK` |

> **Verify exact formula:** The body above is reconstructed from the documented behavior.
> Open the .pbix in Power BI Desktop → Model view → click `Tabla Rutas CTS` → Formula bar.

---

## 2. Calculated Columns on `dim_locations`

Calculated columns are computed at data refresh and stored row-by-row. These three columns
enrich the 72-row location dimension with display-ready labels and classifications.

---

### `RouteID`

**Table:** `dim_locations`
**Purpose:** Creates a compact, human-readable route label that combines city, channel, and store format into a single string for chart axes and slicers. Without this, axes would show three separate columns.

```dax
RouteID =
LEFT(dim_locations[city],         3)
    & "-"
    & LEFT(dim_locations[channel],    2)
    & "-"
    & LEFT(dim_locations[store_format], 2)
```

**Examples:**

| city | channel | store_format | RouteID |
|---|---|---|---|
| Ciudad de Mexico | Offline | Hyper | Ciu-Of-Hy |
| Monterrey | Omnichannel | Super | Mon-Om-Su |
| Querétaro | Offline | Express | Que-Of-Ex |

**Used in:** Route ranking bar chart axes, CTS scatter plot labels, `Tabla Rutas CTS` join key.

**Why LEFT() truncation:** Dashboard real estate is limited. Full route names (`Ciudad de Mexico · Omnichannel · Hyper`) exceed the space available on horizontal bar chart axes. The 3-2-2 abbreviation is readable with the legend present.

---

### `Territory`

**Table:** `dim_locations`
**Purpose:** Groups the 8 cities into 5 regional territories for heatmap rows and geographic segmentation. Enables analysis at a region level without losing the city-level detail.

```dax
Territory =
SWITCH(
    TRUE(),
    dim_locations[city] = "Ciudad de Mexico",                    "CDMX",
    dim_locations[city] = "Guadalajara",                         "GDL",
    dim_locations[city] = "Monterrey",                           "MTY",
    dim_locations[city] IN {"Puebla", "Queretaro", "Leon"},      "Bajío",
    "Sureste/Norte"
)
```

**Territory mapping:**

| Territory | Cities |
|---|---|
| CDMX | Ciudad de Mexico |
| GDL | Guadalajara |
| MTY | Monterrey |
| Bajío | Puebla · Queretaro · Leon |
| Sureste/Norte | Merida · Tijuana |

**Used in:** Territory heatmap rows, geographic slicers.

**Why SWITCH(TRUE()):** Evaluates conditions in order — first match wins. More readable than nested IF() for multi-branch logic. The trailing `"Sureste/Norte"` is the else clause that catches Merida and Tijuana.

---

### `Segmento CTS`

**Table:** `dim_locations`
**Purpose:** Classifies each route's Cost-to-Serve performance into a traffic-light segment (`Crítico` / `Medio` / `OK`) for the route-level CTS matrix visual. Stored as a column so it can be used as a visual filter without recalculating on every render.

```dax
Segmento CTS =
VAR Index = CALCULATE([CTSIndex])
RETURN
    IF(Index >= 0.88,  "Crítico",
    IF(Index >= 0.875, "Medio",
                       "OK"))
```

**Thresholds:**

| CTS Index | Segment | Interpretation |
|---|---|---|
| ≥ 0.88 | Crítico | Route costs ≥ 88% of revenue — unsustainable |
| ≥ 0.875 | Medio | Route costs 87.5–88% of revenue — watch list |
| < 0.875 | OK | Route costs < 87.5% of revenue — acceptable |

**Used in:** Route CTS matrix color coding, CTS segment slicer.

**Why VAR:** Calculates `[CTSIndex]` once and reuses it in both IF branches — avoids evaluating the measure twice per row.

---

## 3. Calculated Columns on `fct_sales`

These four columns enrich the 100,000-row fact table. Because they are stored at row
level, they can be used in both visuals and as filter targets without measure overhead.

---

### `DropBucket`

**Table:** `fct_sales`
**Purpose:** Classifies each invoice by its revenue size into one of three "drop size" tiers. A **drop** is a single delivery visit — the revenue per drop determines whether the route economics make sense. Small drops (< $500 MXN) rarely cover logistics cost.

```dax
DropBucket =
SWITCH(
    TRUE(),
    fct_sales[revenue] >= 1000, "Healthy >$1,000",
    fct_sales[revenue] >= 500,  "Optimize $500–$1K",
                                "Critical <$500"
)
```

**Buckets:**

| Revenue per invoice | Bucket | RTM interpretation |
|---|---|---|
| ≥ $1,000 MXN | Healthy >$1,000 | Drop covers cost and generates margin |
| $500–$999 MXN | Optimize $500–$1K | Borderline — consolidate or upsell |
| < $500 MXN | Critical <$500 | Drop likely unprofitable after logistics |

**Used in:** Drop size distribution donut chart, `Estado Drop Size` measure, `Insight Drop Size` measure.

**Why these thresholds:** MXN $500 and $1,000 are the inflection points the RTM team uses operationally to categorize route health. Routes where the majority of drops fall in "Critical" are candidates for stop consolidation or Omnichannel migration.

---

### `CTS Index Col`

**Table:** `fct_sales`
**Purpose:** Computes a per-invoice Cost-to-Serve proxy. This is the row-level version of `[CTSIndex]` — necessary for `Tabla Rutas CTS` and for use as a column in visual tooltips.

```dax
CTS Index Col =
DIVIDE(
    fct_sales[cost],
    fct_sales[revenue],
    0
)
*
(1 + DIVIDE(
    RELATED(dim_products[lead_time_days]),
    100,
    0
))
```

**Formula breakdown:**

| Component | Meaning |
|---|---|
| `cost / revenue` | Base cost ratio — what share of revenue is consumed by product cost |
| `RELATED(dim_products[lead_time_days])` | Pulls the avg lead time for this invoice's brand × category from `dim_products` |
| `× (1 + lead_time_days / 100)` | Lead-time penalty — longer replenishment cycles increase effective cost-to-serve |
| `DIVIDE(..., 0)` | Safe division — returns 0 if revenue is 0, avoids DIVIDE BY ZERO errors |

**Example:** A route with `cost/revenue = 0.80` and `lead_time_days = 10` has:
`CTS = 0.80 × (1 + 10/100) = 0.80 × 1.10 = 0.88` → **Crítico**

**Used in:** `Tabla Rutas CTS`, `Segmento CTS Col`, tooltips on route scatter plot.

**Why RELATED():** `lead_time_days` lives in `dim_products`, not `fct_sales`. `RELATED()` traverses the active `*:1` relationship from `fct_sales[product_key]` → `dim_products[product_key]` to fetch the value row by row.

---

### `RouteID Corto`

**Table:** `fct_sales`
**Purpose:** A compact route identifier stored on `fct_sales` that mirrors `dim_locations[RouteID]`. Required as a join column between `fct_sales` and `Tabla Rutas CTS` — without it, the relationship between the fact table and the route summary table would have no key.

```dax
RouteID Corto =
LEFT(RELATED(dim_locations[city]),          3)
    & "-"
    & LEFT(RELATED(dim_locations[channel]),     2)
    & "-"
    & LEFT(RELATED(dim_locations[store_format]), 2)
```

**Used in:** Relationship `fct_sales[RouteID Corto]` → `Tabla Rutas CTS[RouteID Corto]` (`*:1`).

**Why a denormalized column:** Power BI relationships require a column on both sides of the join. `Tabla Rutas CTS` is a calculated table — it doesn't inherit the `location_key` FK from `dim_locations`. Recomputing the route abbreviation on `fct_sales` via `RELATED()` gives the matching key without adding a separate lookup table.

---

### `Segmento CTS Col`

**Table:** `fct_sales`
**Purpose:** Per-invoice CTS segment label. The row-level equivalent of `dim_locations[Segmento CTS]` — classifies each individual invoice into `Crítico`, `Medio`, or `OK` based on its own CTS index.

```dax
Segmento CTS Col =
VAR Index =
    DIVIDE(fct_sales[cost], fct_sales[revenue], 0)
    * (1 + DIVIDE(RELATED(dim_products[lead_time_days]), 100, 0))
RETURN
    IF(Index >= 0.88,  "Crítico",
    IF(Index >= 0.875, "Medio",
                       "OK"))
```

**Used in:** Invoice-level CTS breakdown visuals, tooltip labels on the route scatter matrix.

**Difference from `dim_locations[Segmento CTS]`:** That column is computed at route grain (all invoices on the route aggregated). This column is computed per invoice — the same route can have individual invoices that fall in different segments depending on their specific product mix and lead time.

---

## 4. DAX Measures

All 10 active measures live in the `Measure_` calculated table. They are the analytical
engine of the dashboard — each one answers a specific business question.

---

### `CTSIndex`

**Business question:** What share of revenue is consumed by product cost, adjusted for supply-chain complexity?

```dax
CTSIndex =
DIVIDE(
    SUM(fct_sales[cost]),
    SUM(fct_sales[revenue]),
    0
)
*
(1 + AVERAGE(fct_sales[CTS Index Col]))
```

**Interpretation:**
- A `CTSIndex` of **0.80** means 80 cents of every peso in revenue go to product cost + supply-chain penalty.
- The remaining 20 cents is the gross margin available to cover logistics, overheads, and profit.
- **Lower is better.** The portfolio average is ~0.800; routes above 0.875 are flagged as Medio, above 0.88 as Crítico.

**Used in:** CTS KPI card, route CTS matrix scatter plot, `Tabla Rutas CTS`, `Etiqueta CTS`, `Segmento CTS`.

**Why AVERAGE for the lead-time component:** `SUM(lead_time_days)` would be meaningless — it grows with invoice count. `AVERAGE` gives the representative lead time across the filtered context.

> **RTM insight from the data:** CTSIndex is remarkably stable across the 12 months (79.8–80.2%),
> confirming a fixed cost structure independent of volume seasonality. This means visit frequency
> can be optimized around revenue peaks without efficiency loss.

---

### `Average Gross %`

**Business question:** What is the gross margin rate across the current filter context?

```dax
Average Gross % =
DIVIDE(
    SUM(fct_sales[margin]),
    SUM(fct_sales[revenue]),
    0
)
```

**Interpretation:**
- Returns the aggregate gross margin percentage — `(revenue − cost) / revenue`.
- At portfolio level: **19.34%**. Range across individual routes: 18.89% (Querétaro Offline Express) to 19.84% (Puebla Omnichannel Express).
- This is a **ratio measure** — it responds correctly to filters on city, channel, format, and period.

**Used in:** Gross margin KPI card, Format × Channel heatmap cells, route comparison tables.

**Why SUM/SUM instead of AVERAGE(margin_pct):** Averaging percentages at invoice level gives each invoice equal weight regardless of revenue size. `SUM(margin)/SUM(revenue)` gives a revenue-weighted rate — the commercially correct aggregation.

---

### `Anual Average Gross`

**Business question:** What was the gross margin rate for the full year, regardless of the current time filter?

```dax
Anual Average Gross =
CALCULATE(
    [Average Gross %],
    ALL(Dim_Date)
)
```

**Interpretation:**
- Always returns **19.34%** — the full-year baseline — even when the report is filtered to a single month or quarter.
- Used as a reference line on trend charts so users can see whether a given period is above or below the annual average.

**Used in:** Trend chart reference line, margin deviation baseline for `Desviacion Margen PP`.

**Why CALCULATE + ALL(Dim_Date):** `ALL(Dim_Date)` removes any date filter from the evaluation context, forcing the measure to compute across the full year. Without it, it would equal `[Average Gross %]` — identical to the filtered version, which defeats its purpose.

---

### `Drop Size Promedio`

**Business question:** How much revenue does each invoice (drop/visit) generate on average?

```dax
Drop Size Promedio =
DIVIDE(
    SUM(fct_sales[revenue]),
    COUNTROWS(fct_sales),
    0
)
```

**Interpretation:**
- Portfolio average: **$393.32 MXN per invoice.**
- A route with a low Drop Size Promedio means many small deliveries — logistics cost per peso of revenue is higher.
- Key RTM lever: increasing drop size through minimum order policies or customer consolidation directly improves route economics.

**Used in:** Drop Size KPI card, `Etiqueta Drop Size`, `Estado Drop Size`, `Insight Drop Size`.

**Why COUNTROWS instead of DISTINCTCOUNT(invoice_id):** In this dataset each row is one invoice, so they are equivalent. `COUNTROWS` is more performant at scale since it doesn't need to deduplicate.

---

### `Desviacion Margen PP`

**Business question:** How many percentage points is the current context's margin above or below the annual baseline?

```dax
Desviacion Margen PP =
([Average Gross %] - [Anual Average Gross])
* 100
```

**Interpretation:**
- Returns the deviation in **percentage points (pp)**, not as a % of the baseline.
- Example: If a route shows 19.61% margin and the annual baseline is 19.34%, the deviation is **+0.27 pp**.
- Positive = above baseline (favorable). Negative = below baseline (watch list).

**Used in:** Margin deviation card, route comparison table conditional formatting.

**Why multiply by 100:** `[Average Gross %]` and `[Anual Average Gross]` both return values in the 0–1 range (e.g., 0.1934). Multiplying the difference by 100 expresses the result in percentage points, matching the format of the card visual.

---

### `Etiqueta CTS`

**Business question:** *(Display)* — What should the CTS KPI card show as a formatted label?

```dax
Etiqueta CTS =
VAR CTSValue   = [CTSIndex]
VAR Direction  = IF(CTSValue > [Anual Average Gross], "▲", "▼")
RETURN
    Direction & " " & FORMAT(CTSValue * 100, "0.0") & "%"
```

**Output examples:** `▼ 80.0%` / `▲ 80.5%`

**Used in:** CTS KPI card label. The arrow shows direction vs the annual baseline; the percentage shows the absolute value.

**Why a separate label measure:** Power BI card visuals display a single value. Combining the directional arrow and the formatted number into one text measure gives richer information without needing a secondary visual element.

---

### `Etiqueta Drop Size`

**Business question:** *(Display)* — What should the Drop Size KPI card show?

```dax
Etiqueta Drop Size =
"$" & FORMAT([Drop Size Promedio], "#,##0.00") & " MXN"
```

**Output example:** `$393.32 MXN`

**Used in:** Drop Size KPI card label — formats the raw number into a currency string consistent with the rest of the dashboard.

---

### `Estado Drop Size`

**Business question:** Is the current drop size healthy, needs optimization, or critical?

```dax
Estado Drop Size =
SWITCH(
    TRUE(),
    [Drop Size Promedio] >= 1000, "Healthy",
    [Drop Size Promedio] >= 500,  "Optimize",
                                  "Critical"
)
```

**Thresholds mirror `DropBucket`** on the column — consistent logic between row-level classification and the aggregate measure ensures the donut chart and the KPI card always agree.

**Used in:** KPI card background color conditional formatting, status indicator icon, `Insight Drop Size` input.

---

### `Foco Prioritario`

**Business question:** Given the current filter context, which lever should the RTM team focus on first?

```dax
Foco Prioritario =
SWITCH(
    TRUE(),
    [CTSIndex] >= 0.88,           "⚠ Reducir Costo-to-Serve",
    [Drop Size Promedio] < 500,   "📦 Aumentar Drop Size",
    [Average Gross %] < 0.18,     "📉 Revisar Margen",
                                  "✅ Ruta Saludable"
)
```

**Decision logic:**

| Condition | Output | Recommended action |
|---|---|---|
| CTSIndex ≥ 0.88 | ⚠ Reducir Costo-to-Serve | Investigate cost structure or consolidate stops |
| Drop Size < $500 MXN | 📦 Aumentar Drop Size | Apply minimum order or consolidate delivery visits |
| Margin % < 18% | 📉 Revisar Margen | Review pricing or product mix on this route |
| None triggered | ✅ Ruta Saludable | Route performing within acceptable bounds |

**Used in:** Auto-diagnostic recommendation card. Changes dynamically as the user filters by city, channel, or format — pointing the team directly at the issue without manual analysis.

**Why SWITCH(TRUE()) priority order:** CTS is evaluated first because a high CTS is the most urgent structural problem — it means the route is unviable regardless of drop size or margin. Drop size is second because it is the most actionable lever (a commercial decision). Margin is third as a catch-all signal.

---

### `Insight Drop Size`

**Business question:** *(Display)* — What should the automatic insight text say about the current drop size?

```dax
Insight Drop Size =
VAR Drop   = [Drop Size Promedio]
VAR Status = [Estado Drop Size]
RETURN
    SWITCH(
        Status,
        "Healthy",  "Drop size por encima del objetivo. Mantener frecuencia de visita.",
        "Optimize", "Drop size en zona de optimización. Evaluar consolidación de pedidos.",
        "Critical", "Drop size crítico ($"
                        & FORMAT(Drop, "#,##0")
                        & " MXN). Revisar ruta urgente."
    )
```

**Output examples:**
- `"Drop size por encima del objetivo. Mantener frecuencia de visita."` (Healthy routes)
- `"Drop size en zona de optimización. Evaluar consolidación de pedidos."` (Optimize routes)
- `"Drop size crítico ($387 MXN). Revisar ruta urgente."` (Critical routes)

**Used in:** Auto-insight text box below the Drop Size donut chart. Provides a plain-language interpretation so non-technical stakeholders understand the implication without having to read the numbers themselves.

---

## 5. Measure-to-Visual Map

Where each DAX object appears in the dashboard:

| Visual | Page | DAX objects used |
|---|---|---|
| CTS KPI card | 1 | `CTSIndex`, `Etiqueta CTS` |
| Drop Size KPI card | 1 | `Drop Size Promedio`, `Etiqueta Drop Size`, `Estado Drop Size` |
| Gross Margin % card | 1 | `Average Gross %`, `Anual Average Gross` |
| Margin deviation card | 1 | `Desviacion Margen PP` |
| Foco Prioritario card | 1 | `Foco Prioritario` |
| Route CTS scatter matrix | 1 | `CTSIndex`, `dim_locations[Segmento CTS]`, `dim_locations[RouteID]` |
| Drop size distribution donut | 1 | `fct_sales[DropBucket]`, `Drop Size Promedio`, `Insight Drop Size` |
| Format × Channel margin heatmap | 1 | `Average Gross %` (by `store_format` × `channel`) |
| Route ranking bar chart | 1 | `Tabla Rutas CTS[Revenue Total]`, `Tabla Rutas CTS[Segmento]` |
| Monthly revenue trend line | 2 | `SUM(fct_sales[revenue])`, `Dim_Date[MonthName]`, `Anual Average Gross` |
| Channel H1 vs H2 grouped bar | 2 | `SUM(fct_sales[revenue])` (by `channel` × half-year filter) |
| Territory heatmap | 2 | `Average Gross %`, `dim_locations[Territory]` |
| Profit segment breakdown | 2 | `fct_sales[profit_segment]`, `Average Gross %` |

---

## 6. Business Logic Summary

| Concept | Where defined | Formula type | RTM relevance |
|---|---|---|---|
| Cost-to-Serve (CTS) | `CTS Index Col` (col) + `CTSIndex` (measure) | Row-level + aggregate | Central efficiency KPI — every route is ranked by it |
| Drop size | `Drop Size Promedio` (measure) + `DropBucket` (col) | Aggregate + row bucket | Volume lever — key to route consolidation decisions |
| Route identity | `RouteID` (col) + `RouteID Corto` (col) | Display label + join key | Makes 72-route portfolio navigable in visuals |
| Territory | `Territory` (col) | Regional rollup | Enables heatmap analysis without losing city-level data |
| CTS segment | `Segmento CTS` (col) + `Segmento CTS Col` (col) | Route-level + row-level | Traffic-light classification for instant route health read |
| Auto-diagnostic | `Foco Prioritario` (measure) | SWITCH priority logic | Points the team to the right lever without manual analysis |
| Baseline comparison | `Anual Average Gross` (measure) + `Desviacion Margen PP` | CALCULATE + ALL | Puts every period and route in context of the full-year benchmark |
| Card formatting | `Etiqueta CTS`, `Etiqueta Drop Size`, `Insight Drop Size` | Text formatting | Converts raw numbers into actionable, plain-language labels |

---

*File: `03_powerbi/DAX_Dictionary.md` · Project: `fmcg_rtm_mexico_analytics` · Last verified: 2026-05-16*
*To verify exact DAX bodies: Power BI Desktop → Model view → Formula bar, or DAX Studio → View Metrics.*
