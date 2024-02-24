#!/usr/bin/python3
"""This module defines the Place class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity

import os
storage_engine = os.environ.get("HBNB_TYPE_STORAGE")

place_amenity = Table(
    name='place_amenity',
    metadata=Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
    )


class Place(BaseModel, Base):
    """This class represents a place in the application."""
    if (storage_engine == "db"):
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
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Getter function for reviews attribute"""
            # Get the Review class from the dummy_classes dictionary
            review_cls = models.dummy_classes['Review']
            # Get all reviews from the database session for the Review class
            all_reviews = models.storage.all(review_cls).values()
            # Filter reviews based on the place_id matching self.id
            matching_reviews = [review for review in all_reviews if review.place_id == self.id]
            return matching_reviews

        @property
        def amenities(self):
            """Getter attribute to return the list of Amenity instances."""
            # Initialize an empty list to store Amenity instances
            amenity_instances = []
            # Get the Amenity class from the dummy_classes dictionary
            amenity_class = models.dummy_classes['Amenity']
            # Iterate over all Amenity instances in the storage
            for amenity_instance in models.storage.all(amenity_class).values():
                # Check if the Amenity instance's ID is in self.amenity_ids
                if amenity_instance.id in self.amenity_ids:
                    # If so, append the Amenity instance to the result list
                    amenity_instances.append(amenity_instance)
            # Return the list of Amenity instances
            return amenity_instances


        @amenities.setter
        def amenities(self, amenity_instance):
            """Setter method for amenities."""
            # Get the Amenity class from the dummy_classes dictionary
            amenity_class = models.dummy_classes['Amenity']
            # Check if the input object is an instance of Amenity
            if isinstance(amenity_instance, amenity_class):
                # If so, append the Amenity instance's ID to amenity_ids
                self.amenity_ids.append(amenity_instance.id)
