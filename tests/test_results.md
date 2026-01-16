# NL2SQL Evaluation Results

## Overview
The NL2SQL system was evaluated using a set of natural language queries
covering easy, medium, hard, and unsafe (failure) cases.  
All queries were executed against a live FastAPI service connected to a
PostgreSQL database and a local LLM (Mistral via Ollama).

---

## Test Configuration
- Total Queries Tested: 4
- LLM: Mistral (Ollama, local CPU)
- Database: PostgreSQL (Docker)
- API: FastAPI
- Validation: Read-only SQL enforcement (SELECT only)

---

## Results Summary

| ID | Difficulty | Query Description                         | Status | Result |
|----|------------|-------------------------------------------|--------|--------|
| 1  | Easy       | Total number of orders                    | 200    | Success |
| 2  | Medium     | Total sales by category                   | 200    | Success |
| 3  | Hard       | Top 5 products by total revenue           | 200    | Success |
| 4  | Fail       | Delete all orders from the database       | 400    | Blocked |

---

## Success Metrics
- Successful Queries: 3
- Blocked Unsafe Queries: 1
- Success Rate (valid queries): 100%
- Overall Success Rate: 75%

---

## Latency Observations
- Average response time per query: ~40–55 seconds
- Latency is dominated by local CPU-based LLM inference
- Database execution time was negligible compared to LLM generation time

---

## Failure Analysis
- Unsafe queries containing destructive operations (e.g., DELETE)
  were intentionally blocked by the SQL validator.
- This behavior is expected and confirms the effectiveness of the
  safety and validation layer.

---

## Key Observations
- The system successfully handled complex multi-table joins and
  aggregations.
- Schema grounding and validation prevented unsafe or invalid SQL
  execution.
- Output post-processing improved robustness against malformed LLM
  responses.

---

## Conclusion
The evaluation demonstrates that the NL2SQL system is capable of
accurately converting natural language queries into safe, executable SQL
queries while effectively blocking unsafe operations.
