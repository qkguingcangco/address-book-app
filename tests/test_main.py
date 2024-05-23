import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.routers import address
from app.database import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[address.get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    # Setup: clean the database before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: clean the database after each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_address():
    response = client.post(
        "/addresses/",
        json={"name": "Test Address 1", "latitude": 10.0, "longitude": 20.0}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Address 1"
    assert response.json()["latitude"] == 10.0
    assert response.json()["longitude"] == 20.0

def test_read_addresses_within_distance():
    # Create some test addresses
    client.post("/addresses/", json={"name": "Test Address 1", "latitude": 10.0, "longitude": 20.0})
    client.post("/addresses/", json={"name": "Test Address 2", "latitude": 10.05, "longitude": 20.05})  # Adjusted coordinates
    client.post("/addresses/", json={"name": "Test Address 3", "latitude": 11.0, "longitude": 21.0})

    # Fetch addresses within 15 km of (10.0, 20.0)
    response = client.get("/addresses/within_distance/?latitude=10.0&longitude=20.0&distance_km=15")
    assert response.status_code == 200
    addresses = response.json()
    assert len(addresses) == 2  # Test Address 1 and Test Address 2 should be within 15 km
    names = [address["name"] for address in addresses]
    assert "Test Address 1" in names
    assert "Test Address 2" in names
    assert "Test Address 3" not in names

def test_read_addresses_within_short_distance():
    # Create some test addresses
    client.post("/addresses/", json={"name": "Test Address 1", "latitude": 10.0, "longitude": 20.0})
    client.post("/addresses/", json={"name": "Test Address 2", "latitude": 10.05, "longitude": 20.05})
    client.post("/addresses/", json={"name": "Test Address 3", "latitude": 11.0, "longitude": 21.0})

    # Fetch addresses within 5 km of (10.0, 20.0)
    response = client.get("/addresses/within_distance/?latitude=10.0&longitude=20.0&distance_km=5")
    assert response.status_code == 200
    addresses = response.json()
    assert len(addresses) == 1  # Only Test Address 1 should be within 5 km
    assert addresses[0]["name"] == "Test Address 1"

def test_delete_address():
    # Create an address to delete
    response = client.post(
        "/addresses/",
        json={"name": "Test Address to Delete", "latitude": 10.0, "longitude": 20.0}
    )
    address_id = response.json()["id"]

    # Delete the created address
    response = client.delete(f"/addresses/{address_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Address to Delete"

    # Try to read the deleted address
    response = client.get(f"/addresses/{address_id}")
    assert response.status_code == 404
