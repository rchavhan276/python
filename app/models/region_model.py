from sqlalchemy import Column, String, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Region(Base):
    __tablename__ = 'regions'

    id = Column(UUID , primary_key=True)
    region_name = Column(String)
    region_code = Column(String)
    description = Column(String)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')