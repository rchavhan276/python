from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_summary_crud import get_asset_summary, get_asset_summary_by_asset_tag
from ...schemas.asset_summary_schema import AssetSummaryModel

router = APIRouter()

# Standard Routers

@router.get("/asset_summary/all", response_model=List[AssetSummaryModel])
def get_all_asset_summary(db: Session = Depends(get_db)):
    asset_summary = get_asset_summary(db)
    if not asset_summary:
        raise HTTPException(status_code=404, detail="Asset Summary not found")
    return asset_summary

@router.get("/asset_summary/tag/{asset_tag}", response_model=AssetSummaryModel)
def get_an_asset_summary_by_asset_tag(asset_tag: str, db: Session = Depends(get_db)):
    asset_summary = get_asset_summary_by_asset_tag(db, asset_tag)
    if not asset_summary:
        raise HTTPException(status_code=404, detail="Asset Summary not found")
    return asset_summary