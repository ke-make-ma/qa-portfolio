import requests

response=requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)
print(response.json())

new_post={
    "title": "Тестовый пост",
    "body": "Тело поста",
    "userId": 1
}

response=requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)
print(response.status_code)
print(response.json())