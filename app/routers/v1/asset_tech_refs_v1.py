from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_tech_ref_crud import get_asset_tech_refs, get_asset_tech_ref_by_id, get_asset_tech_ref_by_asset_id, create_asset_tech_ref, create_asset_tech_refs
from ...schemas.asset_tech_ref_schema import AssetTechRefModel, AddAssetTechRefModel

router = APIRouter()

@router.get("/asset_tech_refs/all", response_model=List[AssetTechRefModel])
def get_all_asset_tech_refs(db: Session = Depends(get_db)):
    asset_tech_refs = get_asset_tech_refs(db)
    if not asset_tech_refs:
        raise HTTPException(status_code=404, detail="Asset Tech Refs not found")
    return asset_tech_refs

@router.get("/asset_tech_refs/{id}", response_model=AssetTechRefModel)
def get_asset_tech_ref_by_uuid(id: str, db: Session = Depends(get_db)):
    asset_tech_ref = get_asset_tech_ref_by_id(db, id)
    if not asset_tech_ref:
        raise HTTPException(status_code=404, detail="Asset Tech Ref not found")
    return asset_tech_ref

# New endpoint for SOP SVC
@router.get("/asset_tech_refs/asset/{asset_id}", response_model=AssetTechRefModel)
def get_asset_tech_ref_by_asset(asset_id: str, db: Session = Depends(get_db)):
    asset_tech_ref = get_asset_tech_ref_by_asset_id(db, asset_id)
    if not asset_tech_ref:
        raise HTTPException(status_code=404, detail="Asset Tech Ref not found")
    return asset_tech_ref

@router.post("/asset_tech_refs/single", response_model=AssetTechRefModel)
def create_a_new_asset_tech_ref(asset_tech_ref: AddAssetTechRefModel, db: Session = Depends(get_db)):
    new_asset_tech_ref = create_asset_tech_ref(db, asset_tech_ref)
    if not new_asset_tech_ref:
        raise HTTPException(status_code=500, detail="Error creating new asset_tech_ref")
    return new_asset_tech_ref

@router.post("/asset_tech_refs/multi", response_model=List[AssetTechRefModel])
def create_multiple_new_asset_tech_refs(asset_tech_refs: List[AddAssetTechRefModel], db: Session = Depends(get_db)):
    new_asset_tech_refs = create_asset_tech_refs(db, asset_tech_refs)
    if not new_asset_tech_refs:
        raise HTTPException(status_code=500, detail="Error creating new asset_tech_refs")
    return new_asset_tech_refs