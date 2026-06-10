import requests
import os

BASE_URL=os.getenv("API_BASE_URL","https://jsonplaceholder.typicode.com")

def check_response(response, expected_status):
    assert response.status_code == expected_status
    assert response.elapsed.total_seconds() < 2.0
    assert "application/json" in response.headers.get("Content-Type", "")
    return response.json()