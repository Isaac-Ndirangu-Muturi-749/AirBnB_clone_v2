#!/usr/bin/python3
"""This module defines the State class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import os
storage_engine = os.environ.get("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """A class for representing State objects"""
    if storage_engine == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete", backref="state")
    else:
        name = ""

        @property
        def cities(self):
            """Getter attribute that returns the list of City instances"""
            all_cities = models.storage.all(City)
            return [city for city in all_cities.values()
                    if city.state_id == self.id]
