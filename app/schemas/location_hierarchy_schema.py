from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class LocationHierarchyModel(BaseModel):
    id: UUID
    parent_location_id: UUID
    child_location_id: UUID
    created_at: datetime
    updated_at: datetime


class AddLocationHierarchyModel(BaseModel):
    parent_location_id: UUID = Field(alias = "parentLocationId")
    child_location_id: UUID = Field(alias = "childLocationId")
   
    
    
   
    
