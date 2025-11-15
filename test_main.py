from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200


def test_get_labels():
    response = client.get("/labels/")
    assert response.status_code == 200


def test_get_label():
    response = client.get("/label/2")
    # Assuming label with ID 2 exists for this test
    assert response.status_code == 200


def test_get_label_not_found():
    response = client.get("/label/1")
    # Assuming label with ID 1 does not exist for this test
    assert response.status_code == 404


def test_post_label():
    label_data = {
        "name_prod": "Test Product",
        "lot_format": "LOT-123",
        "lot_detail": "Test Lot Detail",
        "expiration_format": "2025-12-31",
        "expiration_detail": "Test Expiration Detail"
    }
    response = client.post("/label/", json=label_data)
    assert response.status_code == 201


def test_put_label():
    label_data = {
        "name_prod": "Updated Product",
        "lot_format": "LOT-456",
        "lot_detail": "Updated Lot Detail",
        "expiration_format": "2026-12-31",
        "expiration_detail": "Updated Expiration Detail"
    }
    response = client.put("/label/47", json=label_data)
    # Assuming label with ID 47 exists for this test
    assert response.status_code == 200


def test_put_label_not_found():
    label_data = {
        "name_prod": "Nonexistent Product",
        "lot_format": "LOT-000",
        "lot_detail": "Nonexistent Lot Detail",
        "expiration_format": "2024-01-01",
        "expiration_detail": "Nonexistent Expiration Detail"
    }
    response = client.put("/label/1", json=label_data)
    # Assuming label with ID 1 does not exist for this test
    assert response.status_code == 404


def test_delete_label():
    response = client.delete("/label/55")
    # Assuming label with ID 12 exists for this test
    assert response.status_code == 200


def test_delete_label_not_found():
    response = client.delete("/label/1")
    # Assuming label with ID 1 does not exist for this test
    assert response.status_code == 404
