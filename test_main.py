from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock
import pytest

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
    assert response.json()["message"] == "Label not found"


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
    response = client.delete("/label/77")
    # Assuming label with ID 12 exists for this test
    assert response.status_code == 200


def test_delete_label_not_found():
    response = client.delete("/label/1")
    # Assuming label with ID 1 does not exist for this test
    assert response.status_code == 404


@patch("controllers.label_controller.get_connection")
def test_get_labels_database_error(mock_get_connection):
    mock_get_connection.side_effect = Exception("Database connection failed")
    response = client.get("/labels/")
    assert response.status_code == 500
    assert response.json()["message"] == "An error occurred"


@patch("controllers.label_controller.get_connection")
def test_get_label_by_id_database_error(mock_get_connection):
    mock_get_connection.side_effect = Exception("Database connection failed")
    response = client.get("/label/2")
    assert response.status_code == 500
    assert response.json()["message"] == "An error occurred"


@patch("controllers.label_controller.get_connection")
def test_create_label_insert_error(mock_get_connection):
    mock_conn = AsyncMock()
    mock_conn.execute.return_value = None
    mock_conn.fetchval.side_effect = Exception("Insert failed")
    mock_get_connection.return_value = mock_conn
    label_data = {
        "name_prod": "Test Product",
        "lot_format": "LOT-123",
        "lot_detail": "Test Lot Detail",
        "expiration_format": "2025-12-31",
        "expiration_detail": "Test Expiration Detail"
    }
    response = client.post("/label/", json=label_data)
    assert response.status_code == 500
    assert response.json()["message"] == \
        "An error occurred while creating the label"


@patch("controllers.label_controller.get_connection")
def test_create_label_database_error(mock_get_connection):
    mock_get_connection.side_effect = Exception("Database connection failed")
    label_data = {
        "name_prod": "Test Product",
        "lot_format": "LOT-123",
        "lot_detail": "Test Lot Detail",
        "expiration_format": "2025-12-31",
        "expiration_detail": "Test Expiration Detail"
    }
    response = client.post("/label/", json=label_data)
    assert response.status_code == 500
    assert response.json()["message"] == \
        "An error occurred while creating the label"


@patch("controllers.label_controller.get_connection")
def test_update_label_update_error(mock_get_connection):
    mock_conn = AsyncMock()
    mock_conn.fetchval.return_value = 2

    def execute_side_effect(query, *args):
        if "UPDATE" in query:
            raise Exception("Update failed")
        return None

    mock_conn.execute.side_effect = execute_side_effect
    mock_get_connection.return_value = mock_conn
    label_data = {
        "name_prod": "Updated Product",
        "lot_format": "LOT-456",
        "lot_detail": "Updated Lot Detail",
        "expiration_format": "2026-12-31",
        "expiration_detail": "Updated Expiration Detail"
    }
    response = client.put("/label/2", json=label_data)
    assert response.status_code == 500
    assert response.json()["message"] == \
        "An error occurred while updating the label"


@patch("controllers.label_controller.get_connection")
def test_update_label_database_error(mock_get_connection):
    mock_get_connection.side_effect = Exception("Database connection failed")
    label_data = {
        "name_prod": "Updated Product",
        "lot_format": "LOT-456",
        "lot_detail": "Updated Lot Detail",
        "expiration_format": "2026-12-31",
        "expiration_detail": "Updated Expiration Detail"
    }
    response = client.put("/label/2", json=label_data)
    assert response.status_code == 500
    assert response.json()["message"] == \
        "An error occurred while updating the label"


@patch("controllers.label_controller.get_connection")
def test_delete_label_delete_error(mock_get_connection):
    mock_conn = AsyncMock()
    mock_conn.fetchval.return_value = 2

    def execute_side_effect(query, *args):
        if "DELETE" in query:
            raise Exception("Delete failed")
        return None

    mock_conn.execute.side_effect = execute_side_effect
    mock_get_connection.return_value = mock_conn
    response = client.delete("/label/2")
    assert response.status_code == 500
    assert response.json()["message"] == \
        "An error occurred while deleting the label"


@patch("controllers.label_controller.get_connection")
def test_delete_label_database_error(mock_get_connection):
    mock_get_connection.side_effect = Exception("Database connection failed")
    response = client.delete("/label/2")
    assert response.status_code == 500
    assert response.json()["message"] == \
        "An error occurred while deleting the label"


if __name__ == "__main__":
    pytest.main(["-v"])
