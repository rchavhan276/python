from sqlalchemy import Column, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from .region_model import Region
from .country_model import Country


Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(UUID , primary_key=True)
    region_id = Column(UUID, ForeignKey(Region.id))
    country_id = Column(UUID, ForeignKey(Country.id))
    client_code = Column(String)
    client_name = Column(String)
    client_address = Column(JSONB)
    client_contact = Column(JSONB)
    description = Column(String)
    crm_reference = Column(String)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')