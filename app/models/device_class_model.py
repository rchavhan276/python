from sqlalchemy import Column, String, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class DeviceClass(Base):
    __tablename__ = 'asset_device_classes'

    id = Column(UUID , primary_key=True)
    asset_device_class_name = Column(String)
    description = Column(String)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')  