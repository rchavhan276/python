from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import json_validator, split_str_validator

class LocationModel(BaseModel):
    id: UUID
    client_id: UUID
    location_code: str
    location_name: str
    location_type: str
    is_outdoor: bool
    is_hazloc: bool
    hazloc_spec: Optional[dict] = {}
    description: Optional[str] = None
    geo_coordinates: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class GeoCoordinatesModel(BaseModel):
    latitude: float
    longitude: float


class AddLocationModel(BaseModel):
    client_id: UUID = Field(alias="clientId")
    location_code: str = Field(alias="locationCode")
    location_name: str = Field(alias="locationName")
    location_type: str = Field(alias="locationType")
    is_outdoor: bool = Field(alias="isOutdoor")
    is_hazloc: bool = Field(alias="isHazLoc")
    hazloc_spec: Optional[dict] = Field(default={}, alias="hazLocSpec")
    description: Optional[str] = Field(default=None, alias="description")
    geo_coordinates: Optional[GeoCoordinatesModel] = Field(default=None, alias="geoCoordinates")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")

    _parse_json_properties = json_validator('hazloc_spec')
    _convert_user_tags = split_str_validator('user_tags')




