from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .device_class_model import DeviceClass


Base = declarative_base()

class DeviceClassHierarchy(Base):
    __tablename__ = 'device_class_hierarchy'

    id = Column(UUID , primary_key=True)
    parent_device_class_id = Column(UUID, ForeignKey(DeviceClass.id))
    child_device_class_id = Column(UUID, ForeignKey(DeviceClass.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')