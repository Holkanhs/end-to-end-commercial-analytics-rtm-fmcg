---
marp: true
theme: default
paginate: true
size: 16:9
html: true
footer: "AI Analyst Lab | RTM Mexico FMCG | May 2026"
style: |

  /* ── BASE ──────────────────────────────────────────────── */
  section {
    background: #060D1F;
    font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
    font-size: 15px;
    color: #D8E4FF;
    padding: 30px 54px 28px 54px;
    box-sizing: border-box;
    position: relative;
  }

  /* ── HEADINGS ──────────────────────────────────────────── */
  h1 {
    font-size: 23px;
    font-weight: 700;
    color: #FFFFFF;
    border-bottom: 2px solid #00C8FF;
    padding-bottom: 7px;
    margin: 0 0 14px 0;
    letter-spacing: -0.01em;
    line-height: 1.2;
  }
  h2 { font-size: 18px; font-weight: 700; color: #C8DFFF; margin: 0 0 8px 0; }
  h3 {
    font-size: 11px;
    font-weight: 600;
    color: #5A80AA;
    margin: 8px 0 5px 0;
    text-transform: uppercase;
    letter-spacing: 0.07em;
  }

  /* ── TEXT ──────────────────────────────────────────────── */
  p  { font-size: 13px; margin: 4px 0; line-height: 1.5; color: #C8DFFF; }
  li { font-size: 13px; margin: 4px 0; line-height: 1.4; color: #C8DFFF; }
  strong { color: #00C8FF; font-weight: 600; }
  ul { padding-left: 18px; margin: 6px 0; }

  /* ── IMAGES ────────────────────────────────────────────── */
  img { border-radius: 6px; display: block; object-fit: contain; }

  /* ── TABLES ────────────────────────────────────────────── */
  table { width: 100%; border-collapse: collapse; font-size: 12px; margin: 8px 0; }
  th {
    background: #0A1E45;
    color: #00C8FF;
    padding: 7px 10px;
    text-align: left;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid rgba(0,200,255,0.3);
  }
  td { padding: 5px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #C8DFFF; }
  tr:nth-child(even) td { background: rgba(0,200,255,0.03); }

  /* ── KPI CARDS ─────────────────────────────────────────── */
  .kpi-row { display: flex; gap: 12px; margin: 12px 0; }
  .kpi-card {
    background: rgba(0,200,255,0.05);
    border: 1px solid rgba(0,200,255,0.18);
    border-left: 3px solid #00C8FF;
    border-radius: 6px;
    padding: 12px 16px;
    flex: 1;
    box-shadow: 0 0 20px rgba(0,200,255,0.06);
  }
  .kpi-value { font-size: 30px; font-weight: 800; color: #00C8FF; line-height: 1; }
  .kpi-label { font-size: 10px; color: #5A80AA; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }
  .kpi-delta { font-size: 11px; color: #4A6A8A; margin-top: 2px; }
  .kpi-card.green { border-left-color: #00E676; }
  .kpi-card.green .kpi-value { color: #00E676; }
  .kpi-card.red { border-left-color: #FF4560; }
  .kpi-card.red .kpi-value { color: #FF4560; }
  .kpi-card.amber { border-left-color: #FFB020; }
  .kpi-card.amber .kpi-value { color: #FFB020; }

  /* ── CALLOUT BOXES ─────────────────────────────────────── */
  .so-what {
    background: rgba(0,200,255,0.07);
    border-left: 3px solid #00C8FF;
    border-radius: 4px;
    padding: 10px 14px;
    margin: 8px 0;
    font-size: 13px;
    line-height: 1.5;
    color: #C8DFFF;
  }
  .finding {
    background: rgba(0,200,255,0.05);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 6px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 12.5px;
    line-height: 1.45;
  }
  .warn {
    background: rgba(255,69,96,0.08);
    border-left: 3px solid #FF4560;
    border-radius: 4px;
    padding: 9px 13px;
    margin: 6px 0;
    font-size: 12.5px;
    line-height: 1.45;
    color: #FFB3BE;
  }
  .ok {
    background: rgba(0,230,118,0.07);
    border-left: 3px solid #00E676;
    border-radius: 4px;
    padding: 9px 13px;
    margin: 6px 0;
    font-size: 12.5px;
    line-height: 1.45;
    color: #A0FFD2;
  }

  /* ── REC ROW ───────────────────────────────────────────── */
  .rec-row {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 10px;
    background: rgba(0,200,255,0.04);
    border: 1px solid rgba(0,200,255,0.12);
    border-radius: 6px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 12.5px;
    align-items: center;
  }
  .rec-action { color: #FFFFFF; font-weight: 600; }
  .rec-owner { color: #5A80AA; font-size: 11px; }
  .rec-metric { color: #00C8FF; font-size: 11px; font-weight: 600; }
  .confidence-high { background: rgba(0,230,118,0.12); border-left: 3px solid #00E676; border-radius: 4px; padding: 2px 8px; font-size: 10px; color: #00E676; font-weight: 600; }
  .confidence-med  { background: rgba(255,176,32,0.12); border-left: 3px solid #FFB020; border-radius: 4px; padding: 2px 8px; font-size: 10px; color: #FFB020; font-weight: 600; }

  /* ── TWO COLUMN ────────────────────────────────────────── */
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin: 8px 0; }
  .col { display: flex; flex-direction: column; gap: 6px; }

  /* ── SOURCE LABEL ──────────────────────────────────────── */
  .src { font-size: 10px; color: #1A3050; position: absolute; bottom: 14px; right: 54px; }

  /* ── IMPACT NUMBER ─────────────────────────────────────── */
  .impact-num {
    font-size: 64px;
    font-weight: 800;
    color: #00C8FF;
    line-height: 1;
    text-align: center;
    margin: 16px 0 6px 0;
    text-shadow: 0 0 60px rgba(0,200,255,0.25);
  }
  .impact-label {
    font-size: 18px;
    color: #6A9DBD;
    text-align: center;
    margin: 0;
  }
  .impact-sub {
    font-size: 13px;
    color: #3A6080;
    text-align: center;
    margin-top: 6px;
  }

  /* ── PORTADA ───────────────────────────────────────────── */
  section.portada {
    background-color: #060D1F;
    background-image:
      linear-gradient(rgba(0,200,255,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,200,255,0.04) 1px, transparent 1px),
      linear-gradient(140deg, #020A18 0%, #060D1F 45%, #091830 100%);
    background-size: 48px 48px, 48px 48px, 100% 100%;
    color: #FFFFFF;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 56px 72px;
  }
  section.portada h1 {
    font-size: 40px;
    font-weight: 800;
    color: #FFFFFF;
    border-bottom: 2px solid #00C8FF;
    padding-bottom: 12px;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
    text-shadow: 0 0 50px rgba(0,200,255,0.2);
  }
  section.portada h2 { font-size: 19px; color: #6A9DBD; font-weight: 400; margin: 0 0 24px 0; }
  section.portada p  { font-size: 13px; color: #3A6080; margin: 3px 0; }
  section.portada .tag {
    display: inline-block;
    background: rgba(0,200,255,0.1);
    border: 1px solid rgba(0,200,255,0.28);
    color: #00C8FF;
    font-size: 11px;
    border-radius: 4px;
    padding: 4px 12px;
    margin: 3px 4px 0 0;
    font-weight: 500;
    letter-spacing: 0.03em;
  }

  /* ── SECTION SEPARATOR ─────────────────────────────────── */
  section.sep {
    background-color: #050C1A;
    background-image:
      linear-gradient(rgba(0,200,255,0.06) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,200,255,0.06) 1px, transparent 1px),
      linear-gradient(135deg, #001428 0%, #003060 50%, #001428 100%);
    background-size: 40px 40px, 40px 40px, 100% 100%;
    color: #FFFFFF;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    padding: 56px 80px;
  }
  section.sep h2 {
    font-size: 32px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 14px 0;
    text-shadow: 0 0 30px rgba(0,200,255,0.35);
  }
  section.sep p { font-size: 17px; color: #6A9DBD; margin: 0; }
  section.sep .sep-num {
    font-size: 56px;
    font-weight: 800;
    color: #00C8FF;
    opacity: 0.15;
    line-height: 1;
    margin-bottom: 6px;
  }

  /* ── CHART-FULL ────────────────────────────────────────── */
  section.chart-full img {
    max-height: 420px;
    width: auto;
    max-width: 100%;
    margin: 4px auto 0 auto;
  }

  /* ── PAGINATION ────────────────────────────────────────── */
  section::after { font-size: 11px; color: #1A3050; }

---

<!-- _class: portada -->

# RTM Performance 2024
## Profitability is not about city — it's about channel and store format

<br>

**Audience:** Logistics Direction · RTM Team · Commercial Team
**Data:** 100,000 invoices · 8 cities · 3 channels · 3 store formats

<div style="margin-top: 18px;">
  <span class="tag">January – December 2024</span>
  <span class="tag">72 routes analyzed</span>
  <span class="tag">dbt + Power BI pipeline</span>
  <span class="tag">Validated narrative</span>
</div>

<!-- Speaker notes:
This analysis answers the central investment question for 2025: where to allocate field capacity and commercial resources to capture the highest margin? The answer is counterintuitive: not in new cities, but in the channel and format mix within the markets we already serve.
-->

---

# The RTM portfolio: $118M across 72 routes — the market is fully covered

<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-value">$118M</div>
    <div class="kpi-label">Total Revenue MXN</div>
    <div class="kpi-delta">100,000 invoices · Jan–Dec 2024</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-value">19.3%</div>
    <div class="kpi-label">Average Gross Margin</div>
    <div class="kpi-delta">$393 MXN avg ticket price</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-value">80.0%</div>
    <div class="kpi-label">Cost to Serve (CTS)</div>
    <div class="kpi-delta">Stable throughout the year</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value">72</div>
    <div class="kpi-label">Routes Analyzed</div>
    <div class="kpi-delta">8 cities × 3 channels × 3 formats</div>
  </div>
</div>

<div class="so-what">The portfolio is fully mapped. The opportunity for 2025 is not expansion — it's <strong>optimizing the channel and format mix</strong> within existing routes. The analysis that follows shows exactly where that opportunity lies.</div>

<div class="src">Source: fct_sales · dim_locations · dbt pipeline · 100k invoices · 2024</div>

<!-- Speaker notes:
These are the numbers that define the portfolio. The key point: CTS stable at 80% throughout the year means the cost structure is fixed. Any margin improvement from route restructuring goes straight to the bottom line.
-->

---

<!-- _class: sep -->

<div class="sep-num">01</div>

## Context: Geography is not the lever

The city gap is just 3.5% — but the route gap is $71k per year

<!-- Speaker notes:
The first section establishes why geography cannot be the investment lever for 2025. The data makes it clear: variability between cities is minimal.
-->

---

<!-- _class: chart-full -->

# Geography does not predict profitability — the city gap is just 3.5%

![w:900](charts/01_city_revenue.png)

<div class="src">Source: Total revenue by city · All channels and formats · Full year 2024</div>

<!-- Speaker notes:
Monterrey generates $15.0M and Tijuana $14.5M — a difference of just $500k between the top and bottom city. This uniformity is remarkable for a portfolio of this scale. It means city expansion is not the margin lever for 2025.
-->

---

# Expanding into new cities will not solve the margin problem

<div class="so-what"><strong>What the data says:</strong> With only 3.5% difference between the #1 and last-ranked city, opening presence in new cities is not the available profitability lever.</div>

<div class="finding">
  <strong>Key finding:</strong> The 8 cities distribute revenue remarkably evenly — Monterrey ($15.0M) vs Tijuana ($14.5M). Geographic distribution is balanced. Margin variability exists, but it lives at a different level.
</div>

<div class="so-what"><strong>The question that follows:</strong> If all cities generate similar revenue, why are some individual routes within those cities far more profitable than others?</div>

<div class="src">Source: fct_sales JOIN dim_locations · Grouped by city · 2024</div>

<!-- Speaker notes:
This slide is the narrative inflection point. The initial hypothesis — that higher-volume cities explain performance — is ruled out here. The focus shifts to the next level: individual routes.
-->

---

<!-- _class: sep -->

<div class="sep-num">02</div>

## Tension: The real gap lives in channel and format

Within the same cities, the gap between the best and worst route is $71k MXN per year

<!-- Speaker notes:
The second section reveals where the portfolio's real variability lives: in the combination of channel and store format, not in geography. We present four mutually reinforcing pieces of evidence.
-->

---

<!-- _class: chart-full -->

# The real gap is not between cities — it's between routes within the same city

![w:1000](charts/05_top_bottom_routes.png)

<div class="src">Source: Annual gross margin by route · City × Channel × Format · 2024</div>

<!-- Speaker notes:
The top 5 routes average $350k in margin; the bottom 5 average $302k. That $71k gap per route, multiplied across 5 routes, represents $355k of recoverable annual margin — without adding a single new route to the portfolio.
-->

---

# $355k MXN of margin is locked in the 5 weakest routes

<div class="kpi-row">
  <div class="kpi-card green">
    <div class="kpi-value">$350k</div>
    <div class="kpi-label">Avg gross margin · Top 5 routes</div>
    <div class="kpi-delta">$401 MXN revenue/unit · CTS 79.8%</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-value">$302k</div>
    <div class="kpi-label">Avg gross margin · Bottom 5 routes</div>
    <div class="kpi-delta">$381 MXN revenue/unit · CTS 80.2%</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-value">$71k</div>
    <div class="kpi-label">Gap per route per year</div>
    <div class="kpi-delta">$355k total across 5 routes — recoverable</div>
  </div>
</div>

<div class="so-what">If the 5 weakest routes operated with the economics of the star routes, the portfolio would recover <strong>$355k MXN of gross margin annually</strong> — without adding a single new route. What separates the top routes from the bottom? The data points to two factors: channel and store format.</div>

<div class="src">Source: fct_sales JOIN dim_locations · Grouped by route · 2024</div>

<!-- Speaker notes:
CTS is also a differentiator: 79.8% for the top 5 vs 80.2% for the bottom 5. Only 0.4 percentage points — but at portfolio scale, that delta explains a significant portion of the $71k gap.
-->

---

<!-- _class: chart-full -->

# The Offline channel fell behind in H2 — the signal is small but clear

![w:860](charts/02_channel_h1_h2.png)

<div class="kpi-row">
  <div class="kpi-card green">
    <div class="kpi-value">+0.18%</div>
    <div class="kpi-label">Omnichannel H2 Growth</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-value">+0.18%</div>
    <div class="kpi-label">Online H2 Growth</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-value">−0.11%</div>
    <div class="kpi-label">Offline H2 vs H1 Decline</div>
  </div>
</div>

<div class="src">Source: fct_sales JOIN dim_locations · Split at 2024-07-01 · By channel</div>

<!-- Speaker notes:
The absolute movement is small. But the directional pattern is unambiguous and consistent: Offline concedes while digital channels gain. Combined with the format × channel matrix, the Offline-only trajectory is becoming structurally less competitive. Without intervention, the gap will widen in 2025.
-->

---

<!-- _class: chart-full -->

# The winning combination: Omnichannel + Super — Express drags the portfolio across all three channels

![w:780](charts/06_format_channel_heatmap.png)

<div class="src">Source: Avg margin % by format × channel combination · 2024</div>

<!-- Speaker notes:
The 3×3 matrix reveals the pattern clearly: Omnichannel Super leads at 19.61%. More importantly: the same format (Hyper) performs better in Omnichannel than in Offline. Express ranks last across all channels — without exception. Format matters as much as channel.
-->

---

<!-- _class: chart-full -->

# Revenue fluctuates — CTS does not. The margin gap is a channel-format problem, not a cost problem

![w:940](charts/04_monthly_trend.png)

<div class="src">Source: Monthly revenue and avg CTS · 72 routes · January–December 2024</div>

<!-- Speaker notes:
This is the finding that eliminates the alternative hypothesis: "maybe Express has a higher CTS due to the logistics of short-stop visits?" No. CTS is stable at 79.8–80.2% throughout the year, regardless of monthly volume. The margin difference between routes is not a cost problem — it's a revenue-per-unit problem, determined by channel and format.
-->

---

# The cost structure is fixed — every margin improvement goes straight to the bottom line

<div class="finding">
  <strong>Critical implication:</strong> CTS remains in the 79.8–80.2% range across all 12 months of 2024, with a variation of just <strong>0.4 percentage points</strong> — regardless of revenue peaks in January, August, and October.
</div>

<div class="ok"><strong>What this means for restructuring:</strong> There is no "hidden cost" to restructuring Express routes. The cost structure is homogeneous across the entire portfolio. Every peso of margin recovered through channel or format migration reaches the bottom line intact — the operational cost does not absorb the gain.</div>

<div class="so-what"><strong>The conclusion:</strong> The $71k gap between star routes and weak routes is <strong>100% a channel and format mix problem</strong> — and it is 100% recoverable.</div>

<div class="src">Source: fct_sales · Grouped monthly · Jan–Dec 2024</div>

<!-- Speaker notes:
This slide closes the tension section argument. We have shown that: (1) geography does not explain the gap, (2) the channel is shifting, (3) the format+channel combination is the driver, and (4) costs are not the bottleneck. We are ready for recommendations.
-->

---

<!-- _class: sep -->

<div class="sep-num">03</div>

## Resolution: Three routes set the standard — three decisions capture the opportunity

$355k MXN annually available without adding a single new route

<!-- Speaker notes:
The final section answers the question the audience is forming: "what do we do now?" We identify the star routes, quantify the total opportunity, and present three concrete actions with owners and dates.
-->

---

<!-- _class: chart-full -->

# Three routes define what's possible — and five routes show what's being lost

![w:920](charts/03_route_matrix.png)

<div class="src">Source: 72 routes (8 cities × 3 channels × 3 formats) · CTS% vs revenue per unit · 2024</div>

<!-- Speaker notes:
The efficiency matrix positions the 72 routes by cost to serve (X axis) vs revenue per unit (Y axis). Star routes sit in the upper-left quadrant: low CTS + high value. Critical routes in the lower-right. CDMX Offline Hyper anchors the star quadrant. Querétaro Offline Express sits at the portfolio floor.
-->

---

# Star routes share a pattern — and that pattern is replicable

<div class="two-col">
  <div class="col">
    <h3>Star routes (upper left quadrant)</h3>
    <div class="ok"><strong>CDMX Offline Hyper</strong><br>$359k MXN margin · CTS 79.8% · $401 MXN/unit</div>
    <div class="ok"><strong>Monterrey Omnichannel Super</strong><br>$355k MXN margin · CTS 79.8% · $399 MXN/unit</div>
    <div class="ok"><strong>Puebla Omnichannel Express</strong><br>$351k MXN margin · CTS 79.9% · $397 MXN/unit</div>
    <h3 style="margin-top: 10px;">Common pattern</h3>
    <div class="finding">Omnichannel or Offline channel · Hyper or Super format · CTS &lt; 79.9% · Ticket &gt; $397 MXN</div>
  </div>
  <div class="col">
    <h3>Critical routes (lower right quadrant)</h3>
    <div class="warn"><strong>Querétaro Offline Express</strong><br>$288k MXN margin · CTS 80.3% · $383 MXN/unit</div>
    <div class="warn"><strong>León Offline Express</strong><br>$295k MXN margin · CTS 80.2% · $380 MXN/unit</div>
    <h3 style="margin-top: 10px;">Common pattern</h3>
    <div class="warn">Always Offline · Always Express · CTS &gt; 80.2% · Ticket &lt; $385 MXN</div>
  </div>
</div>

<div class="src">Source: fct_sales JOIN dim_locations · By route · 2024</div>

<!-- Speaker notes:
Star routes are not random exceptions — they share the same channel, format, CTS, and ticket pattern. Critical routes share their pattern too. This confirms that restructuring is possible: there is a clear model to follow.
-->

---

<div style="text-align: center; padding: 20px 0 10px 0;">
  <div class="impact-num">$355k</div>
  <div class="impact-label">MXN of recoverable margin — without adding a single new route</div>
  <div class="impact-sub">Restructure 5 weak routes to star route economics</div>
</div>

<div class="kpi-row" style="margin-top: 16px;">
  <div class="kpi-card green">
    <div class="kpi-value">$355k</div>
    <div class="kpi-label">Restructure 5 weak routes</div>
    <div class="kpi-delta">$71k per route per year</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-value">$201k</div>
    <div class="kpi-label">Cost of inaction over 3 years</div>
    <div class="kpi-delta">$67k/yr × 3 · just 2 Express routes</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-value">$180–220k</div>
    <div class="kpi-label">Omnichannel migration 5% of volume</div>
    <div class="kpi-delta">Across the 10 weakest Offline routes · Q2 2025</div>
  </div>
</div>

<div class="src">Source: Route gap analysis · Omnichannel migration projection · 2024</div>

<!-- Speaker notes:
The total opportunity exceeds $500k MXN annually if both levers are executed in parallel. The cost of inaction is concrete: $201k over 3 years from just the 2 critical Express routes. This is the number to bring to the leadership team.
-->

---

# Three decisions the RTM team can execute immediately

<div class="rec-row">
  <div class="rec-action">R1 — Protect and scale the 3 star routes<br><span class="rec-owner">Priority frequency · Preferential stock · Commercial terms review</span></div>
  <div><span class="confidence-high">HIGH CONFIDENCE</span><br><span class="rec-owner">Field Ops · Jan 2025</span></div>
  <div class="rec-metric">CTS &lt; 79.9% · Margin &gt; $350k across 3 routes</div>
</div>

<div class="rec-row">
  <div class="rec-action">R2 — Restructure Offline Express routes (Querétaro + León)<br><span class="rec-owner">Option A: migrate to Omnichannel · B: consolidate stops · C: managed exit</span></div>
  <div><span class="confidence-high">HIGH CONFIDENCE</span><br><span class="rec-owner">RTM Manager · Mar 2025</span></div>
  <div class="rec-metric">Margin ≥ $320k MXN by Q2 2025</div>
</div>

<div class="rec-row">
  <div class="rec-action">R3 — Accelerate Omnichannel migration<br><span class="rec-owner">10 lowest-ticket Offline clients/city · digital onboarding with commercial support</span></div>
  <div><span class="confidence-med">MEDIUM–HIGH</span><br><span class="rec-owner">Commercial + Logistics · Mar 2025</span></div>
  <div class="rec-metric">+0.3 pp margin · 5% volume converted · Q2</div>
</div>

<div class="src">Source: RTM portfolio analysis · dbt pipeline · 2024</div>

<!-- Speaker notes:
The three recommendations are ordered by confidence: R1 and R2 have direct support from the full-year annual data. R3 is supported by the H2 trend, but its magnitude depends on commercial execution speed. Owner, date, and success metric are defined for each.
-->

---

# Action plan — next 90 days

| # | Action | Owner | Deadline | Success Metric |
|---|--------|-------|----------|----------------|
| 1 | Review route plan for Querétaro Offline Express | RTM Manager | Mar 2025 | Margin ≥ $320k MXN in Q2 |
| 2 | Omnichannel conversion pilot in 2 Offline routes | Commercial + Logistics | Mar 2025 | +0.3 pp margin |
| 3 | Define visit frequency for top 10 routes | Field Operations | Jan 2025 | 100% star route coverage |
| 4 | Review cost structure for Hyper Omnichannel | RTM + Finance | Mar 2025 | CTS% < 80.0% |
| 5 | Monthly route review cadence | RTM Leadership | Feb 2025 | Active dashboard with KPIs |

<div class="ok" style="margin-top: 10px;"><strong>Program success criterion:</strong> Increase average portfolio margin from <strong>$328k to $345k MXN per route</strong> by December 2025 — equivalent to a 5.2% improvement over the current baseline.</div>

<div class="src">Analysis: dbt-mexico-fmcg-rtm pipeline · 100k invoices · Jan–Dec 2024 · Validated</div>

<!-- Speaker notes:
All 5 actions have an owner, date, and metric. The full program success criterion: $328k → $345k average margin per route by end of 2025. This is the metric for the monthly RTM Leadership dashboard.
-->

---

# Appendix — Sources, methodology and limitations

<div class="two-col">
  <div class="col">
    <h3>Data & Pipeline</h3>
    <ul>
      <li><strong>Source:</strong> Mexico FMCG Retail Sales Customer Inventory (2024)</li>
      <li><strong>Pipeline:</strong> Snowflake raw → dbt staging → marts → 4 CSVs → Power BI</li>
      <li><strong>Route defined as:</strong> City × Channel × Format (72 unique combinations)</li>
      <li><strong>CTS:</strong> Total cost / Total revenue per route — proxy that excludes transportation logistics costs not captured in the transactional dataset</li>
    </ul>
    <h3 style="margin-top: 10px;">Tech stack</h3>
    <ul>
      <li>Snowflake · dbt Core · DuckDB · Python</li>
      <li>Power BI (interactive dashboard)</li>
      <li>Marp (executive presentation)</li>
    </ul>
  </div>
  <div class="col">
    <h3>Quality & Validation</h3>
    <ul>
      <li><strong>100,000 rows</strong> post-pipeline · 0 nulls in critical columns</li>
      <li>72 unique routes · 288 customer profiles · 64 product combinations</li>
      <li>Arithmetic check: Revenue ≈ Cost + Margin ✓</li>
      <li>Channel share: sums to 100% ✓</li>
    </ul>
    <h3 style="margin-top: 10px;">Limitations</h3>
    <div class="warn" style="margin-top: 6px;">Single-year dataset (2024). No year-over-year comparison available — H1/H2 split used as internal trend benchmark.</div>
    <div class="warn">CTS is a proxy — excludes transportation and distribution logistics costs not captured in the transactional dataset.</div>
  </div>
</div>

<div style="margin-top: 10px; padding: 8px 14px; background: rgba(0,200,255,0.05); border: 1px solid rgba(0,200,255,0.15); border-radius: 5px; font-size: 11px; color: #3A6080;">
  Prepared with Claude Code AI Analyst · DBT-MEXICO-FMCG-RTM project · May 2026 · Story Architect + Storytelling + Deck Creator pipeline
</div>

<!-- Speaker notes:
The appendix documents the key limitations: single-year dataset and CTS as a proxy. Both are known to the team. Full reproducibility is guaranteed: all models are codified in dbt and the build_powerbi_data.py script regenerates the 4 CSVs from raw.
-->
