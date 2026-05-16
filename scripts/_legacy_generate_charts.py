import sys, os
sys.path.insert(0, r'C:\Users\Héctor\Desktop\PROJECT_PORTFOLIO\CLAUDE_CODE_ANALYST')

import duckdb
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from helpers.chart_helpers import swd_style

CSV = 'bi_Analytics/rtm_final_powerbi.csv'
OUT = 'outputs/charts'
os.makedirs(OUT, exist_ok=True)

con = duckdb.connect()

# Apply SWD style globally and get palette
colors = swd_style()

BLUE       = '#2563EB'
ORANGE     = '#F97316'
RED        = '#DC2626'
GREEN      = '#16A34A'
GREY       = '#9CA3AF'
DARK_GREY  = '#374151'

# ══════════════════════════════════════════════════════════════════════════
# CHART 1 — City Revenue Ranking
# ══════════════════════════════════════════════════════════════════════════
df1 = con.sql(f"""
SELECT city,
       ROUND(SUM(revenue)/1e6, 2) AS rev_m,
       ROUND(AVG(margin_pct)*100, 1) AS margin_pct,
       ROUND(SUM(cost)/SUM(revenue)*100, 1) AS cts_pct
FROM read_csv_auto('{CSV}')
GROUP BY 1 ORDER BY rev_m DESC
""").df()

fig, ax = plt.subplots(figsize=(10, 5.5))
bar_colors = [BLUE if i == 0 else (RED if i == len(df1)-1 else GREY)
              for i in range(len(df1))]
bars = ax.barh(df1['city'][::-1], df1['rev_m'][::-1],
               color=bar_colors[::-1], height=0.6, zorder=3)

for bar, val, m in zip(bars, df1['rev_m'][::-1], df1['margin_pct'][::-1]):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f'MXN ${val:.1f}M  |  {m:.1f}% margin',
            va='center', fontsize=9, color=DARK_GREY)

ax.set_xlim(0, 19)
ax.set_xlabel('Revenue (MXN millions)', fontsize=9)
ax.set_title('Monterrey leads the portfolio — Tijuana trails by 3.5%',
             fontsize=13, fontweight='bold', pad=12)
ax.annotate('Full Year 2024 · All channels and formats combined',
            xy=(0.01, 1.02), xycoords='axes fraction', fontsize=8, color=GREY)

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/01_city_revenue.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 1 saved')


# ══════════════════════════════════════════════════════════════════════════
# CHART 2 — Channel H1 vs H2
# ══════════════════════════════════════════════════════════════════════════
df2 = con.sql(f"""
SELECT channel,
       ROUND(SUM(CASE WHEN invoice_date < '2024-07-01' THEN revenue END)/1e6, 2) AS h1,
       ROUND(SUM(CASE WHEN invoice_date >= '2024-07-01' THEN revenue END)/1e6, 2) AS h2
FROM read_csv_auto('{CSV}')
GROUP BY 1 ORDER BY (h2-h1) DESC
""").df()

fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(df2))
w = 0.35
b1 = ax.bar(x - w/2, df2['h1'], w, label='H1 2024', color=GREY, zorder=3)
b2 = ax.bar(x + w/2, df2['h2'], w, label='H2 2024', color=BLUE, zorder=3)

for bar in list(b1) + list(b2):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'${bar.get_height():.2f}M', ha='center', va='bottom', fontsize=9)

offline_idx = df2[df2['channel']=='Offline'].index[0]
ax.annotate('Offline declines\nin H2 ▼',
            xy=(offline_idx + w/2, df2.loc[offline_idx,'h2']),
            xytext=(offline_idx + w/2 + 0.5, df2.loc[offline_idx,'h2'] - 0.3),
            fontsize=8.5, color=RED, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))

ax.set_xticks(x)
ax.set_xticklabels(df2['channel'], fontsize=10)
ax.set_ylim(0, 22)
ax.set_ylabel('Revenue (MXN millions)', fontsize=9)
ax.legend(frameon=False, fontsize=9)
ax.set_title('Offline channel loses ground in H2 while Digital routes grow',
             fontsize=13, fontweight='bold', pad=12)
ax.annotate('H1 = Jan–Jun 2024 · H2 = Jul–Dec 2024',
            xy=(0.01, 1.02), xycoords='axes fraction', fontsize=8, color=GREY)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/02_channel_h1_h2.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 2 saved')


# ══════════════════════════════════════════════════════════════════════════
# CHART 3 — Route Efficiency Scatter
# ══════════════════════════════════════════════════════════════════════════
df3 = con.sql(f"""
SELECT
    city, channel, store_format,
    SUM(units) AS units,
    ROUND(SUM(revenue)/SUM(units), 2) AS rev_per_unit,
    ROUND(SUM(cost)/SUM(revenue)*100, 2) AS cts_pct,
    ROUND(SUM(margin)/1e3, 1) AS margin_k
FROM read_csv_auto('{CSV}')
GROUP BY 1,2,3
""").df()

channel_colors = {'Online': BLUE, 'Omnichannel': GREEN, 'Offline': ORANGE}
fmt_markers    = {'Hyper': 'o', 'Super': 's', 'Express': '^'}

fig, ax = plt.subplots(figsize=(11, 6.5))

sizes = 60 + (df3['units'] - df3['units'].min()) / (df3['units'].max() - df3['units'].min()) * 180

for idx, row in df3.iterrows():
    ax.scatter(row['cts_pct'], row['rev_per_unit'],
               s=sizes[idx], alpha=0.82, zorder=4,
               color=channel_colors.get(row['channel'], GREY),
               marker=fmt_markers.get(row['store_format'], 'o'),
               edgecolors='white', linewidths=0.6)

med_cts = df3['cts_pct'].median()
med_rpu = df3['rev_per_unit'].median()
ax.axvline(med_cts, color=GREY, linestyle='--', lw=0.9, alpha=0.5)
ax.axhline(med_rpu, color=GREY, linestyle='--', lw=0.9, alpha=0.5)

ax.text(79.42, 410.0, 'STAR ROUTES\nLow cost · High value', fontsize=7.5,
        color=GREEN, fontweight='bold')
ax.text(80.28, 410.0, 'HIGH VALUE\nHigh cost', fontsize=7.5, color=ORANGE)
ax.text(79.42, 376.5, 'VOLUME ROUTES\nLow cost · Lower value', fontsize=7.5, color=BLUE)
ax.text(80.28, 376.5, 'CRITICAL\nReview needed', fontsize=7.5, color=RED, fontweight='bold')

# Label top 3 and bottom 3 by margin
for _, row in df3.nlargest(3, 'margin_k').iterrows():
    ax.annotate(f"{row['city']}\n{row['store_format']}",
                xy=(row['cts_pct'], row['rev_per_unit']),
                xytext=(row['cts_pct'] - 0.22, row['rev_per_unit'] + 1.8),
                fontsize=7, color=GREEN, fontweight='bold')
for _, row in df3.nsmallest(3, 'margin_k').iterrows():
    ax.annotate(f"{row['city']}\n{row['store_format']}",
                xy=(row['cts_pct'], row['rev_per_unit']),
                xytext=(row['cts_pct'] + 0.03, row['rev_per_unit'] - 3.0),
                fontsize=7, color=RED)

legend_ch = [mpatches.Patch(facecolor=c, label=ch) for ch, c in channel_colors.items()]
legend_fm = [plt.Line2D([0],[0], marker=m, color='w', markerfacecolor=DARK_GREY,
             markersize=7, label=f) for f, m in fmt_markers.items()]
l1 = ax.legend(handles=legend_ch, title='Channel', frameon=False,
               fontsize=8, title_fontsize=8, loc='upper left')
ax.add_artist(l1)
ax.legend(handles=legend_fm, title='Format', frameon=False,
          fontsize=8, title_fontsize=8, loc='lower right')

ax.set_xlabel('Cost-to-Serve %  (lower → better)', fontsize=9)
ax.set_ylabel('Revenue per Unit (MXN)', fontsize=9)
ax.set_title('Route Efficiency Matrix — every route mapped by cost efficiency and ticket value',
             fontsize=12, fontweight='bold', pad=12)
ax.annotate('Bubble size = volume  ·  Shape = store format  ·  Color = channel  |  2024',
            xy=(0.01, 1.02), xycoords='axes fraction', fontsize=8, color=GREY)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/03_route_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 3 saved')


# ══════════════════════════════════════════════════════════════════════════
# CHART 4 — Monthly Revenue & CTS Trend
# ══════════════════════════════════════════════════════════════════════════
df4 = con.sql(f"""
SELECT
    STRFTIME(invoice_date, '%b') AS month_lbl,
    STRFTIME(invoice_date, '%Y-%m') AS month_sort,
    ROUND(SUM(revenue)/1e6, 2) AS rev_m,
    ROUND(SUM(cost)/SUM(revenue)*100, 2) AS cts_pct
FROM read_csv_auto('{CSV}')
GROUP BY 1,2 ORDER BY 2
""").df()

fig, ax1 = plt.subplots(figsize=(11, 5.5))
ax2 = ax1.twinx()

x = range(len(df4))
ax1.bar(x, df4['rev_m'], color=BLUE, alpha=0.65, zorder=3)
ax2.plot(x, df4['cts_pct'], color=ORANGE, marker='o', linewidth=2,
         markersize=5, zorder=4)
ax2.fill_between(x, df4['cts_pct'], alpha=0.08, color=ORANGE)

ax1.set_xticks(list(x))
ax1.set_xticklabels(df4['month_lbl'], fontsize=9)
ax1.set_ylabel('Revenue (MXN millions)', fontsize=9, color=BLUE)
ax2.set_ylabel('Cost-to-Serve %', fontsize=9, color=ORANGE)
ax2.set_ylim(78.5, 81.5)
ax1.set_ylim(0, 12.5)

ax1.axvline(5.5, color=DARK_GREY, linestyle=':', lw=1.2, alpha=0.6)
ax1.text(5.62, 11.9, 'H2', fontsize=8, color=DARK_GREY)

peak_i = df4['rev_m'].idxmax()
low_i  = df4['rev_m'].idxmin()
ax1.annotate(f"Peak ${df4.loc[peak_i,'rev_m']:.1f}M",
             xy=(peak_i, df4.loc[peak_i,'rev_m']),
             xytext=(peak_i - 1.8, df4.loc[peak_i,'rev_m'] + 0.1),
             fontsize=8, color=BLUE,
             arrowprops=dict(arrowstyle='->', color=BLUE, lw=1))
ax1.annotate(f"Trough ${df4.loc[low_i,'rev_m']:.1f}M",
             xy=(low_i, df4.loc[low_i,'rev_m']),
             xytext=(low_i + 0.3, df4.loc[low_i,'rev_m'] - 0.9),
             fontsize=8, color=RED,
             arrowprops=dict(arrowstyle='->', color=RED, lw=1))

p1 = mpatches.Patch(facecolor=BLUE, alpha=0.65, label='Revenue (MXN M)')
p2 = plt.Line2D([0],[0], color=ORANGE, marker='o', linewidth=2, label='Cost-to-Serve %')
ax1.legend(handles=[p1, p2], frameon=False, fontsize=9, loc='upper right')

ax1.set_title('Revenue peaks Jan/Aug/Oct — Cost-to-Serve stable across the year',
              fontsize=13, fontweight='bold', pad=12)
ax1.annotate('Monthly totals · All 72 routes combined · 2024',
             xy=(0.01, 1.02), xycoords='axes fraction', fontsize=8, color=GREY)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/04_monthly_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 4 saved')


# ══════════════════════════════════════════════════════════════════════════
# CHART 5 — Top 5 vs Bottom 5 Routes
# ══════════════════════════════════════════════════════════════════════════
df5 = con.sql(f"""
SELECT
    city || ' › ' || channel || ' › ' || store_format AS route,
    ROUND(SUM(margin)/1e3, 1) AS margin_k,
    ROUND(AVG(margin_pct)*100,1) AS margin_pct,
    ROUND(SUM(cost)/SUM(revenue)*100,1) AS cts_pct
FROM read_csv_auto('{CSV}')
GROUP BY 1
""").df()

top5 = df5.nlargest(5, 'margin_k').sort_values('margin_k')
bot5 = df5.nsmallest(5, 'margin_k').sort_values('margin_k', ascending=False)
combined = pd.concat([bot5.assign(tier='bottom'), top5.assign(tier='top')]).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(12, 6))
bar_c = [GREEN if t == 'top' else RED for t in combined['tier']]
bars  = ax.barh(combined['route'], combined['margin_k'],
                color=bar_c, height=0.6, zorder=3)

for bar, (_, row) in zip(bars, combined.iterrows()):
    label = f"${row['margin_k']:.0f}k  |  {row['margin_pct']:.1f}% margin  |  CTS {row['cts_pct']:.1f}%"
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            label, va='center', fontsize=8.5, color=DARK_GREY)

mean_val = df5['margin_k'].mean()
ax.axvline(mean_val, color=GREY, linestyle='--', lw=1, alpha=0.7)
ax.text(mean_val + 0.3, len(combined) - 0.3,
        f"Portfolio avg\n${mean_val:.0f}k", fontsize=8, color=GREY)

ax.axhline(4.5, color=DARK_GREY, linestyle=':', lw=1, alpha=0.4)
ax.set_xlabel('Gross Margin (MXN thousands)', fontsize=9)
ax.set_xlim(0, 430)
ax.set_title('CDMX Offline Hyper leads — Querétaro Offline Express is the portfolio floor',
             fontsize=12, fontweight='bold', pad=12)
ax.annotate('Full Year 2024 · Route = City › Channel › Store Format',
            xy=(0.01, 1.02), xycoords='axes fraction', fontsize=8, color=GREY)

gp = mpatches.Patch(color=GREEN, label='Top 5 routes by margin')
rp = mpatches.Patch(color=RED,   label='Bottom 5 routes by margin')
ax.legend(handles=[gp, rp], frameon=False, fontsize=9, loc='lower right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/05_top_bottom_routes.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 5 saved')


# ══════════════════════════════════════════════════════════════════════════
# CHART 6 — Store Format × Channel margin heatmap
# ══════════════════════════════════════════════════════════════════════════
df6 = con.sql(f"""
SELECT
    store_format,
    channel,
    ROUND(AVG(margin_pct)*100, 2) AS margin_pct
FROM read_csv_auto('{CSV}')
GROUP BY 1,2
""").df()

pivot = df6.pivot(index='store_format', columns='channel', values='margin_pct')

fig, ax = plt.subplots(figsize=(8, 4.5))
im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto',
               vmin=pivot.values.min()-0.05, vmax=pivot.values.max()+0.05)

ax.set_xticks(range(len(pivot.columns)))
ax.set_yticks(range(len(pivot.index)))
ax.set_xticklabels(pivot.columns, fontsize=11)
ax.set_yticklabels(pivot.index, fontsize=11)

mean_val = pivot.values.mean()
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        val = pivot.values[i, j]
        txt_color = 'white' if val < mean_val - 0.05 else DARK_GREY
        ax.text(j, i, f'{val:.2f}%', ha='center', va='center',
                fontsize=12, fontweight='bold', color=txt_color)

plt.colorbar(im, ax=ax, label='Avg Margin %', shrink=0.85)
ax.set_title('Margin % by Format × Channel — Super Omnichannel outperforms',
             fontsize=12, fontweight='bold', pad=12)
ax.annotate('Average transaction margin % · 2024 full year',
            xy=(0.01, 1.05), xycoords='axes fraction', fontsize=8, color=GREY)

plt.tight_layout()
plt.savefig(f'{OUT}/06_format_channel_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 6 saved')

print('\nAll 6 charts generated in', OUT)
con.close()
