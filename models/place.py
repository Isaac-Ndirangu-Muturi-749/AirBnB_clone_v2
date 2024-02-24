#!/usr/bin/python3
"""This module defines the Place class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """This class represents a place in the application."""

    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    user = relationship("User", back_populates="places")
    city = relationship("City", back_populates="places")
    reviews = relationship("Review", cascade="all, delete", back_populates="place")
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new Place instance."""
        super().__init__(*args, **kwargs)


from models.base_model import BaseModel
from models.amenity import Amenity


class Place(BaseModel):
    """This class represents a place in the application."""

    def __init__(self, *args, **kwargs):
        """Initialize a new Place instance."""
        super().__init__(*args, **kwargs)
        self.amenity_ids = []

    @property
    def amenities(self):
        """Getter attribute to return the list of Amenity instances."""
        from models import storage
        amenities_list = []
        for amenity_id in self.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities_list.append(amenity)
        return amenities_list

    @amenities.setter
    def amenities(self, amenity_obj):
        """Setter attribute to handle appending Amenity ids."""
        if isinstance(amenity_obj, Amenity):
            self.amenity_ids.append(amenity_obj.id)
