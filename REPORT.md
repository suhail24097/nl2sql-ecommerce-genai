# NL2SQL System Report

## 1. Introduction
This project implements an end-to-end Natural Language to SQL (NL2SQL) system
for querying an e-commerce database using plain English queries.
The system converts user questions into SQL, validates them for safety,
executes them on a relational database, and returns structured results via a REST API.

The primary goal of this project is to demonstrate:
- Reliable natural language to SQL conversion
- Safe and controlled SQL execution
- Practical evaluation of a GenAI-powered database querying system

---

## 2. Dataset and Database Design

### 2.1 Dataset
The system uses an e-commerce dataset containing approximately 10,000 records.
The dataset includes information about customers, products, orders, order items,
and product reviews.

### 2.2 Database Schema
The dataset is modeled into a PostgreSQL relational database with the following tables:

- **customers**: customer profile and demographic information  
- **products**: product metadata and categories  
- **orders**: order-level transaction details  
- **order_items**: line-item level purchase details  
- **reviews**: customer ratings and textual feedback  

Relationships between tables are defined using primary and foreign keys.
This normalized schema enables complex analytical queries involving joins
and aggregations.

---

## 3. System Architecture

### 3.1 High-Level Architecture
The system consists of the following components:

1. **FastAPI Backend**
   - Exposes REST endpoints for query generation, validation, and schema access

2. **Large Language Model (LLM)**
   - Mistral model served locally using Ollama
   - Responsible for converting natural language into SQL

3. **Retrieval-Augmented Generation (RAG)**
   - Schema information and examples are embedded and retrieved
   - Helps ground SQL generation and reduce hallucinations

4. **SQL Validator**
   - Enforces read-only queries
   - Blocks unsafe operations such as DELETE, DROP, UPDATE, and TRUNCATE

5. **PostgreSQL Database**
   - Stores and executes validated SQL queries
   - Runs inside Docker for reproducibility

---

## 4. API Design

The FastAPI application exposes the following endpoints:

### 4.1 POST /nl2sql
- Accepts a natural language question
- Generates SQL using the LLM
- Validates the generated SQL
- Executes the query if safe
- Returns SQL and query results

### 4.2 POST /validate
- Accepts a raw SQL query
- Performs syntax, safety, and schema validation
- Does not execute the query

### 4.3 GET /schema
- Returns database schema metadata
- Useful for inspection, debugging, and future frontend integration

---

## 5. Model and Prompting Strategy

### 5.1 Model Choice
- **Model**: Mistral
- **Deployment**: Local inference via Ollama (CPU-based)

The model was chosen for its strong reasoning capability and suitability
for local deployment without external API dependencies.

## Agentic Orchestration Design

The NL2SQL system is implemented using an agentic orchestration approach, where the task of converting natural language into executable SQL is decomposed into multiple coordinated steps (agents), rather than relying on a single-purpose LLM call.

The pipeline consists of the following agents:

a. **Schema-Aware Generation Agent**
   - Converts the user’s natural language question into SQL.
   - Injects relevant table schemas and column information dynamically.
   - Augments the prompt using retrieved few-shot examples from a vector database (RAG).

b. **Validation Agent**
   - Performs SQL syntax validation.
   - Verifies table and column existence against the database schema.
   - Enforces safety constraints by blocking destructive operations such as `DROP`, `DELETE`, `UPDATE`, and `TRUNCATE`.

c. **Execution Agent**
   - Executes only validated and safe `SELECT` queries on the PostgreSQL database.
   - Collects and formats query results for API responses.

d. **Self-Correction Agent**
   - If SQL generation or execution fails, the error message is sent back to the LLM.
   - The model attempts to regenerate a corrected SQL query based on feedback.

So implemented procedurally within the FastAPI service, this multi-step design follows an agentic orchestration paradigm, where each agent has a clearly defined responsibility. This approach improves reliability, safety, and interpretability compared to a single monolithic LLM call.


### 5.2 Prompting Strategy
The prompt includes:
- Database schema information
- Explicit instruction to generate only SELECT queries
- Constraints to avoid unsafe SQL operations

### 5.3 Output Post-processing
To improve robustness:
- Markdown formatting (```sql) is removed
- Extraneous text is stripped
- SQL output is forced to start at the SELECT keyword

This significantly improves execution reliability.

---

## 6. SQL Validation and Safety

To ensure database safety, the following validation rules are enforced:

- Only SELECT queries are allowed
- Destructive keywords (DELETE, DROP, UPDATE, TRUNCATE) are blocked
- Queries referencing unknown tables or columns are rejected

Unsafe or invalid queries return HTTP 400 responses.
Infrastructure or database errors return HTTP 500 responses.

This strict validation layer prevents accidental or malicious data modification.

---

## 7. Evaluation Methodology

### 7.1 Test Setup
Evaluation was conducted using a Python script that sends real HTTP requests
to the running FastAPI service.

Test queries were categorized as:
- Easy
- Medium
- Hard
- Unsafe (failure cases)

All tests were executed against a live PostgreSQL database and LLM.

### 7.2 Evaluation Results
A total of 4 representative queries were evaluated:

- 3 valid analytical queries executed successfully
- 1 unsafe query was correctly blocked

- **Success rate (valid queries): 100%**
- **Overall success rate: 75%**

### 7.3 Latency Analysis
- Average response time per query: ~40–55 seconds
- Latency is dominated by local CPU-based LLM inference
- SQL execution time is negligible in comparison

---

## 8. Observations and Challenges

### 8.1 Observations
- The system successfully handled multi-table joins and aggregations
- RAG-based grounding improved SQL accuracy
- Output post-processing reduced malformed SQL generation

### 8.2 Challenges
- LLM latency on CPU-based local inference
- Occasional markdown-formatted SQL output
- Handling ambiguous natural language terms (e.g., “profit”, “region”)

---

## 9. Conclusion

This project demonstrates a complete and safe NL2SQL pipeline using
modern GenAI techniques.
The system effectively translates natural language queries into executable SQL,
enforces strict safety constraints, and provides measurable evaluation results.

The architecture is modular, extensible, and suitable for future enhancements
such as UI integration, caching, or graph-based schema reasoning.
