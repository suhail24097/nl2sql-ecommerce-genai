import requests
import json
import time

API_URL = "http://127.0.0.1:8000/nl2sql"

with open("tests/test_queries.json") as f:
    queries = json.load(f)

results = []

for q in queries:
    start = time.time()
    try:
        response = requests.post(
            API_URL,
            json={"question": q["question"]}
        )
        elapsed = round((time.time() - start) * 1000, 2)

        results.append({
            "id": q["id"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "status": response.status_code,
            "time_ms": elapsed,
            "success": response.status_code == 200,
            "response": response.text
        })

    except Exception as e:
        results.append({
            "id": q["id"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "status": "error",
            "error": str(e),
            "success": False
        })

# print(results)
print("\nEvaluation Results:\n")
for r in results:
    # print(json.dumps(r, indent=2))
    # print("-" * 60)
    with open("tests/test_results.json", "w") as f:
        json.dump(results, f, indent=2)

