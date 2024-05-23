from sqlalchemy.orm import Session
from geopy.distance import geodesic
from . import models, schemas
import logging

logger = logging.getLogger(__name__)

def get_address(db: Session, address_id: int):
    try:
        logger.debug(f"Fetching address with ID: {address_id}")
        address = db.query(models.Address).filter(models.Address.id == address_id).first()
        if address:
            logger.info(f"Address found: {address}")
        else:
            logger.warning(f"No address found with ID: {address_id}")
        return address
    except Exception as e:
        logger.error("Error in get_address: %s", str(e))
        raise

def get_addresses(db: Session, page: int = 1, page_size: int = 10):
    try:
        offset = (page - 1) * page_size
        logger.debug(f"Fetching addresses for page: {page}, page size: {page_size}, offset: {offset}")
        addresses = db.query(models.Address).offset(offset).limit(page_size).all()
        logger.info(f"{len(addresses)} addresses found on page {page}")
        return addresses
    except Exception as e:
        logger.error("Error in get_addresses: %s", str(e))
        raise

def create_address(db: Session, address: schemas.AddressCreate):
    try:
        logger.debug(f"Creating new address with data: {address}")
        db_address = models.Address(**address.model_dump())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        logger.info(f"New address created: {db_address}")
        return db_address
    except Exception as e:
        logger.error("Error in create_address: %s", str(e))
        db.rollback()  # rollback in case of error
        raise

def delete_address(db: Session, address_id: int):
    try:
        logger.debug(f"Deleting address with ID: {address_id}")
        db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
        if db_address:
            db.delete(db_address)
            db.commit()
            logger.info(f"Address deleted: {db_address}")
        else:
            logger.warning(f"No address found to delete with ID: {address_id}")
        return db_address
    except Exception as e:
        logger.error("Error in delete_address: %s", str(e))
        db.rollback()  # rollback in case of error
        raise

def get_addresses_within_distance(db: Session, latitude: float, longitude: float, distance_km: float):
    try:
        logger.debug(f"Fetching addresses within {distance_km} km of ({latitude}, {longitude})")
        addresses = db.query(models.Address).all()
        nearby_addresses = []
        for address in addresses:
            address_coords = (address.latitude, address.longitude)
            distance = geodesic((latitude, longitude), address_coords).km
            logger.debug(f"Distance to ({address.latitude}, {address.longitude}) is {distance} km")
            if distance <= distance_km:
                nearby_addresses.append(address)
        logger.info(f"{len(nearby_addresses)} addresses found within {distance_km} km of ({latitude}, {longitude})")
        return nearby_addresses
    except Exception as e:
        logger.error("Error in get_addresses_within_distance: %s", str(e))
        raise
