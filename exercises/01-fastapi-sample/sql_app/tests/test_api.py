from .test_api_requests import *
 
EMAIL1 = "deadpool@example.com"
PASSWORD1 = "chimichangas4life"
EMAIL2 = "deadpool2@example.com"
PASSWORD2 = "chimichangas4life2"
EMAIL3 = "deadpool3@example.com"
PASSWORD3 = "chimichangas4life3"

ITEM1 = "title1"
ITEM_DES1 = "description1"
ITEM2 = "title2"
ITEM_DES2 = "description2"

def test_create_single_user(test_db, client):
    # POST /users/
    data1 = post_users(EMAIL1, PASSWORD1, client)
    assert data1["email"] == EMAIL1
    assert "id" in data1
    user_id = data1["id"]
    
    # POST /token
    data2 = post_token(EMAIL1, PASSWORD1, client)
    assert "access_token" in data2
    token = data2["access_token"]

    # GET /users/{user_id}
    data3 = get_users_userid(token, user_id, client)
    assert data3["email"] == EMAIL1
    assert data3["id"] == user_id
    
    # GET /users/
    data4 = get_users(token, client)
    assert len(data4) == 1
    assert data4[0]["id"] ==  user_id
    assert data4[0]["email"] == EMAIL1

def test_create_multi_user(test_db, client):
    # POST /users/
    data1 = post_users(EMAIL1, PASSWORD1, client)
    assert data1["email"] == EMAIL1
    assert "id" in data1
    user_id1 = data1["id"]
    
    # POST /users/
    data2 = post_users(EMAIL2, PASSWORD1, client)
    assert data2["email"] == EMAIL2
    assert "id" in data2
    user_id2 = data2["id"]
    
    # POST /token
    data3 = post_token(EMAIL1, PASSWORD1, client)
    assert "access_token" in data3
    token = data3["access_token"]

    # GET /users/
    data4 = get_users(token, client)
    assert len(data4) == 2
    user_list = [user_id1,user_id2]
    for i in data4:
        assert i["id"] in user_list
        if i["id"] in user_list: user_list.remove(i["id"])
        assert i["email"] in [EMAIL1,EMAIL2]
    assert len(user_list) == 0
    
    # GET /users/{user_id}
    data5 = get_users_userid(token, user_id1, client)
    assert data5["email"] == EMAIL1
    assert data5["id"] == user_id1
    
    # GET /users/{user_id}
    data6 = get_users_userid(token, user_id2, client)
    assert data6["email"] == EMAIL2
    assert data6["id"] == user_id2

def test_create_single_item(test_db, client):
    # POST /users/
    data1 = post_users(EMAIL1, PASSWORD1, client)
    assert data1["email"] == EMAIL1
    assert "id" in data1
    user_id = data1["id"]

    # POST /token
    data2 = post_token(EMAIL1, PASSWORD1, client)
    assert "access_token" in data2
    token = data2["access_token"]
    
    # POST /users/{user_id}/items
    data3 = post_users_userid_items(token, user_id, ITEM1, ITEM_DES1, client)
    assert data3["title"] == ITEM1
    assert data3["description"] == ITEM_DES1
    assert data3["owner_id"] == user_id 
    item_id = data3["id"]

    # GET /items/
    data4 = get_items(token, client)
    assert len(data4) == 1
    assert data4[0]["id"] == item_id
    assert data4[0]["owner_id"] ==  user_id
    assert data4[0]["title"] == ITEM1
    assert data4[0]["description"] == ITEM_DES1
    
    # GET /me/items/
    data5 = get_me_items(token, client)
    assert len(data5) == 1
    assert data5[0]["id"] == item_id
    assert data5[0]["owner_id"] == user_id
    assert data5[0]["title"] == ITEM1
    assert data5[0]["description"] == ITEM_DES1

def test_create_multi_item(test_db, client):
    # POST /users/
    data1 = post_users(EMAIL1, PASSWORD1, client)
    assert data1["email"] == EMAIL1
    assert "id" in data1
    user_id = data1["id"]

    # POST /token
    data2 = post_token(EMAIL1, PASSWORD1, client)
    assert "access_token" in data2
    token = data2["access_token"]
    
    # POST /users/{user_id}/items
    data3 = post_users_userid_items(token, user_id, ITEM1, ITEM_DES1, client)
    assert data3["title"] == ITEM1
    assert data3["description"] == ITEM_DES1
    assert data3["owner_id"] == user_id 
    item_id1 = data3["id"]
    
    data4 = post_users_userid_items(token, user_id, ITEM2, ITEM_DES2, client)
    assert data4["title"] == ITEM2
    assert data4["description"] == ITEM_DES2
    assert data4["owner_id"] == user_id 
    item_id2 = data4["id"]

    # GET /items/
    data5 = get_items(token, client)
    assert len(data5) == 2
    item_list = [item_id1,item_id2]
    for i in data5:
        assert i["id"] in item_list
        if i["id"] in item_list: item_list.remove(i["id"])
        assert i["title"] in [ITEM1, ITEM2]
        assert i["description"] in [ITEM_DES1, ITEM_DES2]
        assert i["owner_id"] == user_id 
    assert len(item_list) == 0
    
    # GET /me/items/
    data6 = get_me_items(token, client)
    assert len(data6) == 2
    item_list = [item_id1,item_id2]
    for i in data6:
        assert i["id"] in item_list
        if i["id"] in item_list: item_list.remove(i["id"])
        assert i["title"] in [ITEM1, ITEM2]
        assert i["description"] in [ITEM_DES1, ITEM_DES2]
        assert i["owner_id"] == user_id 
    assert len(item_list) == 0
       
def test_delete_user(test_db, client):
    # POST /users/
    data1 = post_users(EMAIL1, PASSWORD1, client)
    user_id = data1["id"]

    # POST /token
    data2 = post_token(EMAIL1, PASSWORD1, client)
    token = data2["access_token"]
    
    # POST /users/{user_id}/items
    data3 = post_users_userid_items(token, user_id, ITEM1, ITEM_DES1, client)
    item_id = data3["id"]
    
    # GET /users/{user_id}/delete
    data4 = post_users(EMAIL2, PASSWORD2, client)
    user_id2 = data4["id"]
    data5 = post_users(EMAIL3, PASSWORD3, client)
    user_id3 = data5["id"]
    
    destination_user = min([user_id2, user_id3])
    data6 = post_users_userid_items(token, destination_user, ITEM2, ITEM_DES2, client)
    item_id2 = data6["id"]
    
    data7 = get_users_userid_delete(token, user_id, client)
    assert data7["email"] == EMAIL1
    assert data7["id"] == user_id
    assert data7["is_active"] == False
    assert len(data7["items"]) == 0
    
    data8 = get_users_userid(token, destination_user, client)
    itemlist = [item_id, item_id2] 
    for i in data8["items"]:
        assert i["id"] in itemlist
        if i["id"] in itemlist: itemlist.remove(i["id"])
        assert i["owner_id"] == destination_user
    assert len(itemlist) == 0
    
def test_auth(test_db, client):
    # POST /users/
    data = post_users(EMAIL1, PASSWORD1, client)
    user_id = data["id"]

    # POST /token
    data = post_token(EMAIL1, PASSWORD1, client)
    token = data["access_token"]
    
    # GET /users/
    response = client.get(f"/users/")
    assert response.status_code != 200, response.text
    response = client.get(f"/users/", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    
    # GET /users/{user_id}
    response = client.get(f"/users/{user_id}")
    assert response.status_code != 200, response.text
    response = client.get(f"/users/{user_id}", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    
    # POST /users/{user_id}/items
    response = client.post(f"/users/{user_id}/items/",
        json={"title": "title1", "description": "description1"})
    assert response.status_code != 200, response.text
    response = client.post(f"/users/{user_id}/items/", headers={"X-API-TOKEN":token},
        json={"title": "title1", "description": "description1"})
    assert response.status_code == 200, response.text

    # GET /items/
    response = client.get("/items/")
    assert response.status_code != 200, response.text
    response = client.get("/items/", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    
    # GET /me/items/
    response = client.get("/me/items")
    assert response.status_code != 200, response.text
    response = client.get("/me/items", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text
    
    # GET /users/{user_id}/delete
    response = client.get(f"/users/{user_id}/delete")
    assert response.status_code != 200, response.text
    response = client.get(f"/users/{user_id}/delete", headers={"X-API-TOKEN":token})
    assert response.status_code == 200, response.text