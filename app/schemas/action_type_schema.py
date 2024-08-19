from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import split_str_validator

class ActionTypeModel(BaseModel):
    id: UUID
    action_type: str
    description: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddActionTypeModel(BaseModel):
    action_type: str = Field(alias = "actionType")
    description: Optional[str] = Field(default=None, alias = "description")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")
    
    
    _convert_user_tags = split_str_validator('user_tags')
    
