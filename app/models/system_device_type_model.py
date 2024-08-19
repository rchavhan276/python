from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .system_model import System
from .device_type_model import DeviceType


Base = declarative_base()

class SystemDeviceType(Base):
    __tablename__ = 'systems_device_types'
    
    id = Column(UUID , primary_key=True)
    system_id = Column(UUID, ForeignKey(System.id))
    device_type_id = Column(UUID, ForeignKey(DeviceType.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')  