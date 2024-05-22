from sqlalchemy.orm import Session
from . import models, schemas

def get_address(db: Session, address_id: int):
    # fetch address by ID (get first result)
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 10):
    # fetch all addresses + pagination
    return db.query(models.Address).offset(skip).limit(limit).all()

def create_address(db: Session, address: schemas.AddressCreate):
    # create new address
    db_address = models.Address(**address.model_dump()) # dict() is deprecated
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    # delete address by ID
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address
