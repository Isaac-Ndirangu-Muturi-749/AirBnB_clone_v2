#!/usr/bin/python3
"""This module defines the City class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.state import State

import os
storage_engine = os.environ.get("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    """A class for representing City objects"""
    if (storage_engine == "db"):
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey(State.id), nullable=False)
        places = relationship("Place", cascade="all, delete", back_populates="city")
    else:
        name = ""
        state_id = ""
