<!-- # React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project. -->



# Graph-Based Data Modeling and Query System

## Overview
This project converts fragmented business data (orders, deliveries, billing, payments) into a connected graph and allows users to explore it using natural language queries.

---

## Architecture

### Backend
- FastAPI
- Pandas for data processing
- NetworkX for graph construction
- Groq LLM (LLaMA 3.1)

### Frontend
- React + Vite
- React Flow for graph visualization

---

## Graph Model

### Nodes
- Orders
- Deliveries
- Billing Documents
- Payments
- Products
- Customers

### Edges
- Order → Delivery
- Delivery → Billing
- Billing → Payment

---

## LLM Integration

We use Groq API with LLaMA 3.1 model.

### Strategy:
- Rule-based data extraction (ensures accuracy)
- LLM used for:
  - Natural language understanding
  - Explanation generation

### Prompt Design:
- No hallucination
- Dataset-grounded answers only
- Business-focused explanation

---

## Features

### Graph
- Interactive graph (zoom, pan, minimap)
- Force-directed layout
- Node highlighting

### Chat
- Natural language queries
- LLM-based explanations
- Graph highlighting using related_ids

### Guardrails
- Restricts queries to dataset domain

---

## Example Queries

- Which products have highest billing?
- Trace order 740508
- Why are some orders not billed?
- Show broken flows

---

## Key Design Decisions

### Why Graph?
To visualize relationships between entities clearly.

### Why NetworkX?
Simple, flexible graph modeling.

### Why Groq?
Fast inference + free tier access.

---

## Limitations

- Payment data may be missing for some billing documents
- Uses partial dataset context for LLM

---

## Future Improvements

- Graph clustering
- Advanced filtering
- Streaming LLM responses

---

## Setup

### Backend
```bash
pip install fastapi uvicorn pandas networkx groq
uvicorn main:app --reload