from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """This class represents an amenity in the application."""

    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    place_amenities = relationship("PlaceAmenity", back_populates="amenity")

    def __init__(self, *args, **kwargs):
        """Initialize a new Amenity instance."""
        super().__init__(*args, **kwargs)
