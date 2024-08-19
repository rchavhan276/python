from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_location_crud import get_asset_location
from ...schemas.asset_location_schema import AssetLocationModel

router = APIRouter()

@router.get("/asset_location/all", response_model=List[AssetLocationModel])
def get_all_asset_location(db: Session = Depends(get_db)):
    try:
        asset_location = get_asset_location(db)
        if not asset_location:
            raise HTTPException(status_code=404, detail="Asset Location not found")
        return asset_location
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))