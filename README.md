# E-Commerce Database Chat (RAG Demo)

> **Demo Project** — Retrieval-Augmented Generation (RAG) over structured data using LLM-driven SQL agents.

A retrieval-augmented generation (RAG) system that enables **natural-language question answering over a large relational database**.  
Built with **LangChain SQL agents** and **OpenAI**, this project demonstrates how to safely ground LLM responses in **real, structured data** rather than free-form text generation.

The included SQLite database contains **536,000+ real e-commerce transaction records**, allowing realistic analytics and follow-up questions.

---

## What This Project Demonstrates

This project intentionally focuses on **structured-data RAG**, showcasing how to:

- Translate natural language into **schema-aware SQL**
- Ground LLM responses exclusively in database retrieval
- Apply **domain constraints** to reduce hallucinations
- Maintain conversational context across follow-up questions
- Test and validate AI-driven workflows end-to-end

It avoids unnecessary vector search to highlight cases where **classic relational databases are the optimal retrieval layer**.

---

## Architecture Overview

```
User (CLI)
   ↓
LangChain SQL Agent
   ↓
Schema-aware SQL generation
   ↓
SQLite query execution
   ↓
Retrieved rows
   ↓
LLM synthesis grounded in results
```

---

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your OpenAI API key.

---

## Usage

```bash
python chat_cli.py
```

Verbose mode:
```bash
python chat_cli.py -v
```

---

## Project Structure

See repository for full breakdown.

---

## Development

```bash
pytest
black src/ tests/
```

---

## Use Cases

- Conversational analytics
- Internal data exploration
- Business intelligence tooling
- AI-assisted reporting
