import requests
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL="https://jsonplaceholder.typicode.com"
def check_response(response, expected_status):
    assert response.status_code == expected_status
    assert response.elapsed.total_seconds() < 1.0
    assert "application/json" in response.headers.get("Content-Type", "")
    return response.json()

@pytest.mark.parametrize("post_id", [1,2,3])
def test_get_post(post_id):
    response=requests.get(f"{BASE_URL}/posts/{post_id}")
    data=check_response(response,200)
    assert data["id"]==post_id
    assert data["userId"] == 1
    assert 'title' in data

def test_create_post():
    new_post={
        "title": "Тестовый пост",
        "body": "Тело поста",
        "userId": 1
    }
    response=requests.post(f"{BASE_URL}/posts", json=new_post)
    data=check_response(response,201)
    assert isinstance(data["id"],int)
    assert data["userId"] == new_post["userId"]
    assert data["title"] == new_post["title"]
    assert data["body"] == new_post["body"]

def test_get_nonexistent():
    response=requests.get(f"{BASE_URL}/posts/999")
    assert response.status_code == 404

def test_create_post_empty_expected_error():
    new_post={"title":""}
    response=requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code!=500
    assert response.status_code in (201,400)