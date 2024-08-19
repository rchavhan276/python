from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.system_crud import get_systems, get_system_by_id, create_system, create_systems, get_system_by_system_name, get_systems_by_category_id
from ...schemas.system_schema import SystemModel, AddSystemModel

router = APIRouter()

# Standard Routers

@router.get("/systems/all", response_model=List[SystemModel])
def get_all_systems(db: Session = Depends(get_db)):
    systems = get_systems(db)
    if not systems:
        raise HTTPException(status_code=404, detail="Systems not found")
    return systems

@router.get("/systems/{id}", response_model=SystemModel)
def get_system_by_uuid(id: UUID, db: Session = Depends(get_db)):
    system = get_system_by_id(db, id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system

@router.post("/systems/single", response_model=SystemModel)
def create_a_new_system(system: AddSystemModel, db: Session = Depends(get_db)):
    new_system = create_system(db, system)
    if not new_system:
        raise HTTPException(status_code=500, detail="Error creating new system")
    return new_system

@router.post("/systems/multi", response_model=List[SystemModel])
def create_multiple_new_systems(systems: List[AddSystemModel], db: Session = Depends(get_db)):
    new_systems = create_systems(db, systems)
    if not new_systems:
        raise HTTPException(status_code=500, detail="Error creating new systems")
    return new_systems

# Specific Routers
@router.get("/systems/name/{system_name}", response_model=SystemModel)
def get_a_system_by_system_name(system_name: str, db: Session = Depends(get_db)):
    system = get_system_by_system_name(db, system_name)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system

@router.get("/systems/category/{category_id}", response_model=List[SystemModel])
def get_all_systems_for_category_id(category_id: UUID, db: Session = Depends(get_db)):
    systems = get_systems_by_category_id(db, category_id)
    if not systems:
        raise HTTPException(status_code=404, detail="Systems not found")
    return systems