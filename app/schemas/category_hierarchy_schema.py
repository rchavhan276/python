from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class CategoryHierarchyModel(BaseModel):
    id: UUID
    parent_category_id: UUID
    child_category_id: UUID
    created_at: datetime
    updated_at: datetime


class AddCategoryHierarchyModel(BaseModel):
    parent_category_id: UUID = Field(alias = "parentCategoryId")
    child_category_id: UUID = Field(alias = "childCategoryId")
   
    
    
   
    
