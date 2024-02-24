#!/usr/bin/python3
"""This module defines the Amenity class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import os
storage_engine = os.environ.get("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base):
    """This class represents an amenity in the application."""
    if (storage_engine == "db"):
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            "PlaceAmenity", back_populates="amenity")
        place_amenities = relationship(
            "Place",
            secondary=place_amenity, back_populates="amenities")
    else:
        name = ""
