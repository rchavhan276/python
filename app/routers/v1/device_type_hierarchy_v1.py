from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.device_type_hierarchy_crud import get_device_type_hierarchies, get_device_type_hierarchy_by_id, create_device_type_hierarchy, create_device_type_hierarchies
from ...schemas.device_type_hierarchy_schema import DeviceTypeHierarchyModel, AddDeviceTypeHierarchyModel

router = APIRouter()

@router.get("/device_type_hierarchies/all", response_model=List[DeviceTypeHierarchyModel])
def get_all_device_type_hierarchies(db: Session = Depends(get_db)):
    device_type_hierarchies = get_device_type_hierarchies(db)
    if not device_type_hierarchies:
        raise HTTPException(status_code=404, detail="Device Type Hierarchies not found")
    return device_type_hierarchies

@router.get("/device_type_hierarchies/{id}", response_model=DeviceTypeHierarchyModel)
def get_device_type_hierarchy_by_uuid(id: UUID, db: Session = Depends(get_db)):
    device_type_hierarchy = get_device_type_hierarchy_by_id(db, id)
    if not device_type_hierarchy:
        raise HTTPException(status_code=404, detail="Device Type Hierarchy not found")
    return device_type_hierarchy

@router.post("/device_type_hierarchies/single", response_model=DeviceTypeHierarchyModel)
def create_a_new_device_type_hierarchy(device_type_hierarchy: AddDeviceTypeHierarchyModel, db: Session = Depends(get_db)):
    new_device_type_hierarchy = create_device_type_hierarchy(db, device_type_hierarchy)
    if not new_device_type_hierarchy:
        raise HTTPException(status_code=500, detail="Error creating new device type hierarchy")
    return new_device_type_hierarchy

@router.post("/device_type_hierarchies/multi", response_model=List[DeviceTypeHierarchyModel])
def create_multiple_new_device_type_hierarchies(device_type_hierarchies: List[AddDeviceTypeHierarchyModel], db: Session = Depends(get_db)):
    new_device_type_hierarchies = create_device_type_hierarchies(db, device_type_hierarchies)
    if not new_device_type_hierarchies:
        raise HTTPException(status_code=500, detail="Error creating new device type hierarchies")
    return new_device_type_hierarchies