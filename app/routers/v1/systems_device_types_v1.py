from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.system_device_type_crud import get_systems_device_types, get_system_device_type_by_id, create_system_device_type, create_systems_device_types
from ...schemas.system_device_type_schema import SystemDeviceTypeModel, AddSystemDeviceTypeModel

router = APIRouter()

@router.get("/systems_device_types/all", response_model=List[SystemDeviceTypeModel])
def get_all_systems_device_types(db: Session = Depends(get_db)):
    systems_device_types = get_systems_device_types(db)
    if not systems_device_types:
        raise HTTPException(status_code=404, detail="System Device Type relationships not found")
    return systems_device_types

@router.get("/systems_device_types/{id}", response_model=SystemDeviceTypeModel)
def get_system_device_type_by_uuid(id: UUID, db: Session = Depends(get_db)):
    system_device_type = get_system_device_type_by_id(db, id)
    if not system_device_type:
        raise HTTPException(status_code=404, detail="System Device Type relationship not found")
    return system_device_type

@router.post("/systems_device_types/single", response_model=SystemDeviceTypeModel)
def create_a_new_system_device_type(system_device_type: AddSystemDeviceTypeModel, db: Session = Depends(get_db)):
    new_system_device_type = create_system_device_type(db, system_device_type)
    if not new_system_device_type:
        raise HTTPException(status_code=500, detail="Error creating new System Device Type relationship")
    return new_system_device_type

@router.post("/systems_device_types/multi", response_model=List[SystemDeviceTypeModel])
def create_multiple_new_systems_device_types(systems_device_types: List[AddSystemDeviceTypeModel], db: Session = Depends(get_db)):
    new_systems_device_types = create_systems_device_types(db, systems_device_types)
    if not new_systems_device_types:
        raise HTTPException(status_code=500, detail="Error creating new System Device Type relationships")
    return new_systems_device_types