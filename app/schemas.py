from pydantic import BaseModel, ConfigDict

class AddressBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True) # Enable ORM mode (orm_mode is deprecated)
