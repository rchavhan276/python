from sqlalchemy import Column, String, Boolean, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import UserDefinedType
from sqlalchemy.ext.declarative import declarative_base
from .client_model import Client
from .project_model import Project
from .location_model import Location
from .category_model import Category
from .system_model import System
from .device_type_model import DeviceType

Base = declarative_base()

class POINT(UserDefinedType):
    def get_col_spec(self):
        return "POINT"
    
class Asset(Base):
    __tablename__ = 'assets'
    
    id = Column(UUID , primary_key=True)
    client_id = Column(UUID, ForeignKey(Client.id))
    project_id = Column(UUID, ForeignKey(Project.id))
    location_id = Column(UUID, ForeignKey(Location.id))
    category_id = Column(UUID, ForeignKey(Category.id))
    system_id = Column(UUID, ForeignKey(System.id))
    device_type_id = Column(UUID, ForeignKey(DeviceType.id))
    asset_tag = Column(String)
    description = Column(String)
    is_active = Column(Boolean)
    geo_coordinates = Column(POINT)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')    