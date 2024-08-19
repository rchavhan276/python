from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class DeviceClassHierarchyModel(BaseModel):
    id: UUID
    parent_device_class_id: UUID
    child_device_class_id: UUID
    created_at: datetime
    updated_at: datetime


class AddDeviceClassHierarchyModel(BaseModel):
    parent_device_class_id: UUID = Field(alias = "parentDeviceClassId")
    child_device_class_id: UUID = Field(alias = "childDeviceClassId")
   
    
    
   
    
