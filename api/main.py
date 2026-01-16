from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from nl2sql.generator import generate_sql
from nl2sql.validator import validate_sql
from nl2sql.executor import execute_sql


app = FastAPI(
    title="NL2SQL GenAI API",
    description="Natural Language to SQL using LLM + RAG",
    version="1.0.0"
)


# -------------------------
# Request models
# -------------------------
class NLQuery(BaseModel):
    question: str


class SQLQuery(BaseModel):
    sql: str


# -------------------------
# Endpoints
# -------------------------
@app.post("/nl2sql")
def nl2sql_endpoint(payload: NLQuery):
    """
    Convert natural language to SQL and execute it safely.
    """
    try:
        sql = generate_sql(payload.question)
        validate_sql(sql)
        result = execute_sql(sql)

        return {
            "question": payload.question,
            "sql": sql,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/validate")
def validate_endpoint(payload: SQLQuery):
    """
    Validate SQL without executing.
    """
    try:
        validate_sql(payload.sql)
        return {"status": "valid"}

    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")



@app.get("/schema")
def schema_endpoint():
    """
    Return database schema info.
    """
    return {
        "tables": {
            "customers": [
                "customer_id", "first_name", "last_name",
                "gender", "age_group", "signup_date", "country"
            ],
            "orders": [
                "order_id", "customer_id",
                "order_date", "order_status", "payment_method"
            ],
            "order_items": [
                "order_item_id", "order_id",
                "product_id", "quantity", "unit_price"
            ],
            "products": [
                "product_id", "product_name",
                "category", "unit_price"
            ],
            "reviews": [
                "review_id", "customer_id",
                "product_id", "rating", "review_text", "review_date"
            ]
        }
    }
