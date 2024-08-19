from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class AssetHierarchyModel(BaseModel):
    id: UUID
    parent_asset_id: UUID
    child_asset_id: UUID
    created_at: datetime
    updated_at: datetime


class AddAssetHierarchyModel(BaseModel):
    parent_asset_id: UUID = Field(alias = "parentAssetId")
    child_asset_id: UUID = Field(alias = "childAssetId")
   
    
    
   
    
