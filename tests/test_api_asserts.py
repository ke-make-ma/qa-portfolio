import requests
import pytest

BASE_URL="https://jsonplaceholder.typicode.com"
#Вспомогательная
def check_response(response, expected_status):
    assert response.status_code == expected_status
    assert response.elapsed.total_seconds() < 1.0
    assert "application/json" in response.headers.get("Content-Type", "")
    return response.json()

#GET
@pytest.mark.parametrize("post_id", [1,2,3])
def test_get_post(post_id):
    response=requests.get(f"{BASE_URL}/posts/{post_id}")
    data=check_response(response,200)
    assert data["id"]==post_id
    assert data["userId"] == 1
    assert 'title' in data

#POST
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

@pytest.mark.parametrize("userId",[1,2,3])
def test_create_post_for_different_users(userId):
    new_post={
        "title": "test title",
        "body": "test body",
        "userId": userId
    }
    response=requests.post(f"{BASE_URL}/posts", json=new_post)
    data=check_response(response,201)
    assert isinstance(data["id"], int)
    assert data["id"] is not None
    assert data["userId"] == new_post["userId"]
    assert data["title"] == new_post["title"]
    assert data["body"] == new_post["body"]

#UPDATE
def test_update_post():
    updated_post={"title":"Updated title", "body":"New body"}
    response=requests.put(f"{BASE_URL}/posts/1",json=updated_post)
    data=check_response(response,200)
    assert updated_post["title"]==data["title"]

#DELETE
def test_delete_post():
    response=requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code in (200,204)

#Негативные тесты
def test_get_nonexistent():
    response=requests.get(f"{BASE_URL}/posts/999")
    assert response.status_code == 404

def test_create_post_empty_expected_error():
    new_post={"title":""}
    response=requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code!=500
    assert response.status_code in (201,400)

def test_get_string():
    response=requests.get(f"{BASE_URL}/posts/abc")
    assert response.status_code == 404

def test_get_zero():
    response=requests.get(f"{BASE_URL}/posts/0")
    assert response.status_code in (400,404)