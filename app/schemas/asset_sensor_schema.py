from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import json_validator, split_str_validator, json_or_int_validator

class AssetSensorModel(BaseModel):
    id: UUID
    asset_id: UUID
    sensor_name: str
    sensor_type: str
    value_type: str
    value_unit: str
    sensor_scope: Optional[dict] = {}
    sensor_source_info: Optional[Any] = None # TODO: This should be jsonb, but all values in the database are integers in this column. Need to figure out how to handle this.
    description: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddAssetSensorModel(BaseModel):
    asset_id: UUID = Field(alias = "assetId")
    sensor_name: str = Field(alias = "sensorName")
    sensor_type: str = Field(alias = "sensorType")
    value_type: str = Field(alias = "valueType")
    value_unit: str = Field(alias = "valueUnit")
    sensor_scope: Optional[dict] = Field(default={}, alias = "sensorScope")
    sensor_source_info: Optional[Union[int, dict]] = Field(default=None, alias = "sensorSourceInfo") # TODO: This should be jsonb, but all values in the database are integers in this column. Need to figure out how to handle this.
    description: Optional[str] = Field(default=None, alias = "description")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")
    
    
    _parse_json_properties = json_validator('sensor_scope')
    _parse_json_or_int_properties = json_or_int_validator('sensor_source_info') # TODO: This is tempporary validator until we figure out how to handle the sensor_source_info column in the database
    _convert_user_tags = split_str_validator('user_tags')
    
