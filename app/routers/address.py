from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import logging
from typing import List, Dict, Any
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
from .. import crud, models, schemas
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)  # Create the tables

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating address with data: {address}")
        db_address = crud.create_address(db=db, address=address)
        return schemas.Address.model_validate(db_address)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error creating address: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching address with ID: {address_id}")
        db_address = crud.get_address(db, address_id=address_id)
        if db_address is None:
            logger.warning(f"Address with ID {address_id} not found")
            raise HTTPException(status_code=404, detail="Address not found")
        return schemas.Address.model_validate(db_address)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error reading address: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting address with ID: {address_id}")
        db_address = crud.delete_address(db, address_id=address_id)
        if db_address is None:
            logger.warning(f"Address with ID {address_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Address not found")
        return schemas.Address.model_validate(db_address)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error deleting address: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=Dict[str, Any])
def read_addresses(request: Request, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching addresses for page {page} with page size {page_size}")
        addresses = crud.get_addresses(db, page=page, page_size=page_size)
        total_addresses = db.query(models.Address).count()
        current_page = page

        parsed_url = urlparse(request.url)
        query_params = dict(parse_qsl(parsed_url.query))
        
        previous_page = None if page <= 1 else urlunparse(parsed_url._replace(query=urlencode({**query_params, "page": page - 1})))
        next_page = None if (page * page_size) >= total_addresses else urlunparse(parsed_url._replace(query=urlencode({**query_params, "page": page + 1})))

        response = {
            "current_page": current_page,
            "previous_page": previous_page,
            "next_page": next_page,
            "addresses": [schemas.Address.model_validate(address) for address in addresses]
        }
        logger.info(f"Returning {len(addresses)} addresses on page {page}")
        return response
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error reading addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/within_distance/", response_model=List[schemas.Address])
def read_addresses_within_distance(latitude: float, longitude: float, distance_km: float, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching addresses within {distance_km} km of ({latitude}, {longitude})")
        addresses = crud.get_addresses_within_distance(db, latitude, longitude, distance_km)
        return [schemas.Address.model_validate(address) for address in addresses]
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error reading addresses within distance: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
