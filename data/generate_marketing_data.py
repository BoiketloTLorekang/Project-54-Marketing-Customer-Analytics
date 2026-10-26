import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(303)

# --- 1. GENERATE DIM_CHANNELS ---
channels = [
    {'channel_id': 'CHN_01', 'channel_name': 'Paid Search (Google)', 'channel_type': 'PPC'},
    {'channel_id': 'CHN_02', 'channel_name': 'Social Media (Meta/Instagram)', 'channel_type': 'Paid Social'},
    {'channel_id': 'CHN_03', 'channel_name': 'Email Marketing', 'channel_type': 'Retention'},
    {'channel_id': 'CHN_04', 'channel_name': 'Organic Search (SEO)', 'channel_type': 'Organic'},
    {'channel_id': 'CHN_05', 'channel_name': 'Affiliate Partners', 'channel_type': 'Partnership'}
]
df_channels = pd.DataFrame(channels)

# --- 2. GENERATE DIM_CUSTOMERS ---
num_customers = 1500
segments = ['Champions', 'Loyal Customers', 'At Risk', 'Lost', 'New Customers']

customers = []
for i in range(1, num_customers + 1):
    customers.append({
        'customer_id': f'CUST_{i:04d}',
        'signup_date': (datetime(2025, 1, 1) + timedelta(days=int(np.random.randint(0, 300)))).strftime('%Y-%m-%d'),
        'customer_segment': np.random.choice(segments, p=[0.15, 0.30, 0.20, 0.15, 0.20]),
        'country': np.random.choice(['South Africa', 'United Kingdom', 'United States', 'Australia'], p=[0.5, 0.2, 0.2, 0.1])
    })
df_customers = pd.DataFrame(customers)

# --- 3. GENERATE FACT_CAMPAIGNS ---
num_campaigns = 50
campaigns = []

for i in range(1, num_campaigns + 1):
    chan = df_channels.sample(1).iloc[0]
    spend = float(round(np.random.uniform(1000, 15000), 2))
    impressions = int(spend * np.random.uniform(40, 120))
    clicks = int(impressions * np.random.uniform(0.015, 0.055))
    conversions = int(clicks * np.random.uniform(0.03, 0.12))
    revenue = float(round(conversions * np.random.uniform(45, 180), 2))
    
    campaigns.append({
        'campaign_id': f'CMP_{i:03d}',
        'channel_id': chan['channel_id'],
        'campaign_name': f"Campaign {i} - {chan['channel_name'].split()[0]}",
        'start_date': (datetime(2025, 1, 1) + timedelta(days=int(np.random.randint(0, 330)))).strftime('%Y-%m-%d'),
        'spend': spend,
        'impressions': impressions,
        'clicks': clicks,
        'conversions': conversions,
        'revenue_generated': revenue
    })
df_campaigns = pd.DataFrame(campaigns)

# --- 4. GENERATE FACT_TRANSACTIONS ---
num_transactions = 5000
transactions = []

for i in range(1, num_transactions + 1):
    cust = df_customers.sample(1).iloc[0]
    chan = df_channels.sample(1).iloc[0]
    
    order_amount = float(round(np.random.exponential(scale=120) + 20, 2))
    
    transactions.append({
        'transaction_id': f'TRX_{i:06d}',
        'customer_id': cust['customer_id'],
        'channel_id': chan['channel_id'],
        'transaction_date': (datetime(2025, 1, 1) + timedelta(days=int(np.random.randint(0, 355)))).strftime('%Y-%m-%d'),
        'order_value': order_amount,
        'discount_applied': float(round(order_amount * np.random.choice([0, 0.05, 0.10, 0.20], p=[0.5, 0.2, 0.2, 0.1]), 2))
    })
df_transactions = pd.DataFrame(transactions)

# --- 5. EXPORT TO EXCEL ---
file_name = "Project_54_Marketing_Dataset.xlsx"
with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
    df_campaigns.to_excel(writer, sheet_name='Fact_Campaigns', index=False)
    df_transactions.to_excel(writer, sheet_name='Fact_Transactions', index=False)
    df_channels.to_excel(writer, sheet_name='Dim_Channels', index=False)
    df_customers.to_excel(writer, sheet_name='Dim_Customers', index=False)

print(f"Project 54 Marketing Dataset successfully generated and exported to '{file_name}'!")