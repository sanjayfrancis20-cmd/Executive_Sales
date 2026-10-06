import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

os.makedirs('assets', exist_ok=True)
os.makedirs('reports', exist_ok=True)

df = pd.read_csv('data/sales_financial_dataset.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])

# --- 1. KEY KPI SUMMARY ---
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_items = df['Quantity'].sum()
overall_margin = (total_profit / total_sales) * 100
avg_order_value = total_sales / total_orders

# Yearly metrics & YoY
yearly = df.groupby('Year').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).reset_index()
yearly['Sales_YoY'] = yearly['Sales'].pct_change() * 100
yearly['Profit_YoY'] = yearly['Profit'].pct_change() * 100
yearly['Margin_%'] = (yearly['Profit'] / yearly['Sales']) * 100

print("=== EXECUTIVE KPI SUMMARY ===")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Overall Profit Margin: {overall_margin:.2f}%")
print(f"Unique Orders: {total_orders:,}")
print(f"Total Units Sold: {total_items:,}")
print(f"Average Order Value: ${avg_order_value:,.2f}")
print("\n--- Yearly Performance ---")
print(yearly.to_string(index=False))

# --- CHART 1: TIME SERIES TREND (Monthly Sales & Profit) ---
monthly = df.set_index('Order Date').resample('ME').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 5.5), dpi=300)
ax2 = ax1.twinx()

line1 = ax1.plot(monthly['Order Date'], monthly['Sales'] / 1e3, color='#1E40AF', linewidth=2.5, marker='o', markersize=4, label='Monthly Sales ($K)')
bar1 = ax2.bar(monthly['Order Date'], monthly['Profit'] / 1e3, color=np.where(monthly['Profit'] >= 0, '#10B981', '#EF4444'), width=18, alpha=0.55, label='Monthly Profit ($K)')

ax1.set_title('Sales & Profitability Monthly Time-Series Trend (2021 - 2024)', fontsize=14, fontweight='bold', pad=15, color='#0F172A')
ax1.set_xlabel('Timeline', fontsize=11, fontweight='semibold', labelpad=10)
ax1.set_ylabel('Total Sales ($ in Thousands)', fontsize=11, fontweight='semibold', color='#1E40AF')
ax2.set_ylabel('Total Profit ($ in Thousands)', fontsize=11, fontweight='semibold', color='#059669')

ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"${x:,.0f}K"))
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"${x:,.0f}K"))
ax1.grid(True, linestyle='--', alpha=0.5)
ax2.grid(False)

# Add Legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

plt.tight_layout()
chart1_path = 'assets/chart_timeseries_trend.png'
plt.savefig(chart1_path)
plt.close()

# --- CHART 2: REGIONAL PERFORMANCE (Sales & Margin %) ---
regional = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).reset_index()
regional['Margin_%'] = (regional['Profit'] / regional['Sales']) * 100
regional.sort_values(by='Sales', ascending=False, inplace=True)

fig, (ax_sales, ax_margin) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

palette = ['#1D4ED8', '#2563EB', '#3B82F6', '#60A5FA']
bars = ax_sales.bar(regional['Region'], regional['Sales'] / 1e6, color=palette, width=0.55, edgecolor='#1E3A8A')
ax_sales.set_title('Total Revenue by Geographic Region', fontsize=12, fontweight='bold', color='#0F172A')
ax_sales.set_ylabel('Sales ($ Millions)', fontsize=10, fontweight='semibold')
ax_sales.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"${x:.2f}M"))
ax_sales.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    yval = bar.get_height()
    ax_sales.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f"${yval:.2f}M", ha='center', va='bottom', fontsize=9, fontweight='bold')

margin_colors = ['#10B981' if m >= 11 else '#F59E0B' for m in regional['Margin_%']]
bars_m = ax_margin.bar(regional['Region'], regional['Margin_%'], color=margin_colors, width=0.55)
ax_margin.set_title('Profit Margin % by Geographic Region', fontsize=12, fontweight='bold', color='#0F172A')
ax_margin.set_ylabel('Profit Margin (%)', fontsize=10, fontweight='semibold')
ax_margin.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:.1f}%"))
ax_margin.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars_m:
    yval = bar.get_height()
    ax_margin.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
chart2_path = 'assets/chart_regional_performance.png'
plt.savefig(chart2_path)
plt.close()

# --- CHART 3: SUB-CATEGORY PROFITABILITY & SALES MATRIX ---
subcat = df.groupby(['Category', 'Sub-Category']).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Discount': 'mean'
}).reset_index()
subcat['Margin_%'] = (subcat['Profit'] / subcat['Sales']) * 100
subcat.sort_values(by='Profit', ascending=True, inplace=True)

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
colors = ['#EF4444' if p < 0 else ('#10B981' if p > 100000 else '#3B82F6') for p in subcat['Profit']]
hbars = ax.barh(subcat['Sub-Category'], subcat['Profit'] / 1e3, color=colors, height=0.65)

ax.set_title('Net Profit Contribution by Product Sub-Category ($ in Thousands)', fontsize=13, fontweight='bold', color='#0F172A', pad=12)
ax.set_xlabel('Total Net Profit ($K)', fontsize=10, fontweight='semibold')
ax.axvline(0, color='#64748B', linewidth=1)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"${x:,.0f}K"))
ax.grid(axis='x', linestyle='--', alpha=0.5)

for bar in hbars:
    width = bar.get_width()
    offset = 4 if width >= 0 else -18
    ha = 'left' if width >= 0 else 'right'
    ax.text(width + offset, bar.get_y() + bar.get_height()/2, f"${width:,.0f}K", ha=ha, va='center', fontsize=8.5, fontweight='bold')

plt.tight_layout()
chart3_path = 'assets/chart_subcategory_profit.png'
plt.savefig(chart3_path)
plt.close()

# --- CHART 4: CUSTOMER SEGMENT BREAKDOWN (Donut Chart) ---
seg = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
wedges, texts, autotexts = ax.pie(
    seg['Sales'], 
    labels=seg['Segment'], 
    autopct='%1.1f%%',
    startangle=140,
    colors=['#2563EB', '#0D9488', '#F59E0B'],
    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
    pctdistance=0.75
)
for t in autotexts:
    t.set_color('white')
    t.set_fontweight('bold')
    t.set_fontsize(10)
for t in texts:
    t.set_fontsize(11)
    t.set_fontweight('semibold')

ax.set_title('Sales Distribution by Customer Segment', fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
chart4_path = 'assets/chart_segment_distribution.png'
plt.savefig(chart4_path)
plt.close()

print("All charts generated and saved in assets/ successfully!")
