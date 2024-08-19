from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_admin_ref_crud import get_asset_admin_refs, get_asset_admin_ref_by_id, create_asset_admin_ref, create_asset_admin_refs
from ...schemas.asset_admin_ref_schema import AssetAdminRefModel, AddAssetAdminRefModel

router = APIRouter()

@router.get("/asset_admin_refs/all", response_model=List[AssetAdminRefModel])
def get_all_asset_admin_refs(db: Session = Depends(get_db)):
    asset_admin_refs = get_asset_admin_refs(db)
    if not asset_admin_refs:
        raise HTTPException(status_code=404, detail="Asset Admin Refs not found")
    return asset_admin_refs

@router.get("/asset_admin_refs/{id}", response_model=AssetAdminRefModel)
def get_asset_admin_ref_by_uuid(id: UUID, db: Session = Depends(get_db)):
    asset_admin_ref = get_asset_admin_ref_by_id(db, id)
    if not asset_admin_ref:
        raise HTTPException(status_code=404, detail="Asset Admin Ref not found")
    return asset_admin_ref

@router.post("/asset_admin_refs/single", response_model=AssetAdminRefModel)
def create_a_new_asset_admin_ref(asset_admin_ref: AddAssetAdminRefModel, db: Session = Depends(get_db)):
    new_asset_admin_ref = create_asset_admin_ref(db, asset_admin_ref)
    if not new_asset_admin_ref:
        raise HTTPException(status_code=500, detail="Error creating new asset_admin_ref")
    return new_asset_admin_ref

@router.post("/asset_admin_refs/multi", response_model=List[AssetAdminRefModel])
def create_multiple_new_asset_admin_refs(asset_admin_refs: List[AddAssetAdminRefModel], db: Session = Depends(get_db)):
    new_asset_admin_refs = create_asset_admin_refs(db, asset_admin_refs)
    if not new_asset_admin_refs:
        raise HTTPException(status_code=500, detail="Error creating new asset_admin_refs")
    return new_asset_admin_refs