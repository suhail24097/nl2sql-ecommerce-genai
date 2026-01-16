# What the validator will do

# Allow only SELECT
# Block DROP, DELETE, UPDATE, INSERT, ALTER
# Check referenced tables exist
# Fail fast with clear error message

import re

# Allowed tables (schema grounding)
ALLOWED_TABLES = {
    "customers",
    "orders",
    "order_items",
    "products",
    "reviews"
}

# Disallowed SQL keywords
FORBIDDEN_KEYWORDS = {
    "drop",
    "delete",
    "update",
    "insert",
    "alter",
    "truncate",
    "create"
}


def validate_sql(sql: str) -> None:
    """
    Raises ValueError if SQL is unsafe or invalid.
    """

    sql_lower = sql.lower().strip()

    # 1. Must be SELECT query
    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    # 2. Block forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_lower):
            raise ValueError(f"Forbidden SQL keyword detected: {keyword}")

    # 3. Check table usage
    tables_in_query = set(
        re.findall(r"from\s+([a-zA-Z_]+)|join\s+([a-zA-Z_]+)", sql_lower)
    )

    extracted_tables = {
        table
        for group in tables_in_query
        for table in group
        if table
    }

    for table in extracted_tables:
        if table not in ALLOWED_TABLES:
            raise ValueError(f"Unknown or unauthorized table used: {table}")
