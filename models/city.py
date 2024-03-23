#!/usr/bin/python3
"""This module defines the City class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.place import Place


class City(BaseModel, Base):
    """A class for representing City objects"""
    if (storage_engine == "db"):
        __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60),
                      ForeignKey("states.id", ondelete='CASCADE'),
                      nullable=False)

    places = relationship('Place',
                          backref='cities',
                          cascade='all, delete-orphan')

    else:
        name = ""
        state_id = ""
