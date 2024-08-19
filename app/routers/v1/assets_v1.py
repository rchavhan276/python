from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_crud import get_assets, get_asset_by_id, create_asset, create_assets, get_assets_by_client_id, get_assets_by_project_id, get_assets_by_location_id, get_assets_by_category_id, get_assets_by_system_id, get_assets_by_device_type_id, get_asset_by_asset_tag
from ...schemas.asset_schema import AssetModel, AddAssetModel

router = APIRouter()

# Standard Routers

@router.get("/assets/all", response_model=List[AssetModel])
def get_all_assets(db: Session = Depends(get_db)):
    assets = get_assets(db)
    if not assets:
        raise HTTPException(status_code=404, detail="Assets not found")
    return assets

@router.get("/assets/{id}", response_model=AssetModel)
def get_asset_by_uuid(id: UUID, db: Session = Depends(get_db)):
    asset = get_asset_by_id(db, id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.post("/assets/single", response_model=AssetModel)
def create_a_new_asset(asset: AddAssetModel, db: Session = Depends(get_db)):
    new_asset = create_asset(db, asset)
    if not new_asset:
        raise HTTPException(status_code=500, detail="Error creating new asset")
    return new_asset

@router.post("/assets/multi", response_model=List[AssetModel])
def create_multiple_new_assets(assets: List[AddAssetModel], db: Session = Depends(get_db)):
    new_assets = create_assets(db, assets)
    if not new_assets:
        raise HTTPException(status_code=500, detail="Error creating new assets")
    return new_assets

# Specific Routers

@router.get("assets/client/{client_id}", response_model=List[AssetModel])
def get_all_assets_for_client_id(client_id: UUID, db: Session = Depends(get_db)):
    assets = get_assets_by_client_id(db, client_id)
    if not assets:
        raise HTTPException(status_code=404, detail="Assets not found")
    return assets

@router.get("/assets/project/{project_id}", response_model=List[AssetModel])
def get_all_assets_for_project_id(project_id: UUID, db: Session = Depends(get_db)):
    assets = get_assets_by_project_id(db, project_id)
    if not assets:
        raise HTTPException(status_code=404, detail="Assets not found")
    return assets

@router.get("/assets/location/{location_id}", response_model=List[AssetModel])
def get_all_assets_for_location_id(location_id: UUID, db: Session = Depends(get_db)):
    assets = get_assets_by_location_id(db, location_id)
    if not assets:
        raise HTTPException(status_code=404, detail="Assets not found")
    return assets

@router.get("/assets/category/{category_id}", response_model=List[AssetModel])
def get_all_assets_for_category_id(category_id: UUID, db: Session = Depends(get_db)):
    assets = get_assets_by_category_id(db, category_id)
    if not assets:
        raise HTTPException(status_code=404, detail="Assets not found")
    return assets

@router.get("/assets/system/{system_id}", response_model=List[AssetModel])
def get_all_assets_for_system_id(system_id: UUID, db: Session = Depends(get_db)):
    assets = get_assets_by_system_id(db, system_id)
    if not assets:
        raise HTTPException(status_code=404, detail="Assets not found")
    return assets

@router.get("/assets/device_type/{device_type_id}", response_model=List[AssetModel])
def get_all_assets_for_device_type_id(device_type_id: UUID, db: Session = Depends(get_db)):
    assets = get_assets_by_device_type_id(db, device_type_id)
    if not assets:
        raise HTTPException(status_code=404, detail="Assets not found")
    return assets

@router.get("/assets/tag/{asset_tag}", response_model=AssetModel)
def get_an_asset_by_asset_tag(asset_tag: str, db: Session = Depends(get_db)):
    asset = get_asset_by_asset_tag(db, asset_tag)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset