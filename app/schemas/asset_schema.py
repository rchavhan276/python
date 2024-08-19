from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import split_str_validator

class AssetModel(BaseModel):
    id: UUID
    client_id: UUID
    project_id: UUID
    location_id: UUID
    category_id: UUID
    system_id: UUID
    device_type_id: UUID
    asset_tag: str
    description: Optional[str]
    is_active: bool
    geo_coordinates: Optional[str]
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class GeoCoordinatesModel(BaseModel):
    latitude: float
    longitude: float


class AddAssetModel(BaseModel):
    client_id: UUID = Field(alias="clientId")
    project_id: UUID = Field(alias="projectId")
    location_id: UUID = Field(alias="locationId")
    category_id: UUID = Field(alias="categoryId")
    system_id: UUID = Field(alias="systemId")
    device_type_id: UUID = Field(alias="deviceTypeId")
    asset_tag: str = Field(alias="assetTag")
    description: Optional[str] = Field(alias="description")
    is_active: bool = Field(alias="isActive")
    geo_coordinates: Optional[GeoCoordinatesModel] = Field(alias="geoCoordinates")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")

    _convert_user_tags = split_str_validator('user_tags')




