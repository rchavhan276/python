from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.device_type_crud import get_device_types, get_device_type_by_id, create_device_type, create_device_types, get_device_type_by_device_type_name, get_device_types_by_system_id
from ...schemas.device_type_schema import DeviceTypeModel, AddDeviceTypeModel

router = APIRouter()

# Standard Routers

@router.get("/device_types/all", response_model=List[DeviceTypeModel])
def get_all_device_types(db: Session = Depends(get_db)):
    device_types = get_device_types(db)
    if not device_types:
        raise HTTPException(status_code=404, detail="Device Types not found")
    return device_types

@router.get("/device_types/{id}", response_model=DeviceTypeModel)
def get_device_type_by_uuid(id: UUID, db: Session = Depends(get_db)):
    device_type = get_device_type_by_id(db, id)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device Type not found")
    return device_type

@router.post("/device_types/single", response_model=DeviceTypeModel)
def create_a_new_device_type(device_type: AddDeviceTypeModel, db: Session = Depends(get_db)):
    new_device_type = create_device_type(db, device_type)
    if not new_device_type:
        raise HTTPException(status_code=500, detail="Error creating new device_type")
    return new_device_type

@router.post("/device_types/multi", response_model=List[DeviceTypeModel])
def create_multiple_new_device_types(device_types: List[AddDeviceTypeModel], db: Session = Depends(get_db)):
    new_device_types = create_device_types(db, device_types)
    if not new_device_types:
        raise HTTPException(status_code=500, detail="Error creating new device_types")
    return new_device_types

# Specific Routers

@router.get("/device_types/name/{device_type_name}", response_model=DeviceTypeModel)
def get_a_device_type_by_device_type_name(device_type_name: str, db: Session = Depends(get_db)):
    device_type = get_device_type_by_device_type_name(db, device_type_name)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device Type not found")
    return device_type

@router.get("/device_types/system/{system_id}", response_model=List[DeviceTypeModel])
def get_all_device_types_for_system_id(system_id: UUID, db: Session = Depends(get_db)):
    device_types = get_device_types_by_system_id(db, system_id)
    if not device_types:
        raise HTTPException(status_code=404, detail="Device Types not found")
    return device_types