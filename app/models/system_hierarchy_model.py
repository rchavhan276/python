from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .system_model import System


Base = declarative_base()

class SystemHierarchy(Base):
    __tablename__ = 'system_hierarchy'

    id = Column(UUID , primary_key=True)
    parent_system_id = Column(UUID, ForeignKey(System.id))
    child_system_id = Column(UUID, ForeignKey(System.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')