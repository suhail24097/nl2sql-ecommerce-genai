import psycopg2
from typing import List, Dict


def execute_sql(sql: str) -> List[Dict]:
    """
    Executes SQL query and returns results as list of dictionaries.
    """

    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce",
        user="postgres",
        password="postgres"
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            results = [
                dict(zip(columns, row))
                for row in rows
            ]

            return results

    finally:
        conn.close()
