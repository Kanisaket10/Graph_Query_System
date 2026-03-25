# AI Usage Logs

## Tools Used
- ChatGPT
- Groq API (LLaMA 3.1)

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

---

## 6. Intent Detection

**Prompt:**
How to classify user queries using LLM?

**Outcome:**
- Implemented detect_intent()
- Replaced hardcoded if-else logic
- Enabled dynamic query understanding

---

## 7. Chat → Graph Integration

**Prompt:**
How to highlight graph nodes based on chat response?

**Outcome:**
- Used related_ids from backend
- Connected chat responses to graph highlighting

---

## Summary

AI was used for:
- Designing system architecture
- Debugging issues
- Improving UI and UX
- Enhancing LLM reasoning
- Writing structured prompts

This iterative process helped refine both backend logic and frontend visualization.