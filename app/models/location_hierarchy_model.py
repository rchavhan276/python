from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .location_model import Location


Base = declarative_base()

class LocationHierarchy(Base):
    __tablename__ = 'location_hierarchy'

    id = Column(UUID , primary_key=True)
    parent_location_id = Column(UUID, ForeignKey(Location.id))
    child_location_id = Column(UUID, ForeignKey(Location.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')