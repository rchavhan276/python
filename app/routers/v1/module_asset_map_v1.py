from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.module_asset_map_crud import get_module_asset_maps, get_module_asset_map_by_id, create_module_asset_map, create_module_asset_maps
from ...schemas.module_asset_map_schema import ModuleAssetMapModel, AddModuleAssetMapModel

router = APIRouter()

@router.get("/module_asset_maps/all", response_model=List[ModuleAssetMapModel])
def get_all_module_asset_maps(db: Session = Depends(get_db)):
    module_asset_maps = get_module_asset_maps(db)
    if not module_asset_maps:
        raise HTTPException(status_code=404, detail="Module Asset Map relationships not found")
    return module_asset_maps

@router.get("/module_asset_maps/{id}", response_model=ModuleAssetMapModel)
def get_module_asset_map_by_uuid(id: UUID, db: Session = Depends(get_db)):
    module_asset_map = get_module_asset_map_by_id(db, id)
    if not module_asset_map:
        raise HTTPException(status_code=404, detail="Module Asset Map relationship not found")
    return module_asset_map

@router.post("/module_asset_maps/single", response_model=ModuleAssetMapModel)
def create_a_new_module_asset_map(module_asset_map: AddModuleAssetMapModel, db: Session = Depends(get_db)):
    new_module_asset_map = create_module_asset_map(db, module_asset_map)
    if not new_module_asset_map:
        raise HTTPException(status_code=500, detail="Error creating new Module Asset Map relationship")
    return new_module_asset_map

@router.post("/module_asset_maps/multi", response_model=List[ModuleAssetMapModel])
def create_multiple_new_module_asset_maps(module_asset_maps: List[AddModuleAssetMapModel], db: Session = Depends(get_db)):
    new_module_asset_maps = create_module_asset_maps(db, module_asset_maps)
    if not new_module_asset_maps:
        raise HTTPException(status_code=500, detail="Error creating new Module Asset Map relationships")
    return new_module_asset_maps