import requests

def test_get_post():
    response=requests.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
    data=response.json()
    assert data["userId"] == 1
    assert data["id"] == 1
    assert 'title' in data

def test_create_post():
    new_post={
        "title": "Тестовый пост",
        "body": "Тело поста",
        "userId": 1
    }
    response=requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)
    assert response.status_code == 201
    data=response.json()
    assert data["userId"] == new_post["userId"]
    assert data["title"] == new_post["title"]
    assert data["body"] == new_post["body"]
