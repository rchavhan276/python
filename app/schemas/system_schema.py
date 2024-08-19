from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import split_str_validator

class SystemModel(BaseModel):
    id: UUID
    system_name: str
    description: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddSystemModel(BaseModel):
    system_name: str = Field(alias = "systemName")
    description: Optional[str] = Field(default=None, alias = "description")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")
    
    _convert_user_tags = split_str_validator('user_tags')
    
