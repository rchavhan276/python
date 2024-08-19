from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.lcm_source_crud import get_lcm_sources, get_lcm_source_by_id, create_lcm_source, create_lcm_sources
from ...schemas.lcm_source_schema import LcmSourceModel, AddLcmSourceModel

router = APIRouter()

@router.get("/lcm_sources/all", response_model=List[LcmSourceModel])
def get_all_lcm_sources(db: Session = Depends(get_db)):
    lcm_sources = get_lcm_sources(db)
    if not lcm_sources:
        raise HTTPException(status_code=404, detail="Device Classes not found")
    return lcm_sources

@router.get("/lcm_sources/{id}", response_model=LcmSourceModel)
def get_lcm_source_by_uuid(id: UUID, db: Session = Depends(get_db)):
    lcm_source = get_lcm_source_by_id(db, id)
    if not lcm_source:
        raise HTTPException(status_code=404, detail="Device Class not found")
    return lcm_source

@router.post("/lcm_sources/single", response_model=LcmSourceModel)
def create_a_new_lcm_source(lcm_source: AddLcmSourceModel, db: Session = Depends(get_db)):
    new_lcm_source = create_lcm_source(db, lcm_source)
    if not new_lcm_source:
        raise HTTPException(status_code=500, detail="Error creating new lcm_source")
    return new_lcm_source

@router.post("/lcm_sources/multi", response_model=List[LcmSourceModel])
def create_multiple_new_lcm_sources(lcm_sources: List[AddLcmSourceModel], db: Session = Depends(get_db)):
    new_lcm_sources = create_lcm_sources(db, lcm_sources)
    if not new_lcm_sources:
        raise HTTPException(status_code=500, detail="Error creating new lcm_sources")
    return new_lcm_sources