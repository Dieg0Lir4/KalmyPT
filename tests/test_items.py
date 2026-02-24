from fastapi.testclient import TestClient

def test_create_item(client: TestClient):
    response = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1500.00
    assert "id" in data

def test_get_items(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data

def test_get_item(client: TestClient):
    # primero creamos un item
    create = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    item_id = create.json()["id"]

    # luego lo buscamos
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_get_item_not_found(client: TestClient):
    response = client.get("/items/999")
    assert response.status_code == 404

def test_update_item(client: TestClient):
    # primero creamos un item
    create = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    item_id = create.json()["id"]

    # luego lo actualizamos
    response = client.put(f"/items/{item_id}", json={
        "name": "Laptop actualizado",
        "description": "Laptop gamer actualizado",
        "price": 2000.00,
        "available": False
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop actualizado"
    assert response.json()["price"] == 2000.00

def test_delete_item(client: TestClient):
    # primero creamos un item
    create = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    item_id = create.json()["id"]

    # luego lo eliminamos
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    # verificamos que ya no existe
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404