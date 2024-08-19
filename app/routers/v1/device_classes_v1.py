from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.device_class_crud import get_device_classes, get_device_class_by_id, create_device_class, create_device_classes, get_device_class_by_device_class_name
from ...schemas.device_class_schema import DeviceClassModel, AddDeviceClassModel

router = APIRouter()

# Standard Routes

@router.get("/device_classes/all", response_model=List[DeviceClassModel])
def get_all_device_classes(db: Session = Depends(get_db)):
    device_classes = get_device_classes(db)
    if not device_classes:
        raise HTTPException(status_code=404, detail="Device Classes not found")
    return device_classes

@router.get("/device_classes/{id}", response_model=DeviceClassModel)
def get_device_class_by_uuid(id: UUID, db: Session = Depends(get_db)):
    device_class = get_device_class_by_id(db, id)
    if not device_class:
        raise HTTPException(status_code=404, detail="Device Class not found")
    return device_class

@router.post("/device_classes/single", response_model=DeviceClassModel)
def create_a_new_device_class(device_class: AddDeviceClassModel, db: Session = Depends(get_db)):
    new_device_class = create_device_class(db, device_class)
    if not new_device_class:
        raise HTTPException(status_code=500, detail="Error creating new device_class")
    return new_device_class

@router.post("/device_classes/multi", response_model=List[DeviceClassModel])
def create_multiple_new_device_classes(device_classes: List[AddDeviceClassModel], db: Session = Depends(get_db)):
    new_device_classes = create_device_classes(db, device_classes)
    if not new_device_classes:
        raise HTTPException(status_code=500, detail="Error creating new device_classes")
    return new_device_classes

# Specific Routes

@router.get("/device_classes/name/{device_class_name}", response_model=DeviceClassModel)
def get_a_device_class_by_device_class_name(device_class_name: str, db: Session = Depends(get_db)):
    device_class = get_device_class_by_device_class_name(db, device_class_name)
    if not device_class:
        raise HTTPException(status_code=404, detail="Device Class not found")
    return device_class