from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import json_validator, split_str_validator

class AssetAlarmModel(BaseModel):
    id: UUID
    asset_id: UUID
    alarm_name: str
    alarm_scope: Optional[dict] = {}
    alarm_source_info: Optional[dict] = {}
    description: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddAssetAlarmModel(BaseModel):
    asset_id: UUID = Field(alias = "assetId")
    alarm_name: str = Field(alias = "alarmName")
    alarm_scope: Optional[dict] = Field(default={}, alias = "alarmScope")
    alarm_source_info: Optional[dict] = Field(default={}, alias = "alarmSourceInfo")
    description: Optional[str] = Field(default=None, alias = "description")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")
    
    
    _parse_json_properties = json_validator('alarm_scope', 'alarm_source_info')
    _convert_user_tags = split_str_validator('user_tags')
    
