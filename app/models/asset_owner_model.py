from sqlalchemy import Column, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .client_model import Client


Base = declarative_base()

class AssetOwner(Base):
    __tablename__ = 'asset_owners'

    id = Column(UUID , primary_key=True)
    client_id = Column(UUID, ForeignKey(Client.id))
    employee_code = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    department = Column(String)
    email = Column(String)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')  
    