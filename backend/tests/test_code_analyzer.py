import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_code_analyzer_and_memory_update():
    # Login as demo user
    resp = client.post(
        "/api/auth/login",
        json={"email": "demo@codepilot.dev", "password": "Demo1234!"}
    )
    token = resp.json()["access_token"]

    # Submit binary search solution
    submission = {
        "problem_title": "Find Peak Element in Mountain Array",
        "problem_statement": "Given a mountain array, find the index of the peak element in O(log n) time.",
        "language": "python",
        "user_code": """def findPeak(arr):\n    low, high = 0, len(arr) - 1\n    while low < high:\n        mid = (low + high) // 2\n        if arr[mid] < arr[mid + 1]:\n            low = mid + 1\n        else:\n            high = mid\n    return low"""
    }

    analyze_resp = client.post(
        "/api/code/analyze",
        headers={"Authorization": f"Bearer {token}"},
        json=submission
    )
    assert analyze_resp.status_code == 200
    data = analyze_resp.json()

    # Validate schema response
    assert data["time_complexity"] in ["O(log n)", "O(n)"]
    assert len(data["concepts_detected"]) > 0
    assert "hint_1" in data and len(data["hint_1"]) > 0
    assert "hint_2" in data and len(data["hint_2"]) > 0
    assert "deeper_explanation" in data
    assert "ai_model_used" in data

    # Verify that Personal Knowledge Memory updated
    concepts_resp = client.get(
        "/api/knowledge/concepts",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert concepts_resp.status_code == 200
    concepts = concepts_resp.json()
    bsearch = next((c for c in concepts if "Binary Search" in c["name"]), None)
    assert bsearch is not None
    assert bsearch["practice_count"] >= 14
