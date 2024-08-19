from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class SystemHierarchyModel(BaseModel):
    id: UUID
    parent_system_id: UUID
    child_system_id: UUID
    created_at: datetime
    updated_at: datetime


class AddSystemHierarchyModel(BaseModel):
    parent_system_id: UUID = Field(alias = "parentSystemId")
    child_system_id: UUID = Field(alias = "childSystemId")
   
    
    
   
    
