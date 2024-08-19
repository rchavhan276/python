from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import json_validator, split_str_validator

class ClientModel(BaseModel):
    id: UUID
    region_id: UUID
    country_id: UUID
    client_code: str
    client_name: str
    client_address: Optional[dict] = {}
    client_contact: Optional[dict] = {}
    description: Optional[str] = None
    crm_reference: Optional[str] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddClientModel(BaseModel):
    region_id: UUID = Field(alias = "regionId")
    country_id: UUID = Field(alias = "countryId")
    client_code: str = Field(alias = "clientCode")
    client_name: str = Field(alias = "clientName")
    client_address: Optional[dict] = Field(default={}, alias = "clientAddress")
    client_contact: Optional[dict] = Field(default={}, alias = "clientContact")
    description: Optional[str] = Field(default=None, alias = "description")
    crm_reference: Optional[str] = Field(default=None, alias = "crmReference")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")
    
    
    _parse_json_properties = json_validator('client_address', 'client_contact')
    _convert_user_tags = split_str_validator('user_tags')
    
