from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from .database import Base

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    __table_args__ = (UniqueConstraint('name', 'latitude', 'longitude', name='_address_uc'),)
