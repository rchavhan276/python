from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import split_str_validator

class AssetOwnerModel(BaseModel):
    id: UUID
    client_id: UUID
    employee_code: str
    first_name: str
    last_name: str
    department: str
    email: str
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddAssetOwnerModel(BaseModel):
    client_id: UUID = Field(alias="clientId")
    employee_code: str = Field(alias="assetTag")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    department: str = Field(alias="department")
    email: str = Field(alias="email")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")

    _convert_user_tags = split_str_validator('user_tags')




