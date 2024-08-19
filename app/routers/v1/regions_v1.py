from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.region_crud import get_regions, get_region_by_id, create_region, create_regions
from ...schemas.region_schema import RegionModel, AddRegionModel

router = APIRouter()

@router.get("/regions/all", response_model=List[RegionModel])
def get_all_regions(db: Session = Depends(get_db)):
    regions = get_regions(db)
    if not regions:
        raise HTTPException(status_code=404, detail="Regions not found")
    return regions

@router.get("/regions/{id}", response_model=RegionModel)
def get_region_by_uuid(id: UUID, db: Session = Depends(get_db)):
    region = get_region_by_id(db, id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region

@router.post("/regions/single", response_model=RegionModel)
def create_a_new_region(region: AddRegionModel, db: Session = Depends(get_db)):
    new_region = create_region(db, region)
    if not new_region:
        raise HTTPException(status_code=500, detail="Error creating new region")
    return new_region

@router.post("/regions/multi", response_model=List[RegionModel])
def create_multiple_new_regions(regions: List[AddRegionModel], db: Session = Depends(get_db)):
    new_regions = create_regions(db, regions)
    if not new_regions:
        raise HTTPException(status_code=500, detail="Error creating new regions")
    return new_regions