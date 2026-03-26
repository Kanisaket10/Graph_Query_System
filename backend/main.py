# -------------------------------
# IMPORTS
# -------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import json
import re
from groq import Groq
import os
from dotenv import load_dotenv


from load_data import (
    sales_orders,
    sales_items,
    delivery_items,
    billing_items,
    payments,
    products
)

load_dotenv()

# -------------------------------
# LLM CLIENT
# -------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# -------------------------------
# APP INIT
# -------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# REQUEST MODEL
# -------------------------------
class QueryRequest(BaseModel):
    query: str


# -------------------------------
# 🔥 INTENT DETECTION (HYBRID FIX)
# -------------------------------
def detect_intent(user_query):

    # ✅ RULE-BASED FIRST (VERY IMPORTANT)
    if "trace" in user_query:
        return "trace"

    if "not billed" in user_query or "broken" in user_query:
        return "broken"

    if "product" in user_query:
        return "product"

    if (
        ("highest" in user_query or "top" in user_query or "most" in user_query)
        and ("delivery" in user_query or "deliveries" in user_query)
    ):
        return "top_delivery"

    # 🤖 fallback to LLM
    try:
        prompt = f"""
Classify query into:
trace / broken / product / top_delivery / general

Query: {user_query}
Return ONLY label.
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content.strip().lower()

    except:
        return "general"

def get_first_existing_col(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


# -------------------------------
# 🔥 LLM RESPONSE
# -------------------------------
def ask_llm(user_query, context):
    if not GROQ_API_KEY or client is None:
        return "LLM is not configured. Set GROQ_API_KEY on the backend environment."

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an SAP Order-to-Cash expert.

STRICT:
- Use ONLY given data
- NO hallucination
- Explain clearly WHY
- Keep answer short (3–4 lines)
- Use only business/domain language (order, delivery, billing, payment, customer, product)
- Do NOT mention implementation details (Python, pandas, DataFrame, API, model, prompt, backend)
- Do NOT say "I assume"
- If data is missing, say: "Insufficient data in provided dataset."
"""
                },
                {
                    "role": "user",
                    "content": f"{context}\n\nQuestion: {user_query}"
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as exc:
        print(f"LLM call failed: {exc}")
        return "LLM request failed. Check GROQ_API_KEY validity/credits and backend logs."


# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def home():
    return {"message": "API running 🚀"}


# -------------------------------
# GRAPH
# -------------------------------
@app.get("/graph")
def get_graph():
    with open("graph.json") as f:
        return json.load(f)


# -------------------------------
# MAIN QUERY API
# -------------------------------
@app.post("/query")
def query_data(req: QueryRequest):

    user_query = req.query.lower()

    intent = detect_intent(user_query)
    print("INTENT:", intent)

    # -------------------------------
    # 🔥 FIX TYPE ISSUE ONCE
    # -------------------------------
    sales_orders["salesOrder"] = sales_orders["salesOrder"].astype(str)
    delivery_items["referenceSdDocument"] = delivery_items["referenceSdDocument"].astype(str)
    billing_items["referenceSdDocument"] = billing_items["referenceSdDocument"].astype(str)

    # -------------------------------
    # TRACE
    # -------------------------------
    if intent == "trace":

        order_match = re.findall(r'\d+', user_query)

        if order_match:
            sample_order = order_match[0]
        else:
            sample_order = sales_orders.iloc[0]["salesOrder"]

        deliveries = delivery_items[
            delivery_items["referenceSdDocument"] == sample_order
        ]["deliveryDocument"].astype(str).unique()

        billings = billing_items[
            billing_items["referenceSdDocument"].isin(deliveries)
        ]["billingDocument"].astype(str).unique()

        payments_list = payments[
            payments["invoiceReference"].astype(str).isin(billings)
        ]["accountingDocument"].astype(str).unique()

        related_ids = (
            [sample_order]
            + list(deliveries)
            + list(billings)
            + list(payments_list)
        )

        answer = ask_llm(
            user_query,
            f"Order: {sample_order}, Deliveries: {deliveries}, Billings: {billings}, Payments: {payments_list}"
        )

        return {"answer": answer, "related_ids": related_ids}

    # -------------------------------
    # 🔥 BROKEN FLOW (FINAL FIX)
    # -------------------------------
    elif intent == "broken":

        broken_orders = []

        for _, order in sales_orders.iterrows():
            order_id = order["salesOrder"]

            has_delivery = not delivery_items[
                delivery_items["referenceSdDocument"] == order_id
            ].empty

            has_billing = not billing_items[
                billing_items["referenceSdDocument"] == order_id
            ].empty

            if has_delivery and not has_billing:
                broken_orders.append(order_id)

        print("BROKEN:", broken_orders[:10])

        answer = ask_llm(
            user_query,
            f"Orders delivered but not billed: {broken_orders[:10]}"
        )

        return {
            "answer": answer,
            "related_ids": broken_orders[:10]
        }

    # -------------------------------
    # TOP PRODUCTS BY BILLING DOC COUNT
    # -------------------------------
    elif intent == "product":
        top_n_match = re.search(r"\btop\s+(\d+)\b", user_query)
        top_n = int(top_n_match.group(1)) if top_n_match else 10

        product_col = get_first_existing_col(
            billing_items,
            ["material", "product", "productId", "materialNumber", "sku"]
        )
        billing_doc_col = get_first_existing_col(
            billing_items,
            ["billingDocument", "billingDoc", "invoiceDocument", "invoiceReference"]
        )

        if not product_col or not billing_doc_col:
            return {
                "answer": "Product billing analysis is unavailable: required product or billing columns are missing.",
                "related_ids": []
            }

        product_counts = (
            billing_items[[product_col, billing_doc_col]]
            .dropna()
            .groupby(product_col)[billing_doc_col]
            .nunique()
            .sort_values(ascending=False)
            .head(top_n)
        )

        if product_counts.empty:
            return {
                "answer": "No product-billing links found in data.",
                "related_ids": []
            }

        top_products = product_counts.index.astype(str).tolist()
        list_lines = [
            f"{idx}. {product} - {int(count)} billing docs"
            for idx, (product, count) in enumerate(product_counts.items(), start=1)
        ]
        counts_text = "\n".join(list_lines)

        return {
            "answer": f"Top {len(top_products)} products by billing document count:\n{counts_text}",
            "related_ids": top_products
        }

    # -------------------------------
    # TOP ORDERS BY DELIVERY COUNT
    # -------------------------------
    elif intent == "top_delivery":
        top_n_match = re.search(r"\btop\s+(\d+)\b", user_query)
        top_n = int(top_n_match.group(1)) if top_n_match else 10

        delivery_counts = (
            delivery_items.groupby("referenceSdDocument")["deliveryDocument"]
            .nunique()
            .sort_values(ascending=False)
            .head(top_n)
        )

        if delivery_counts.empty:
            return {
                "answer": "No delivery-linked orders found in data.",
                "related_ids": []
            }

        top_orders = delivery_counts.index.astype(str).tolist()
        list_lines = [
            f"{idx}. {order} - {int(count)} deliveries"
            for idx, (order, count) in enumerate(delivery_counts.items(), start=1)
        ]
        counts_text = "\n".join(list_lines)

        return {
            "answer": f"Top {len(top_orders)} orders by delivery count:\n{counts_text}",
            "related_ids": top_orders
        }

    # -------------------------------
    # FALLBACK
    # -------------------------------
    return {
        "answer": "Ask about orders, delivery, billing, trace, or top deliveries."
    }