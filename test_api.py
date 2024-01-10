from fastapi.testclient import TestClient
from main import app  
from io import BytesIO
import base64

client = TestClient(app)

# test for add_user
def test_add_user():
    response = client.post("/post/user", json={
        "username": "levi",
        "password": "swift",
        "profile_info": "midnights"
    })
    assert response.status_code == 200  
    assert response.json() is not None  


# test for add_post 
def test_post_without_image():

    data = {
        "user_id": (None, "1"),  # user_id as string
        "description": (None, "cruel summer")
    }

    response = client.post('/post', data=data)
    print(response.status_code)  # Debugging
    print(response.json()) 
    assert response.status_code == 200
    assert response.json() is not None


# test for add_comment
def test_add_comment():
    response = client.post("/post/comment", json={
        "user_id": 5,
        "post_id": 6,
        "content": "oh wow, that worked. im impressed"
    })
    assert response.status_code == 200  
    assert response.json() is not None 


# test for get_newest_post
def test_get_newest_post():
    response = client.get("/get/posts/newest")
    assert response.status_code == 200


# test for get_comment     
def test_get_comment():
    post_id = 1
    response = client.get(f'/get/comment?post_id={post_id}')
    assert response.status_code == 200
    assert isinstance(response.json(), list) 
    print('test /get/comment:')
    for comment in response.json():
        print(comment[3])


# test for post_like 
def test_post_like():
    data = {
        'user_id': 5, 
        'post_id': 6
    }
    response = client.post('/post/like', json=data)
    assert response.status_code == 200  
    assert response.json() is not None 


# test for get_like
def test_get_like():
    post_id = 6
    response = client.get(f'/get/like?post_id={post_id}')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(response.json())


# test for get_all_posts
def test_get_all_posts():
    response = client.get("/get/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # res = response.json()
    # for d in res:
    #    for a in d:
    #        print(a)
    #        break


# test get_post_byUser
def test_get_post_by_user():
    user_id = 2
    response = client.get(f'/get/post/user?user_id={user_id}')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    for post in response.json():
        print(post[2])


if __name__ == "__main__":
    
    
    # PASSED 
    #test_add_user()
    #test_get_newest_post()
    #test_get_comment()
    #test_add_comment()
    #test_post_like()
    #test_get_like()
    #test_get_all_posts()
    #test_get_post_by_user()

    #FAILED 
    test_post_without_image()
