from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import json_validator, split_str_validator

class AssetActionModel(BaseModel):
    id: UUID
    asset_id: UUID
    action_type_id: UUID
    action_name: str
    action_scope: Optional[dict] = {}
    action_source_info: Optional[dict] = {}
    description: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddAssetActionModel(BaseModel):
    asset_id: UUID = Field(alias = "assetId")
    action_type_id: UUID = Field(alias = "actionTypeId")
    action_name: str = Field(alias = "actionName")
    action_scope: Optional[dict] = Field(default={}, alias = "actionScope")
    action_source_info: Optional[dict] = Field(default={}, alias = "actionSourceInfo")
    description: Optional[str] = Field(default=None, alias = "description")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")
    
    
    _parse_json_properties = json_validator('action_scope', 'action_source_info')
    _convert_user_tags = split_str_validator('user_tags')
    
