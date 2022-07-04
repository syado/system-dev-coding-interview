def post_token(email, password, client):
    # POST /token
    response = client.post(
        "/token",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()

def post_users(email, password, client):
    # POST /users/
    response = client.post(
        "/users/",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()

def get_users(token, client):
    # GET /users/
    response = client.get(f"/users/", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    return response.json()

def get_users_userid(token, user_id, client):
    # GET /users/{user_id}
    response = client.get(f"/users/{user_id}", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    return response.json()

def post_users_userid_items(token, user_id, title, description, client):    
    # POST /users/{user_id}/items
    response = client.post(f"/users/{user_id}/items/", headers={"X-API-TOKEN":token},
        json={"title": title, "description": description})
    assert response.status_code == 200, response.text
    return response.json()

def get_items(token, client):
    # GET /items/
    response = client.get("/items/", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    return response.json()

def get_me_items(token, client):
    # GET /me/items/
    response = client.get("/me/items", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    return response.json()

def get_users_userid_delete(token, user_id, client):
    # GET /users/{user_id}/delete
    response = client.get(f"/users/{user_id}/delete", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    return response.json()