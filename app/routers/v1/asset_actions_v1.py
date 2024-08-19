from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_action_crud import get_asset_actions, get_asset_action_by_id, create_asset_action, create_asset_actions
from ...schemas.asset_action_schema import AssetActionModel, AddAssetActionModel

router = APIRouter()

@router.get("/asset_actions/all", response_model=List[AssetActionModel])
def get_all_asset_actions(db: Session = Depends(get_db)):
    asset_actions = get_asset_actions(db)
    if not asset_actions:
        raise HTTPException(status_code=404, detail="Actions not found")
    return asset_actions

@router.get("/asset_actions/{id}", response_model=AssetActionModel)
def get_asset_action_by_uuid(id: UUID, db: Session = Depends(get_db)):
    asset_action = get_asset_action_by_id(db, id)
    if not asset_action:
        raise HTTPException(status_code=404, detail="Action not found")
    return asset_action

@router.post("/asset_actions/single", response_model=AssetActionModel)
def create_a_new_asset_action(asset_action: AddAssetActionModel, db: Session = Depends(get_db)):
    new_asset_action = create_asset_action(db, asset_action)
    if not new_asset_action:
        raise HTTPException(status_code=500, detail="Error creating new action")
    return new_asset_action

@router.post("/asset_actions/multi", response_model=List[AssetActionModel])
def create_multiple_new_asset_actions(asset_actions: List[AddAssetActionModel], db: Session = Depends(get_db)):
    new_asset_actions = create_asset_actions(db, asset_actions)
    if not new_asset_actions:
        raise HTTPException(status_code=500, detail="Error creating new actions")
    return new_asset_actions