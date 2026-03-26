# AI Usage Logs

## Tools Used
- Cursor AI Assistant
- ChatGPT
- Groq API (LLaMA 3.1) for model inference in the app

---

## Workflow Timeline (High Level)
1. Built initial graph pipeline from O2C relational files.
2. Added React Flow visualization and chat panel integration.
3. Debugged graph edge mapping and query routing behavior.
4. Improved backend intents and deterministic aggregations.
5. Hardened prompts/guardrails and deployed backend + frontend on Render.

---

## 1. Graph Construction

**Prompt:**
How to convert relational dataset into graph using NetworkX?

**Outcome:**
- Used directed graph (DiGraph)
- Created nodes for orders, deliveries, billing, payments
- Added edges for relationships

---

## 2. Graph Visualization

**Prompt:**
How to visualize graph using React Flow?

**Outcome:**
- Implemented ReactFlow
- Added node styling (colors by type)
- Added zoom, pan, minimap

---

## 3. Debugging Graph Issues

**Prompt:**
Why are edges not visible in ReactFlow?

**Outcome:**
- Fixed incorrect edge format
- Ensured source/target IDs match nodes
- Removed incorrect filtering
- Verified graph rendering with minimap and zoom controls

---

## 4. LLM Integration

**Prompt:**
How to integrate Groq LLM with FastAPI?

**Outcome:**
- Created ask_llm function
- Added context grounding
- Implemented structured prompts

---

## 5. Prompt Engineering

**Prompt:**
How to prevent hallucination in LLM responses?

**Outcome:**
- Added strict system prompt rules:
  - Use only dataset context
  - Avoid assumptions
  - Provide reasoning
- Prevented internal tech leakage in responses (no Python/pandas/API mentions)
- Added explicit missing-data response behavior

---

## 6. Intent Detection

**Prompt:**
How to classify user queries using LLM?

**Outcome:**
- Implemented detect_intent()
- Added rule-based handling for assignment-critical queries
- Added intent paths for top deliveries and top products by billing count
- Improved trace handling for missing/invalid IDs

---

## 7. Chat → Graph Integration

**Prompt:**
How to highlight graph nodes based on chat response?

**Outcome:**
- Used related_ids from backend
- Connected chat responses to graph highlighting
- Updated chat UI to preserve multiline ranked-list responses

---

## 8. Deployment and Production Debugging

**Prompt:**
How to deploy FastAPI + Vite app on Render and validate env configuration?

**Outcome:**
- Deployed backend as Render Web Service and frontend as Render Static Site
- Set `GROQ_API_KEY` on backend and `VITE_API_URL` on frontend
- Verified redeploy flow and confirmed live endpoints with test queries

---

## Summary

AI was used for:
- Designing system architecture
- Debugging issues
- Improving UI and UX
- Enhancing LLM reasoning
- Writing structured prompts
- Deployment troubleshooting and validation

This iterative process helped refine both backend logic and frontend visualization.