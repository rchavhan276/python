from sqlalchemy import Column, String, Boolean, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import UserDefinedType
from sqlalchemy.ext.declarative import declarative_base
from .client_model import Client


Base = declarative_base()

class POINT(UserDefinedType):
    def get_col_spec(self):
        return "POINT"

class Location(Base):
    __tablename__ = 'locations'

    id = Column(UUID , primary_key=True)
    client_id = Column(UUID, ForeignKey(Client.id))
    location_code = Column(String)
    location_name = Column(String)
    location_type = Column(String)
    is_outdoor = Column(Boolean)
    is_hazloc = Column(Boolean)
    hazloc_spec = Column(JSONB)
    description = Column(String)
    geo_coordinates = Column(POINT)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')  
