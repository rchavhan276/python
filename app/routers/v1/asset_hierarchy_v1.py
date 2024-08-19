from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_hierarchy_crud import get_asset_hierarchies, get_asset_hierarchy_by_id, create_asset_hierarchy, create_asset_hierarchies
from ...schemas.asset_hierarchy_schema import AssetHierarchyModel, AddAssetHierarchyModel

router = APIRouter()

@router.get("/asset_hierarchies/all", response_model=List[AssetHierarchyModel])
def get_all_asset_hierarchies(db: Session = Depends(get_db)):
    asset_hierarchies = get_asset_hierarchies(db)
    if not asset_hierarchies:
        raise HTTPException(status_code=404, detail="Action Types not found")
    return asset_hierarchies

@router.get("/asset_hierarchies/{id}", response_model=AssetHierarchyModel)
def get_asset_hierarchy_by_uuid(id: UUID, db: Session = Depends(get_db)):
    asset_hierarchy = get_asset_hierarchy_by_id(db, id)
    if not asset_hierarchy:
        raise HTTPException(status_code=404, detail="Action Type not found")
    return asset_hierarchy

@router.post("/asset_hierarchies/single", response_model=AssetHierarchyModel)
def create_a_new_asset_hierarchy(asset_hierarchy: AddAssetHierarchyModel, db: Session = Depends(get_db)):
    new_asset_hierarchy = create_asset_hierarchy(db, asset_hierarchy)
    if not new_asset_hierarchy:
        raise HTTPException(status_code=500, detail="Error creating new action type")
    return new_asset_hierarchy

@router.post("/asset_hierarchies/multi", response_model=List[AssetHierarchyModel])
def create_multiple_new_asset_hierarchies(asset_hierarchies: List[AddAssetHierarchyModel], db: Session = Depends(get_db)):
    new_asset_hierarchies = create_asset_hierarchies(db, asset_hierarchies)
    if not new_asset_hierarchies:
        raise HTTPException(status_code=500, detail="Error creating new action types")
    return new_asset_hierarchies