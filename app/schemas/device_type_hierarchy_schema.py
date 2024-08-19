from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class DeviceTypeHierarchyModel(BaseModel):
    id: UUID
    parent_device_type_id: UUID
    child_device_type_id: UUID
    created_at: datetime
    updated_at: datetime


class AddDeviceTypeHierarchyModel(BaseModel):
    parent_device_type_id: UUID = Field(alias = "parentDeviceTypeId")
    child_device_type_id: UUID = Field(alias = "childDeviceTypeId")
   
    
    
   
    
