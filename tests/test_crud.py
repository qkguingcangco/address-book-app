from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import crud, models, schemas
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def test_create_address():
    db = TestingSessionLocal()
    address_in = schemas.AddressCreate(name="Test Address", latitude=10.0, longitude=20.0)
    address = crud.create_address(db=db, address=address_in)
    assert address.name == "Test Address"
    assert address.latitude == 10.0
    assert address.longitude == 20.0
    db.close()

def test_get_address():
    db = TestingSessionLocal()
    address_in = schemas.AddressCreate(name="Test Address", latitude=10.0, longitude=20.0)
    address = crud.create_address(db=db, address=address_in)
    fetched_address = crud.get_address(db=db, address_id=address.id)
    assert fetched_address
    assert fetched_address.name == "Test Address"
    db.close()

def test_delete_address():
    db = TestingSessionLocal()
    address_in = schemas.AddressCreate(name="Test Address", latitude=10.0, longitude=20.0)
    address = crud.create_address(db=db, address=address_in)
    crud.delete_address(db=db, address_id=address.id)
    deleted_address = crud.get_address(db=db, address_id=address.id)
    assert deleted_address is None
    db.close()
