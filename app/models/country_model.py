from sqlalchemy import Column, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from .region_model import Region


Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'

    id = Column(UUID , primary_key=True)
    region_id = Column(UUID, ForeignKey(Region.id))
    country_name = Column(String)
    country_code = Column(String)
    description = Column(String)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')