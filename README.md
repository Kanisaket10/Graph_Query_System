# Graph-Based Data Modeling and Query System

## Overview
This project models SAP Order-to-Cash (O2C) lifecycle data as a graph and answers domain questions through a chat interface.  
It combines deterministic data logic (for accuracy) with LLM-generated business explanations (for readability).

---

## Architecture Decisions

### 1) Two-tier architecture
- **Frontend**: React + Vite + React Flow
- **Backend**: FastAPI + Pandas + Graph generation endpoint
- **Reason**: Separates UI concerns from query/data logic, makes deployment and debugging easier.

### 2) Deterministic logic first, LLM second
- Backend computes key answers (trace, broken flows, top deliveries, top products) using dataframe operations.
- LLM is used to convert computed context into short business explanations.
- **Reason**: Reduces hallucination risk and improves consistency for evaluation queries.

### 3) Graph-based visualization for process understanding
- Entities are represented as nodes and lifecycle links as edges.
- **Reason**: O2C data is inherently relationship-driven (Order -> Delivery -> Billing -> Payment).

---

## Database Choice

### Chosen approach
- **No external DB** is used in this version.
- Data is loaded from provided `.jsonl` files into **Pandas DataFrames** at backend startup.

### Why this choice
- Dataset is bounded and read-heavy for analytical queries.
- Fast iteration for assignment scope (no schema migration/DB setup overhead).
- Simple local + cloud deployment.

### Tradeoff
- Not ideal for very large datasets or high concurrency; production scale could migrate to PostgreSQL/graph DB.

---

## LLM Prompting Strategy

### Model
- Groq API with `llama-3.1-8b-instant`.

### Prompt strategy
- System prompt enforces:
  - use only provided dataset context
  - no hallucination
  - business-domain language only
  - no implementation leakage (Python/pandas/API/model details)
  - avoid uncertain phrasing like "I assume"
- Missing-data behavior is explicit and controlled.

### Query handling flow
1. Rule-based intent detection (`trace`, `broken`, `product`, `top_delivery`).
2. Deterministic data aggregation/tracing in backend.
3. LLM explanation over computed context (where needed).

---

## Guardrails

The system includes explicit safeguards:

1. **Domain restriction**
- Queries are routed to O2C-specific intents and fallback prompts users to ask in supported domain.

2. **Dataset grounding**
- Answers are generated from computed context derived from dataset tables.

3. **No internal-tech disclosure**
- Prompt instructs model not to reveal backend implementation details.

4. **Missing/invalid input handling**
- Trace queries without IDs return guided prompts (example IDs).
- Invalid document IDs return clear "no matching flow" messages.

5. **Fallback behavior**
- Unsupported questions return a controlled domain hint, not fabricated output.

---

## Graph Model

### Nodes
- Sales Orders
- Deliveries
- Billing Documents
- Payments
- Products
- Customers

### Edges
- Sales Order -> Delivery
- Delivery -> Billing
- Billing -> Payment

---

## Supported Example Queries

- `which products are associated with the highest number of billing documents`
- `top 5 orders by deliveries`
- `which orders are not billed`
- `trace order 740506`
- `trace billing document 90012345`

---

## Setup and Run

## 1) Backend (FastAPI)

From project root:

```bash
cd backend
pip install fastapi uvicorn pandas python-dotenv groq
uvicorn main:app --reload
```

Backend runs on:
- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

Required backend env var:
- `GROQ_API_KEY=<your_key>`

## 2) Frontend (React + Vite)

From project root:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:
- `http://localhost:5173`

Frontend env var:
- `VITE_API_URL=<backend_base_url>`

---

## Deployment Notes (Render)

- Backend: Render Web Service (FastAPI)
- Frontend: Render Static Site (root `frontend`, publish `dist`)
- Ensure frontend env points to backend URL:
  - `VITE_API_URL=https://<your-backend>.onrender.com`

---

## Limitations

- Some records may not complete full O2C lifecycle in dataset (expected gaps).
- Rule-based intents cover assignment scope; broader NL coverage can be improved.

---

## Future Improvements

- Add stronger intent parser for complex multi-condition queries.
- Add caching/indexing for faster large-data queries.
- Add authentication and query logging for production usage.