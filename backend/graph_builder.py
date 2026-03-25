import networkx as nx
import json
from load_data import *
import pandas as pd

G = nx.DiGraph()

# ---------------------------
# 1. Customers
# ---------------------------
for _, row in customers.iterrows():
    G.add_node(str(row['businessPartner']), type="customer")

# ---------------------------
# 2. Orders
# ---------------------------
for _, row in sales_orders.iterrows():
    G.add_node(str(row['salesOrder']), type="order")

# Customer → Order
for _, row in sales_orders.iterrows():
    G.add_edge(
        str(row['soldToParty']),
        str(row['salesOrder']),
        relation="PLACED"
    )

# ---------------------------
# 3. Order Items → Product
# ---------------------------
for _, row in sales_items.iterrows():
    order_id = str(row['salesOrder'])
    product_id = str(row['material'])

    G.add_node(product_id, type="product")
    G.add_edge(order_id, product_id, relation="CONTAINS")

# ---------------------------
# 4. Delivery
# ---------------------------
for _, row in delivery_items.iterrows():
    delivery_id = str(row['deliveryDocument'])
    order_id = str(row['referenceSdDocument'])

    G.add_node(delivery_id, type="delivery")
    G.add_edge(order_id, delivery_id, relation="DELIVERED")

# ---------------------------
# 5. Billing
# ---------------------------
for _, row in billing_items.iterrows():
    billing_id = str(row['billingDocument'])
    delivery_ref = str(row['referenceSdDocument'])

    G.add_node(billing_id, type="billing")
    G.add_edge(delivery_ref, billing_id, relation="BILLED")

# ---------------------------
# 6. Payments
# ---------------------------
for _, row in payments.iterrows():
    payment_id = str(row['accountingDocument'])
    invoice_ref = row['invoiceReference']

    G.add_node(payment_id, type="payment")

    if pd.notna(invoice_ref):
        G.add_edge(str(invoice_ref), payment_id, relation="PAID")

# ---------------------------
# Convert to JSON (ReactFlow compatible)
# ---------------------------
def graph_to_json(G):
    nodes = []
    for n in G.nodes():
        nodes.append({
            "id": str(n),
            "label": str(n),
            "type": G.nodes[n].get("type", "")
        })

    edges = []
    for u, v, data in G.edges(data=True):
        edges.append({
            "source": str(u),
            "target": str(v),
            "label": data.get("relation", "")
        })

    return {"nodes": nodes, "edges": edges}

graph_data = graph_to_json(G)

with open("graph.json", "w") as f:
    json.dump(graph_data, f, indent=2)

print("✅ Graph saved as graph.json")