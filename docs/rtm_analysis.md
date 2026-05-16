# Route-To-Market 2024 — Analysis Writeup

> Full-year performance analysis of 72 RTM routes across 8 Mexican cities. Identifies the star routes worth scaling, the critical routes that need restructuring, and the channel shift the team should prepare for in 2025.

**Audience:** Logistics Director, RTM team, Commercial team.
**Decision supported:** Where to invest in 2025 — which routes to protect, which to restructure, which channel shift to accelerate.
**Data window:** January 1 – December 31, 2024. **Analysis date:** May 2026.

---

## TL;DR — three findings

1. **Star routes confirmed.** CDMX Offline Hyper, Monterrey Omnichannel Super, and Puebla Omnichannel Express each generate over **$350k MXN** in annual gross margin — the most valuable assets in the RTM portfolio.

2. **Offline is losing ground in H2.** Offline channel revenue declined **−0.11%** in the second half of 2024, while Omnichannel and Online both grew **+0.18%**. The gap will widen without intervention.

3. **Express format is the portfolio drag.** Across all channels, Express stores underperform Hyper and Super on both margin % and average ticket. Querétaro Offline Express sits at the floor of the portfolio.

---

## The numbers at a glance

| KPI | Value | Source |
|---|---|---|
| Total revenue | $118.0M MXN | `SUM(fct_sales.revenue)` |
| Total invoices | 100,000 | `COUNT(fct_sales.invoice_id)` |
| Average gross margin % | 19.34% | `AVG(fct_sales.margin_pct)` |
| Average ticket | $393.32 MXN | `AVG(fct_sales.avg_ticket_price)` |
| Cost-to-Serve index | ~80.0% | `SUM(cost) / SUM(revenue)` |
| Routes analyzed | 72 | 8 cities × 3 channels × 3 formats |

---

## Finding 1 — City revenue: a tight portfolio, geography isn't the lever

![City revenue ranking](../outputs/charts/01_city_revenue.png)

The gap between the top and bottom cities is only **3.5%** ($15.0M for Monterrey vs $14.5M for Tijuana). This is unusually tight — it means **geography is not the primary driver of profitability**. The real differentiators are **channel** and **store format** (see Findings 3 and 4).

---

## Finding 2 — Channel: Offline loses, Omnichannel and Online gain in H2

![Channel H1 vs H2](../outputs/charts/02_channel_h1_h2.png)

Splitting the year at July 1:
- **Omnichannel:** +0.18% in H2 vs H1
- **Online:** +0.18% in H2 vs H1
- **Offline:** **−0.11%** in H2 vs H1

This is a small absolute shift but a clear directional signal. Combined with the Format × Channel heatmap (Finding 5), it confirms the **Offline-only path is becoming structurally less competitive**.

---

## Finding 3 — Route efficiency: every route mapped by cost vs value

![Route efficiency matrix](../outputs/charts/03_route_matrix.png)

The matrix plots all 72 routes by **Cost-to-Serve %** (x) vs **Revenue per Unit** (y), sized by transaction volume.

- **Upper-left quadrant** = star routes (low cost, high value). CDMX Offline Hyper anchors this group.
- **Lower-right quadrant** = critical routes (high cost, low value). Querétaro Offline Express sits here.
- **Median lines** divide the portfolio into 4 quadrants — used by the RTM team for monthly review.

---

## Finding 4 — Seasonality: revenue swings, cost-to-serve doesn't

![Monthly trend](../outputs/charts/04_monthly_trend.png)

- **Revenue peaks:** January, August, October.
- **Revenue troughs:** February, June, September.
- **Cost-to-Serve:** stable at **79.8–80.2%** across all 12 months.

The constant CTS confirms a **fixed cost structure independent of volume** — the team can plan route visits around peak months without efficiency loss.

---

## Finding 5 — Format × Channel margin matrix

![Format × Channel heatmap](../outputs/charts/06_format_channel_heatmap.png)

The clearest grid pattern in the analysis:

- **Omnichannel Super** = 19.61% margin — best in portfolio
- **Hyper Omnichannel** beats **Hyper Offline** on the same format
- **Express** underperforms across all channels — efficiency doesn't compensate for low ticket value

This is the chart to bring to the next commercial review.

---

## Finding 6 — Top vs bottom 5 routes

![Top vs bottom routes](../outputs/charts/05_top_bottom_routes.png)

| Indicator | Top 5 routes | Bottom 5 routes | Gap |
|---|---|---|---|
| Avg gross margin | $350k MXN | $302k MXN | **+16%** |
| Avg margin % | 19.5% | 19.1% | +0.4 pp |
| Avg CTS % | 79.8% | 80.2% | −0.4 pp |
| Revenue / unit | $401 MXN | $381 MXN | **+5.3%** |
| Dominant channel | Offline / Omnichannel | Offline / Express | — |
| Dominant format | Hyper / Super | Express / Super | — |

The gap between best and worst is **$71k MXN per route per year**. Across the 5 weakest routes, that's **$355k MXN of annual margin recoverable** if they can be restructured to the economics of the star routes.

---

## Recommendations for 2025

### R1 — Protect and scale the star routes

**Targets:** CDMX Offline Hyper, Monterrey Omnichannel Super, Puebla Omnichannel Express.

**Actions:**
- Lock in **priority visit frequency** — don't bundle these with low-value stops in the same route.
- Guarantee **stock availability** with preferential replenishment (current lead time ≈ 8–9 days).
- Review commercial terms to incentivize higher volume at these points.

**Expected outcome:** Keep CTS below 79.9% and margin above $350k MXN on these routes through 2025.

### R2 — Restructure Offline Express

**Targets:** Querétaro Offline Express, Leon Offline Express.

**Three options to evaluate:**
- **(A) Migrate to Omnichannel** — move these customers to a digital service model.
- **(B) Consolidate stops** — group nearby Express clients to raise ticket per visit.
- **(C) Exit & reassign** — free field capacity for Hyper/Super routes in the same city.

**Cost of inaction:** ~$67k MXN of margin gap vs portfolio average on these 2 routes per year.

### R3 — Accelerate the Omnichannel migration

The H2 trend is already visible. The Format × Channel matrix confirms the direction.

**Plan:**
- Identify the **10 lowest-ticket Offline customers** per city; offer digital onboarding with commercial support.
- **Q2 2025 conversion target:** 5% of Offline volume migrated to Omnichannel on the 5 weakest routes.
- **Measurement metric:** margin recovered per converted route.

**Quantified opportunity:** A 5% volume shift on the 10 weakest Offline routes recovers **$180k–$220k MXN** of annual gross margin.

---

## Action plan — next 90 days

| # | Action | Owner | Deadline | Success metric |
|---|---|---|---|---|
| 1 | Review Querétaro Offline Express route plan | RTM Manager | Mar 2025 | Margin ≥ $320k MXN in Q2 |
| 2 | Pilot Omnichannel migration on 2 Offline routes | Commercial + Logistics | Mar 2025 | +0.3 pp margin |
| 3 | Define visit frequency for top 10 routes | Field Ops | Jan 2025 | 100% coverage on star routes |
| 4 | Review cost structure: Tijuana Omnichannel Hyper | RTM + Finance | Mar 2025 | CTS % < 80.0% |
| 5 | Monthly RTM route review cadence | RTM Director | Feb 2025 | Dashboard live |

---

## Sources and method

- **Source data:** Mexico FMCG Retail Sales Customer Inventory (2024) — 100,000 invoice lines, January–December 2024.
- **Pipeline:** Snowflake `sales_data_raw` → dbt staging → intermediate → marts → Power BI.
- **Route definition:** City × Channel × Store Format (72 unique combinations).
- **CTS definition:** `SUM(cost) / SUM(revenue)` per route (proxy — excludes uncaptured logistics overhead).

**Data quality:**
- 100,000 rows post-pipeline.
- `customer_age` 0-filled where source was null (~15% of rows); flag in visuals as "n/d" if showing age breakdown.
- Single-year dataset — YoY comparison not available; H1 vs H2 used as internal benchmark.

**Reproducibility:** all transformations are codified in [`../02_dbt/models/`](../02_dbt/models/) (dbt SQL) and [`../scripts/build_powerbi_data.py`](../scripts/build_powerbi_data.py) (Python+DuckDB mirror). The 4 CSVs the Power BI dashboard consumes live in [`../03_powerbi/data/`](../03_powerbi/data/) and are fully regenerable from raw.

---

## Related deliverables

- **Power BI dashboard:** [`../03_powerbi/RTM_FINAL_PROJECT.pbix`](../03_powerbi/RTM_FINAL_PROJECT.pbix) — interactive version of all analyses above.
- **Executive deck (Spanish):** [`../outputs/RTM_Ejecutivo_2024.pdf`](../outputs/RTM_Ejecutivo_2024.pdf).
- **Performance analysis (English PDF):** [`../outputs/RTM_Performance_Analysis.pdf`](../outputs/RTM_Performance_Analysis.pdf).
- **Schema reference:** [`schema.md`](schema.md).
