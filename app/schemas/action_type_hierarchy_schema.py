from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class ActionTypeHierarchyModel(BaseModel):
    id: UUID
    parent_action_type_id: UUID
    child_action_type_id: UUID
    created_at: datetime
    updated_at: datetime


class AddActionTypeHierarchyModel(BaseModel):
    parent_action_type_id: UUID = Field(alias = "parentActionTypeId")
    child_action_type_id: UUID = Field(alias = "childActionTypeId")
   
    
    
   
    
