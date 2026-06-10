import pytest
import requests
import json

import os
TOKEN = os.getenv("GITHUB_TOKEN")
assert TOKEN, "GITHUB_TOKEN not set"


with open ("tests/test_repo.json", 'r') as file:
    TEST_DATA=json.load(file)


def test_create_repo():
    response=requests.delete("https://api.github.com/user/repos",json=TEST_DATA)
    assert response.status_code == 201
    assert response.json()["name"] == TEST_DATA["name"]