from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import split_str_validator

class RegionModel(BaseModel):
    id: UUID
    region_name: str
    region_code: str
    description: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddRegionModel(BaseModel):
    region_id: UUID = Field(alias = "regionId")
    region_name: str = Field(alias = "regionName")
    region_code: str = Field(alias = "regionCode")
    description: Optional[str] = Field(default=None, alias = "description")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")
    
    
    _convert_user_tags = split_str_validator('user_tags')
    
