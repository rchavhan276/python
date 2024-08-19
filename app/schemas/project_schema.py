from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime, date
from uuid import UUID
from ..utils.validators import split_str_validator

class ProjectModel(BaseModel):
    id: UUID
    client_id: UUID
    project_code: str
    project_name: str
    description: Optional[str] = None
    cn_project_code: Optional[str] = None
    lcm_contract_ref: Optional[str] = None
    lcm_contract_tier: Optional[str] = None
    lcm_contract_startdate: Optional[date] = None
    lcm_contract_enddate: Optional[date] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddProjectModel(BaseModel):
    client_id: UUID = Field(alias="clientId")
    project_code: str = Field(alias="projectCode")
    project_name: str = Field(alias="projectName")
    description: Optional[str] = Field(default=None, alias="description")
    cn_project_code: Optional[str] = Field(default=None, alias="cnProjectCode")
    lcm_contract_ref: Optional[str] = Field(default=None, alias="lcmContractRef")
    lcm_contract_tier: Optional[str] = Field(default=None, alias="lcmContractTier")
    lcm_contract_startdate: Optional[date] = Field(default=None, alias="lcmContractStartdate")
    lcm_contract_enddate: Optional[date] = Field(default=None, alias="lcmContractEnddate")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")

    _convert_user_tags = split_str_validator('user_tags')




