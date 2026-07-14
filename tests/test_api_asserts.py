import requests
import pytest
from api_client import BASE_URL, check_response
import json

with open("tests/fixtures/test_data.json", "r") as file:
    TEST_DATA=json.load(file)

#GET
@pytest.mark.parametrize("post_id", TEST_DATA["post_id"])
def test_get_post(post_id):
    response=requests.get(f"{BASE_URL}/posts/{post_id}")
    data=check_response(response, 200)
    assert data["id"]==post_id

@pytest.mark.parametrize("post_id, expected_status",
    [(1,200),
    (0,404),
    (-1,404),
    ('abc',404),
    (999,404)])
def test_get_post_for_different_ids(post_id, expected_status):
    response=requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == expected_status

#POST
def test_create_post():
    new_post={
        "title": "Тестовый пост",
        "body": "Тело поста",
        "userId": 1
    }
    response=requests.post(f"{BASE_URL}/posts", json=new_post)
    data=check_response(response, 201)
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
    data=check_response(response, 201)
    assert isinstance(data["id"], int)
    assert data["userId"] == new_post["userId"]
    assert data["title"] == new_post["title"]
    assert data["body"] == new_post["body"]

def test_create_post_empty_body():
    response = requests.post(f"{BASE_URL}/posts", json={})
    assert response.status_code in (400, 201)

#UPDATE
def test_update_post():
    updated_post={"title":"Updated title", "body":"New body"}
    response=requests.put(f"{BASE_URL}/posts/1",json=updated_post)
    data=check_response(response, 200)
    assert updated_post["title"]==data["title"]

#DELETE
@pytest.mark.parametrize("post_id",[5,6,7])
def test_delete_post(post_id):
    response=requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code in (200,204)
    
def test_delete_post_then_get():
    new_post={
        "title":"To delete",
        "body":"Body", 
        "userId":3
        }    
    response=requests.post(f"{BASE_URL}/posts", json=new_post)
    post_id = check_response(response, 201)["id"]

    response=requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code in (200,204)

    response=requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 404

#PATCH
def test_patch_post():
    get_response=requests.get(f"{BASE_URL}/posts/1")
    original = check_response(get_response, 200)

    patch_data={"title":"Patched title"}
    patch_response=requests.patch(f"{BASE_URL}/posts/1", json=patch_data)
    updated = check_response(patch_response, 200)

    assert updated["id"] == original["id"]
    assert updated["title"] == patch_data["title"]
    assert updated["body"] == original["body"]
    assert updated["userId"] == original["userId"]

#HEAD
def test_head_post():
    response=requests.head(f"{BASE_URL}/posts/1")
    assert response.status_code in (200,204)
    assert "application/json" in response.headers.get("Content-Type", "")
    assert response.text == "" #проверка, что HEAD не возвращает тело

#OPTIONS
def test_options_post():
    response=requests.options(f"{BASE_URL}/posts/1")
    assert response.status_code in (200,204)

#all methods
def test_allowed_methods():
    assert requests.get(f"{BASE_URL}/posts/1").status_code == 200
    assert requests.post(f"{BASE_URL}/posts/1").status_code != 405
    assert requests.put(f"{BASE_URL}/posts/1", json={}).status_code in (200, 204)
    assert requests.delete(f"{BASE_URL}/posts/1").status_code in (200, 204)

#Негативные тесты
def test_create_post_empty_expected_error():
    new_post={"title":""}
    response=requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code!=500
    assert response.status_code in (201,400)