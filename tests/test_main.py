from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_address():
    response = client.post(
        "/addresses/",
        json={"name": "Test Address", "latitude": 10.0, "longitude": 20.0}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Address"

def test_read_address():
    # Create an address to read
    response = client.post(
        "/addresses/",
        json={"name": "Test Address", "latitude": 10.0, "longitude": 20.0}
    )
    address_id = response.json()["id"]
    
    # Read the created address
    response = client.get(f"/addresses/{address_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Address"

def test_delete_address():
    # Create an address to delete
    response = client.post(
        "/addresses/",
        json={"name": "Test Address", "latitude": 10.0, "longitude": 20.0}
    )
    address_id = response.json()["id"]
    
    # Delete the created address
    response = client.delete(f"/addresses/{address_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Address"
    
    # Try to read the deleted address
    response = client.get(f"/addresses/{address_id}")
    assert response.status_code == 404
