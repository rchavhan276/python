from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.system_hierarchy_crud import get_system_hierarchies, get_system_hierarchy_by_id, create_system_hierarchy, create_system_hierarchies
from ...schemas.system_hierarchy_schema import SystemHierarchyModel, AddSystemHierarchyModel

router = APIRouter()

@router.get("/system_hierarchies/all", response_model=List[SystemHierarchyModel])
def get_all_system_hierarchies(db: Session = Depends(get_db)):
    system_hierarchies = get_system_hierarchies(db)
    if not system_hierarchies:
        raise HTTPException(status_code=404, detail="System Hierarchies not found")
    return system_hierarchies

@router.get("/system_hierarchies/{id}", response_model=SystemHierarchyModel)
def get_system_hierarchy_by_uuid(id: UUID, db: Session = Depends(get_db)):
    system_hierarchy = get_system_hierarchy_by_id(db, id)
    if not system_hierarchy:
        raise HTTPException(status_code=404, detail="System Hierarchy not found")
    return system_hierarchy

@router.post("/system_hierarchies/single", response_model=SystemHierarchyModel)
def create_a_new_system_hierarchy(system_hierarchy: AddSystemHierarchyModel, db: Session = Depends(get_db)):
    new_system_hierarchy = create_system_hierarchy(db, system_hierarchy)
    if not new_system_hierarchy:
        raise HTTPException(status_code=500, detail="Error creating new system hierarchy")
    return new_system_hierarchy

@router.post("/system_hierarchies/multi", response_model=List[SystemHierarchyModel])
def create_multiple_new_system_hierarchies(system_hierarchies: List[AddSystemHierarchyModel], db: Session = Depends(get_db)):
    new_system_hierarchies = create_system_hierarchies(db, system_hierarchies)
    if not new_system_hierarchies:
        raise HTTPException(status_code=500, detail="Error creating new system hierarchies")
    return new_system_hierarchies