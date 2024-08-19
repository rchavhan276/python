from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.device_class_hierarchy_crud import get_device_class_hierarchies, get_device_class_hierarchy_by_id, create_device_class_hierarchy, create_device_class_hierarchies
from ...schemas.device_class_hierarchy_schema import DeviceClassHierarchyModel, AddDeviceClassHierarchyModel

router = APIRouter()

@router.get("/device_class_hierarchies/all", response_model=List[DeviceClassHierarchyModel])
def get_all_device_class_hierarchies(db: Session = Depends(get_db)):
    device_class_hierarchies = get_device_class_hierarchies(db)
    if not device_class_hierarchies:
        raise HTTPException(status_code=404, detail="Device Class Hierarchies not found")
    return device_class_hierarchies

@router.get("/device_class_hierarchies/{id}", response_model=DeviceClassHierarchyModel)
def get_device_class_hierarchy_by_uuid(id: UUID, db: Session = Depends(get_db)):
    device_class_hierarchy = get_device_class_hierarchy_by_id(db, id)
    if not device_class_hierarchy:
        raise HTTPException(status_code=404, detail="Device Class Hierarchy not found")
    return device_class_hierarchy

@router.post("/device_class_hierarchies/single", response_model=DeviceClassHierarchyModel)
def create_a_new_device_class_hierarchy(device_class_hierarchy: AddDeviceClassHierarchyModel, db: Session = Depends(get_db)):
    new_device_class_hierarchy = create_device_class_hierarchy(db, device_class_hierarchy)
    if not new_device_class_hierarchy:
        raise HTTPException(status_code=500, detail="Error creating new device class hierarchy")
    return new_device_class_hierarchy

@router.post("/device_class_hierarchies/multi", response_model=List[DeviceClassHierarchyModel])
def create_multiple_new_device_class_hierarchies(device_class_hierarchies: List[AddDeviceClassHierarchyModel], db: Session = Depends(get_db)):
    new_device_class_hierarchies = create_device_class_hierarchies(db, device_class_hierarchies)
    if not new_device_class_hierarchies:
        raise HTTPException(status_code=500, detail="Error creating new device class hierarchies")
    return new_device_class_hierarchies