import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_sales_data(num_records=9994, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    # Categories and Sub-Categories hierarchy with typical baseline pricing & margins
    catalog = {
        'Technology': {
            'Phones': {'base_price': (150, 950), 'margin': 0.18, 'discount_range': (0.0, 0.3)},
            'Accessories': {'base_price': (20, 180), 'margin': 0.25, 'discount_range': (0.0, 0.2)},
            'Machines': {'base_price': (400, 2500), 'margin': 0.08, 'discount_range': (0.0, 0.4)},
            'Copiers': {'base_price': (600, 3500), 'margin': 0.35, 'discount_range': (0.0, 0.2)}
        },
        'Furniture': {
            'Chairs': {'base_price': (80, 500), 'margin': 0.12, 'discount_range': (0.0, 0.3)},
            'Bookcases': {'base_price': (100, 650), 'margin': 0.05, 'discount_range': (0.0, 0.4)},
            'Tables': {'base_price': (150, 900), 'margin': -0.06, 'discount_range': (0.1, 0.5)}, # known margin drag
            'Furnishings': {'base_price': (15, 120), 'margin': 0.20, 'discount_range': (0.0, 0.2)}
        },
        'Office Supplies': {
            'Storage': {'base_price': (30, 320), 'margin': 0.14, 'discount_range': (0.0, 0.25)},
            'Binders': {'base_price': (5, 90), 'margin': 0.22, 'discount_range': (0.0, 0.4)},
            'Paper': {'base_price': (10, 80), 'margin': 0.32, 'discount_range': (0.0, 0.15)},
            'Art': {'base_price': (8, 60), 'margin': 0.24, 'discount_range': (0.0, 0.2)},
            'Appliances': {'base_price': (50, 450), 'margin': 0.19, 'discount_range': (0.0, 0.3)},
            'Envelopes': {'base_price': (6, 50), 'margin': 0.30, 'discount_range': (0.0, 0.1)},
            'Labels': {'base_price': (5, 40), 'margin': 0.35, 'discount_range': (0.0, 0.1)},
            'Fasteners': {'base_price': (4, 30), 'margin': 0.28, 'discount_range': (0.0, 0.1)},
            'Supplies': {'base_price': (12, 110), 'margin': 0.08, 'discount_range': (0.0, 0.25)}
        }
    }

    regions_data = {
        'West': {
            'states': ['California', 'Washington', 'Oregon', 'Arizona', 'Nevada', 'Colorado', 'Utah'],
            'cities': {'California': ['Los Angeles', 'San Francisco', 'San Diego', 'San Jose'],
                       'Washington': ['Seattle', 'Spokane'], 'Oregon': ['Portland', 'Eugene'],
                       'Arizona': ['Phoenix', 'Tucson'], 'Nevada': ['Las Vegas', 'Reno'],
                       'Colorado': ['Denver', 'Colorado Springs'], 'Utah': ['Salt Lake City', 'Provo']},
            'weight': 0.32
        },
        'East': {
            'states': ['New York', 'Pennsylvania', 'Massachusetts', 'New Jersey', 'Ohio'],
            'cities': {'New York': ['New York City', 'Buffalo', 'Rochester'],
                       'Pennsylvania': ['Philadelphia', 'Pittsburgh'], 'Massachusetts': ['Boston', 'Worcester'],
                       'New Jersey': ['Newark', 'Jersey City'], 'Ohio': ['Columbus', 'Cleveland', 'Cincinnati']},
            'weight': 0.29
        },
        'Central': {
            'states': ['Illinois', 'Texas', 'Michigan', 'Wisconsin', 'Minnesota', 'Indiana'],
            'cities': {'Illinois': ['Chicago', 'Naperville'], 'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
                       'Michigan': ['Detroit', 'Grand Rapids'], 'Wisconsin': ['Milwaukee', 'Madison'],
                       'Minnesota': ['Minneapolis', 'Saint Paul'], 'Indiana': ['Indianapolis', 'Fort Wayne']},
            'weight': 0.23
        },
        'South': {
            'states': ['Florida', 'North Carolina', 'Virginia', 'Georgia', 'Tennessee'],
            'cities': {'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
                       'North Carolina': ['Charlotte', 'Raleigh'], 'Virginia': ['Richmond', 'Virginia Beach'],
                       'Georgia': ['Atlanta', 'Savannah'], 'Tennessee': ['Nashville', 'Memphis']},
            'weight': 0.16
        }
    }

    segments = ['Consumer', 'Corporate', 'Home Office']
    segment_weights = [0.52, 0.30, 0.18]

    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    ship_weights = [0.59, 0.20, 0.15, 0.06]

    # Generate customer base
    customers = []
    for i in range(1, 800):
        seg = np.random.choice(segments, p=segment_weights)
        c_id = f"CG-{10000 + i}"
        c_name = f"Customer_{i:03d} ({seg})"
        customers.append((c_id, c_name, seg))

    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days

    records = []
    region_names = list(regions_data.keys())
    region_probs = [regions_data[r]['weight'] for r in region_names]

    for i in range(1, num_records + 1):
        order_num = 100000 + (i // 2) # some orders have multiple items
        order_id = f"CA-{order_num}"
        
        # Date generation with seasonal weight (Q4 higher sales)
        day_offset = random.randint(0, total_days)
        order_date = start_date + timedelta(days=day_offset)
        # Seasonal bump for Nov/Dec
        if order_date.month in [11, 12] and random.random() < 0.25:
            # retain
            pass

        ship_mode = np.random.choice(ship_modes, p=ship_weights)
        ship_delay = 5 if ship_mode == 'Standard Class' else (3 if ship_mode == 'Second Class' else (1 if ship_mode == 'First Class' else 0))
        ship_date = order_date + timedelta(days=ship_delay)

        cust = random.choice(customers)
        cust_id, cust_name, segment = cust

        reg = np.random.choice(region_names, p=region_probs)
        state = random.choice(regions_data[reg]['states'])
        city = random.choice(regions_data[reg]['cities'].get(state, [state + " City"]))
        postal = f"{random.randint(10000, 99999)}"

        cat = random.choice(list(catalog.keys()))
        subcat = random.choice(list(catalog[cat].keys()))
        subcat_meta = catalog[cat][subcat]

        prod_id = f"{cat[:3].upper()}-{subcat[:3].upper()}-{random.randint(1000, 9999)}"
        prod_name = f"{subcat} Model {random.randint(100, 999)} Series"

        qty = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=[0.25, 0.25, 0.18, 0.12, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01])
        base_unit_price = round(random.uniform(*subcat_meta['base_price']), 2)

        disc_min, disc_max = subcat_meta['discount_range']
        # Discount logic
        discount_choice = round(random.uniform(disc_min, disc_max), 2)
        if random.random() < 0.45:
            discount = 0.0
        else:
            discount = discount_choice

        # High discount penalty in Central region
        if reg == 'Central' and cat == 'Furniture' and discount > 0.2:
            discount = min(0.6, discount + 0.15)

        gross_sales = base_unit_price * qty
        sales = round(gross_sales * (1.0 - discount), 2)

        # Baseline unit cost based on expected product margin
        nominal_margin = subcat_meta['margin']
        unit_cost = base_unit_price * (1.0 - nominal_margin)
        total_cost = round(unit_cost * qty * random.uniform(0.95, 1.05), 2)

        # Actual profit
        profit = round(sales - total_cost, 2)
        profit_margin = round(profit / sales if sales > 0 else 0.0, 4)

        # Target sales for KPI variance tracking
        target_sales = round(sales * random.uniform(0.90, 1.15), 2)

        records.append({
            'Order ID': order_id,
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Ship Date': ship_date.strftime('%Y-%m-%d'),
            'Ship Mode': ship_mode,
            'Customer ID': cust_id,
            'Customer Name': cust_name,
            'Segment': segment,
            'Country': 'United States',
            'City': city,
            'State': state,
            'Postal Code': postal,
            'Region': reg,
            'Product ID': prod_id,
            'Category': cat,
            'Sub-Category': subcat,
            'Product Name': prod_name,
            'Sales': sales,
            'Quantity': qty,
            'Discount': discount,
            'Profit': profit,
            'Cost': total_cost,
            'Profit Margin': profit_margin,
            'Target Sales': target_sales,
            'Year': order_date.year,
            'Quarter': f"Q{(order_date.month - 1) // 3 + 1}",
            'Month': order_date.strftime('%b'),
            'Month_Num': order_date.month
        })

    df = pd.DataFrame(records)
    df.sort_values(by=['Order Date', 'Order ID'], inplace=True)
    return df

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    print("Generating Sales & Financial Dataset...")
    df = generate_sales_data(9994, seed=42)
    csv_path = os.path.join('data', 'sales_financial_dataset.csv')
    xlsx_path = os.path.join('data', 'sales_financial_dataset.xlsx')
    
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False, engine='openpyxl')
    
    print(f"Dataset successfully created!")
    print(f"Total Rows: {len(df):,}")
    print(f"Total Sales: ${df['Sales'].sum():,.2f}")
    print(f"Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"Avg Profit Margin: {(df['Profit'].sum() / df['Sales'].sum()) * 100:.2f}%")
    print(f"Saved to:\n - {csv_path}\n - {xlsx_path}")
