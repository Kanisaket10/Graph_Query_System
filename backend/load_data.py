import pandas as pd
import os
import glob

def load_folder(folder_path):
    print(f"\nLoading folder: {folder_path}")
    
    files = glob.glob(os.path.join(folder_path, "*.jsonl"))
    
    df_list = []
    
    for file in files:
        print("Reading:", file)
        df = pd.read_json(file, lines=True)
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df


# Load ALL important tables

sales_orders = load_folder("../sap-o2c-data/sales_order_headers")

sales_items = load_folder("../sap-o2c-data/sales_order_items")

deliveries = load_folder("../sap-o2c-data/outbound_delivery_headers")

delivery_items = load_folder("../sap-o2c-data/outbound_delivery_items")

billing = load_folder("../sap-o2c-data/billing_document_headers")

billing_items = load_folder("../sap-o2c-data/billing_document_items")

customers = load_folder("../sap-o2c-data/business_partners")

products = load_folder("../sap-o2c-data/products")

payments = load_folder("../sap-o2c-data/payments_accounts_receivable")


# Print columns to understand structure
print("\n Orders Columns:", sales_orders.columns)
print("\n Deliveries Columns:", deliveries.columns)
print("\n Billing Columns:", billing.columns)
print("\n Customers Columns:", customers.columns)

print("\nSales Items Columns:", sales_items.columns)
print("\nDelivery Items Columns:", delivery_items.columns)
print("\nBilling Items Columns:", billing_items.columns)
print("\nPayments Columns:", payments.columns)