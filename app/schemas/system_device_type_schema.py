from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class SystemDeviceTypeModel(BaseModel):
    id: UUID
    system_id: UUID
    device_type_id: UUID
    created_at: datetime
    updated_at: datetime


class AddSystemDeviceTypeModel(BaseModel):
    system_id: UUID = Field(alias = "systemId")
    device_type_id: UUID = Field(alias = "deviceTypeId")
 