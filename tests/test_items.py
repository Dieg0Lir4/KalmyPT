from fastapi.testclient import TestClient

# ============================================================
# Tests diseñados por Claude (Anthropic) - claude-sonnet-4-6
# Cubren CRUD, validaciones, paginación y casos límite
# ============================================================

# --- CRUD básico ---

def test_create_item(client: TestClient):
    # crea un item y verifica que se creó correctamente
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
    # verifica que el endpoint devuelve la estructura correcta
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data

def test_get_item(client: TestClient):
    # crea un item y lo busca por ID
    create = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    item_id = create.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_get_item_not_found(client: TestClient):
    # verifica que devuelve 404 si el item no existe
    response = client.get("/items/999")
    assert response.status_code == 999

def test_update_item(client: TestClient):
    # crea un item y lo actualiza
    create = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    item_id = create.json()["id"]

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
    # crea un item, lo elimina y verifica que ya no existe
    create = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    item_id = create.json()["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404

# --- Validaciones de campos inválidos ---

def test_create_item_precio_negativo(client: TestClient):
    # verifica que no se puede crear un item con precio negativo
    response = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": -100.00,
        "available": True
    })
    assert response.status_code == 422

def test_create_item_nombre_vacio(client: TestClient):
    # verifica que no se puede crear un item con nombre vacío
    response = client.post("/items/", json={
        "name": "",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    assert response.status_code == 422

def test_create_item_sin_nombre(client: TestClient):
    # verifica que el nombre es obligatorio
    response = client.post("/items/", json={
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    assert response.status_code == 422

def test_create_item_sin_precio(client: TestClient):
    # verifica que el precio es obligatorio
    response = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "available": True
    })
    assert response.status_code == 422

def test_create_item_precio_cero(client: TestClient):
    # verifica que el precio no puede ser cero
    response = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 0,
        "available": True
    })
    assert response.status_code == 422

def test_create_item_precio_string(client: TestClient):
    # verifica que el precio no puede ser un string
    response = client.post("/items/", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": "hola",
        "available": True
    })
    assert response.status_code == 422

def test_update_item_no_existe(client: TestClient):
    # verifica que devuelve 404 al actualizar un item que no existe
    response = client.put("/items/999", json={
        "name": "Laptop",
        "description": "Laptop gamer",
        "price": 1500.00,
        "available": True
    })
    assert response.status_code == 404

def test_delete_item_no_existe(client: TestClient):
    # verifica que devuelve 404 al eliminar un item que no existe
    response = client.delete("/items/999")
    assert response.status_code == 404

# --- Paginación ---

def test_paginacion_default(client: TestClient):
    # verifica que la paginación por defecto es page=1 y size=10
    for i in range(3):
        client.post("/items/", json={
            "name": f"Item {i}",
            "description": f"Descripcion {i}",
            "price": 100.00,
            "available": True
        })
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 10
    assert data["total"] == 3
    assert len(data["items"]) == 3

def test_paginacion_segunda_pagina(client: TestClient):
    # verifica que la segunda página devuelve los items correctos
    for i in range(15):
        client.post("/items/", json={
            "name": f"Item {i}",
            "description": f"Descripcion {i}",
            "price": 100.00,
            "available": True
        })
    response = client.get("/items/?page=2&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["total"] == 15
    assert len(data["items"]) == 5

def test_paginacion_size_personalizado(client: TestClient):
    # verifica que el size personalizado funciona correctamente
    for i in range(10):
        client.post("/items/", json={
            "name": f"Item {i}",
            "description": f"Descripcion {i}",
            "price": 100.00,
            "available": True
        })
    response = client.get("/items/?page=1&size=5")
    data = response.json()
    assert len(data["items"]) == 5
    assert data["size"] == 5

# --- Casos límite ---

def test_page_cero(client: TestClient):
    # verifica que page=0 no es válido
    response = client.get("/items/?page=0")
    assert response.status_code == 422

def test_size_cero(client: TestClient):
    # verifica que size=0 no es válido
    response = client.get("/items/?size=0")
    assert response.status_code == 422

def test_size_mayor_limite(client: TestClient):
    # verifica que size mayor a 100 no es válido
    response = client.get("/items/?size=101")
    assert response.status_code == 422

def test_nombre_muy_largo(client: TestClient):
    # verifica que el nombre no puede tener más de 100 caracteres
    response = client.post("/items/", json={
        "name": "a" * 101,
        "description": "Descripcion",
        "price": 100.00,
        "available": True
    })
    assert response.status_code == 422

def test_descripcion_muy_larga(client: TestClient):
    # verifica que la descripción no puede tener más de 500 caracteres
    response = client.post("/items/", json={
        "name": "Laptop",
        "description": "a" * 501,
        "price": 100.00,
        "available": True
    })
    assert response.status_code == 422

def test_lista_vacia(client: TestClient):
    # verifica que una DB vacía devuelve una lista vacía
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []