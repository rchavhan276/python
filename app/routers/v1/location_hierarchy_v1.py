from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.location_hierarchy_crud import get_location_hierarchies, get_location_hierarchy_by_id, create_location_hierarchy, create_location_hierarchies
from ...schemas.location_hierarchy_schema import LocationHierarchyModel, AddLocationHierarchyModel

router = APIRouter()

@router.get("/location_hierarchies/all", response_model=List[LocationHierarchyModel])
def get_all_location_hierarchies(db: Session = Depends(get_db)):
    location_hierarchies = get_location_hierarchies(db)
    if not location_hierarchies:
        raise HTTPException(status_code=404, detail="Action Types not found")
    return location_hierarchies

@router.get("/location_hierarchies/{id}", response_model=LocationHierarchyModel)
def get_location_hierarchy_by_uuid(id: UUID, db: Session = Depends(get_db)):
    location_hierarchy = get_location_hierarchy_by_id(db, id)
    if not location_hierarchy:
        raise HTTPException(status_code=404, detail="Action Type not found")
    return location_hierarchy

@router.post("/location_hierarchies/single", response_model=LocationHierarchyModel)
def create_a_new_location_hierarchy(location_hierarchy: AddLocationHierarchyModel, db: Session = Depends(get_db)):
    new_location_hierarchy = create_location_hierarchy(db, location_hierarchy)
    if not new_location_hierarchy:
        raise HTTPException(status_code=500, detail="Error creating new action type")
    return new_location_hierarchy

@router.post("/location_hierarchies/multi", response_model=List[LocationHierarchyModel])
def create_multiple_new_location_hierarchies(location_hierarchies: List[AddLocationHierarchyModel], db: Session = Depends(get_db)):
    new_location_hierarchies = create_location_hierarchies(db, location_hierarchies)
    if not new_location_hierarchies:
        raise HTTPException(status_code=500, detail="Error creating new action types")
    return new_location_hierarchies