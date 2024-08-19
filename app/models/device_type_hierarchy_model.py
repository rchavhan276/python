from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .device_type_model import DeviceType


Base = declarative_base()

class DeviceTypeHierarchy(Base):
    __tablename__ = 'device_type_hierarchy'

    id = Column(UUID , primary_key=True)
    parent_device_type_id = Column(UUID, ForeignKey(DeviceType.id))
    child_device_type_id = Column(UUID, ForeignKey(DeviceType.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')