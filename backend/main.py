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
    payments
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

    # 🤖 fallback to LLM
    try:
        prompt = f"""
Classify query into:
trace / broken / product / general

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
    # FALLBACK
    # -------------------------------
    return {
        "answer": "Ask about orders, delivery, billing or trace."
    }