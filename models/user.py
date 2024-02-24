#!/usr/bin/python3
"""This module defines the User class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import os
storage_engine = os.environ.get("HBNB_TYPE_STORAGE")


class User(BaseModel, Base):
    """This class represents a user in the application."""
    if (storage_engine == 'db'):
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship(
            "Place",
            cascade="all, delete",
            back_populates="user")
        reviews = relationship(
            "Review",
            cascade="all, delete",
            back_populates="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
