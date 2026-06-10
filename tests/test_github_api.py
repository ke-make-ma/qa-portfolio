import requests
import json
import os
TOKEN = os.getenv("GITHUB_TOKEN")
assert TOKEN, "GITHUB_TOKEN not set"

headers={"Authorization":f"Bearer {TOKEN}"}
BASE_URL = os.getenv("API_BASE_URL", "https://api.github.com")

with open ("tests/fixtures/test_repo.json", 'r') as file:
    TEST_DATA=json.load(file)

def test_create_and_delete_repository():
    create_response=requests.post(f"{BASE_URL}/user/repos",json=TEST_DATA,headers=headers)
    assert create_response.status_code == 201
    assert create_response.json()["name"] == TEST_DATA["name"]
    repo_full_name = create_response.json()["full_name"]

    delete_url = f"{BASE_URL}/repos/{repo_full_name}"
    delete_response=requests.delete(delete_url,headers=headers)
    assert delete_response.status_code == 204

    get_response=requests.get(delete_url,headers=headers)
    assert get_response.status_code == 404

