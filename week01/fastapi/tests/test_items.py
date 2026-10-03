import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import ItemService
from app.dependencies import get_item_service
from  app.models import ItemCreate

client = TestClient(app)

@pytest.fixture()
def service():
    service =  ItemService()

    app.dependency_overrides[get_item_service] = lambda: service

    yield service

    app.dependency_overrides.clear()


def test_create_item(service):
    response = client.post(
        "/items/",
        json={
            "name": "Keyboard",
            "price": 999,
            "in_stock": True
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Keyboard"
    assert data["price"] == 999
    assert data["in_stock"] is True
    assert data["id"] == 1


def test_get_item(service):
    service.create(
        ItemCreate(
            name = "Keyboard",
            price = 999,
            in_stock = True
        )
    )

    response= client.get("/items/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Keyboard"
    assert data["price"] == 999
    assert data["in_stock"] == True

def test_update_item(service):
    service.create(
        ItemCreate(
            name = "Keyboard",
            price = 999,
            in_stock = True
        )
    )

    response = client.put(
        "items/1",
        json={
            "name": "Mechanical Keyboard",
            "price": 1499,
            "in_stock": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 1499
    assert data["in_stock"] is True

def test_delete_item(service):
    service.create(
        ItemCreate(
            name = "Keyboard",
            price = 999,
            in_stock = True
        )
    )
    response = client.delete(
        "/items/1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Item deleted successfully"


def test_get_missing_item(service):
    response = client.get("/items/999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Item 999 not found"


