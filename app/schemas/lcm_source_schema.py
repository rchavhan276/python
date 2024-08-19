from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import split_str_validator

class LcmSourceModel(BaseModel):
    id: UUID
    namespace: str
    module_name: str
    description: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddLcmSourceModel(BaseModel):
    namespace: str = Field(alias = "namespace")
    module_name: str = Field(alias = "moduleName")
    description: Optional[str] = Field(default=None, alias = "description")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")
    
    _convert_user_tags = split_str_validator('user_tags')
    
