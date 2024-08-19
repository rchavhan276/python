from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_owner_crud import get_asset_owners, get_asset_owner_by_id, create_asset_owner, create_asset_owners
from ...schemas.asset_owner_schema import AssetOwnerModel, AddAssetOwnerModel

router = APIRouter()

@router.get("/asset_owners/all", response_model=List[AssetOwnerModel])
def get_all_asset_owners(db: Session = Depends(get_db)):
    asset_owners = get_asset_owners(db)
    if not asset_owners:
        raise HTTPException(status_code=404, detail="Asset Owners not found")
    return asset_owners

@router.get("/asset_owners/{id}", response_model=AssetOwnerModel)
def get_asset_owner_by_uuid(id: UUID, db: Session = Depends(get_db)):
    asset_owner = get_asset_owner_by_id(db, id)
    if not asset_owner:
        raise HTTPException(status_code=404, detail="Asset Owner not found")
    return asset_owner

@router.post("/asset_owners/single", response_model=AssetOwnerModel)
def create_a_new_asset_owner(asset_owner: AddAssetOwnerModel, db: Session = Depends(get_db)):
    new_asset_owner = create_asset_owner(db, asset_owner)
    if not new_asset_owner:
        raise HTTPException(status_code=500, detail="Error creating new asset owner")
    return new_asset_owner

@router.post("/asset_owners/multi", response_model=List[AssetOwnerModel])
def create_multiple_new_asset_owners(asset_owners: List[AddAssetOwnerModel], db: Session = Depends(get_db)):
    new_asset_owners = create_asset_owners(db, asset_owners)
    if not new_asset_owners:
        raise HTTPException(status_code=500, detail="Error creating new asset owners")
    return new_asset_owners