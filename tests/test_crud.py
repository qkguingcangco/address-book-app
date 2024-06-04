import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import crud, models, schemas
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    # Drop all tables
    Base.metadata.drop_all(bind=engine)

def test_create_address(db):
    address_in = schemas.AddressCreate(name="Test Address", latitude=10.0, longitude=20.0)
    address = crud.create_address(db=db, address=address_in)
    assert address.name == "Test Address"
    assert address.latitude == 10.0
    assert address.longitude == 20.0

def test_get_address(db):
    address_in = schemas.AddressCreate(name="Test Address", latitude=10.0, longitude=20.0)
    address = crud.create_address(db=db, address=address_in)
    fetched_address = crud.get_address(db=db, address_id=address.id)
    assert fetched_address
    assert fetched_address.name == "Test Address"

def test_delete_address(db):
    address_in = schemas.AddressCreate(name="Test Address", latitude=10.0, longitude=20.0)
    address = crud.create_address(db=db, address=address_in)
    crud.delete_address(db=db, address_id=address.id)
    deleted_address = crud.get_address(db=db, address_id=address.id)
    assert deleted_address is None

def test_update_address(db):
    # Create an address
    address_in = schemas.AddressCreate(name="Test Address", latitude=10.0, longitude=20.0)
    address = crud.create_address(db=db, address=address_in)
    
    # Update the address
    address_update = schemas.AddressCreate(name="Updated Address", latitude=15.0, longitude=25.0)
    updated_address = crud.update_address(db=db, address_id=address.id, address=address_update)
    
    # Verify the update
    assert updated_address.name == "Updated Address"
    assert updated_address.latitude == 15.0
    assert updated_address.longitude == 25.0
    
    # Fetch the updated address and verify
    fetched_address = crud.get_address(db=db, address_id=address.id)
    assert fetched_address
    assert fetched_address.name == "Updated Address"
    assert fetched_address.latitude == 15.0
    assert fetched_address.longitude == 25.0
