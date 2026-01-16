# NL2SQL E-Commerce System

An end-to-end Natural Language to SQL (NL2SQL) system that allows users to query
an e-commerce database using plain English.
The system safely converts natural language queries into SQL, validates them,
executes them on a PostgreSQL database, and returns structured results via a REST API.

---

##  Features

- Natural language to SQL conversion using a Large Language Model (LLM)
- Safe SQL execution with strict validation (SELECT-only)
- Retrieval-Augmented Generation (RAG) for schema grounding
- REST API built with FastAPI
- PostgreSQL database running in Docker
- Swagger UI for easy API testing
- Evaluation framework with success and latency metrics

---

##  System Architecture

User Query
↓
FastAPI (/nl2sql)
↓
LLM (Mistral via Ollama)
↓
SQL Post-processing
↓
SQL Validation (Safety Rules)
↓
PostgreSQL (Docker)
↓
Query Results

---

##  Tech Stack

- **Backend**: FastAPI
- **LLM**: Mistral (served locally via Ollama)
- **Vector Store**: FAISS
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Language**: Python 3
- **API Docs**: Swagger UI

---

##  Project Structure

nl2sql-ecommerce/
├── api/ # FastAPI application
├── nl2sql/ # NL2SQL core logic (generator, validator, executor)
├── tests/ # Test queries and evaluation results
├── notebooks/ # Evaluation script
├── docker-compose.yml # Docker services (Postgres, Ollama)
├── schema.sql # Database schema
├── seed_data.sql # Data loading script
├── REPORT.md # Technical report
├── README.md # Project documentation
└── venv/ # Python virtual environment

---

## Relationship Diagram - 
A Neo4j-style relationship diagram is provided in `data/relationship_diagram.png`, representing the knowledge graph equivalent of the relational schema.
I modeled the relational e-commerce schema as a Neo4j graph to explicitly capture entity relationships.
Customers place orders, orders contain items, items map to products, and products belong to categories.
This graph representation helps in understanding joins and schema reasoning for NL2SQL.

##  Setup Instructions

### 1️ Prerequisites

- Python 3.11.x
- Docker Desktop (running)
- Ollama installed

---

### 2️ Clone the Repository

bash:-
git clone <repository-url>
cd nl2sql-ecommerce

### 3️ Create and Activate Virtual Environment :-
python -m venv venv
venv\Scripts\activate   # Windows

### 4️ Install Python Dependencies :-
pip install -r requirements.txt

### 5️ Start Docker Services :-
docker compose up -d

And also Ensure the following containers are running:
1. ecommerce_postgres
2. ollama

### 6️ Pull LLM Model:-
ollama pull mistral

### 7️ Start FastAPI Server:-
uvicorn api.main:app --reload

The API will be available at: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs

API Endpoints:-

## 7.1 POST /nl2sql
Which Generate and execute SQL from natural language.
Request - 
{
  "question": "Total sales by category"
}

Response
{
  "question": "Total sales by category",
  "sql": "SELECT ...",
  "result": [...]
}

## 7.2 POST /validate
Which Validate SQL without executing it.

Request
{
  "sql": "SELECT * FROM products"
}

## 7.3 GET /schema
Retrieve database schema metadata.


### 8 Evaluation:-
Evaluation was performed using real HTTP requests to the running API, 
Test queries include easy, medium, hard, and unsafe cases
Unsafe queries are intentionally blocked

Results are documented in tests/test_results.md

## To run evaluation:
python notebooks/evaluation.py

### 9. Safety & Validation:-

Only SELECT queries are allowed
Destructive operations (DELETE, DROP, UPDATE, TRUNCATE) are blocked
Invalid schema references are rejected
SQL output is post-processed to remove malformed LLM responses

### 10. Known Limitations :-

High latency due to CPU-based local LLM inference
Ambiguous natural language terms may be rejected
No query caching implemented

