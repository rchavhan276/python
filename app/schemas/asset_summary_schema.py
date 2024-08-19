from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime, date
from uuid import UUID

class AssetSummaryModel(BaseModel):
    asset_id: UUID
    asset_tag: str
    asset_owner: Union[None, str]
    email: Union[None, str]
    client_name: str
    project_name: str
    location: str
    is_active: bool
    asset_lifecycle_status: str
    installation_date: Union[None, date]
    make: str
    model: str
    serial_number: str