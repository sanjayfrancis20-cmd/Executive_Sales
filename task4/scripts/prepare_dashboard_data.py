import json
import pandas as pd

df = pd.read_csv('data/sales_financial_dataset.csv')

# Prepare records optimized for frontend filtering
records = df[[
    'Order ID', 'Order Date', 'Year', 'Month', 'Region', 'Segment', 
    'Category', 'Sub-Category', 'Sales', 'Profit', 'Quantity', 'Discount'
]].to_dict(orient='records')

with open('deliverables/dashboard_data.js', 'w', encoding='utf-8') as f:
    f.write("const RAW_SALES_DATA = " + json.dumps(records) + ";\n")

print(f"Exported {len(records)} records to deliverables/dashboard_data.js")
