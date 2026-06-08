import requests
import pytest

BASE_URL="https://jsonplaceholder.typicode.com"
#Вспомогательная
def check_response(response, expected_status):
    assert response.status_code == expected_status
    assert response.elapsed.total_seconds() < 2.0
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
    post_id=response.json()["id"]
    assert response.status_code == 201 #стоит ли вместо этого использовать функцию check_response?

    response=requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code in (200,204)

    response=requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 404

#PATCH
def test_patch_post():
    original=requests.get(f"{BASE_URL}/posts/1").json()
    patch_data={"title":"Patched title"}
    response=requests.patch(f"{BASE_URL}/posts/1", json=patch_data)
    assert response.status_code==200
    data=response.json()
    assert data["title"]==patch_data["title"]
    assert data["body"]==original["body"]
    assert data["userId"] == original["userId"]

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
    # GET должен работать
    assert requests.get(f"{BASE_URL}/posts/1").status_code == 200
    # POST должен работать
    assert requests.post(f"{BASE_URL}/posts/1").status_code != 405
    # PUT должен работать
    assert requests.put(f"{BASE_URL}/posts/1", json={}).status_code != 405
    # DELETE должен работать
    assert requests.delete(f"{BASE_URL}/posts/1").status_code != 405

#Негативные тесты
def test_create_post_empty_expected_error():
    new_post={"title":""}
    response=requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code!=500
    assert response.status_code in (201,400)