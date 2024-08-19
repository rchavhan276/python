from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class CategorySystemModel(BaseModel):
    id: UUID
    category_id: UUID
    system_id: UUID
    created_at: datetime
    updated_at: datetime


class AddCategorySystemModel(BaseModel):
    category_id: UUID = Field(alias = "categoryId")
    system_id: UUID = Field(alias = "systemId")
   
    
    
   
    
