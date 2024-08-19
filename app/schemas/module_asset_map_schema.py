from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class ModuleAssetMapModel(BaseModel):
    id: UUID
    module_id: UUID
    asset_id: UUID
    created_at: datetime
    updated_at: datetime


class AddModuleAssetMapModel(BaseModel):
    module_id: UUID = Field(alias = "lcmSourceId")
    asset_id: UUID = Field(alias = "assetId")
 