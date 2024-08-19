from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_sensor_crud import get_asset_sensors, get_asset_sensor_by_id, create_asset_sensor, create_asset_sensors
from ...schemas.asset_sensor_schema import AssetSensorModel, AddAssetSensorModel

router = APIRouter()

@router.get("/asset_sensors/all", response_model=List[AssetSensorModel])
def get_all_asset_sensors(db: Session = Depends(get_db)):
    asset_sensors = get_asset_sensors(db)
    if not asset_sensors:
        raise HTTPException(status_code=404, detail="Sensors not found")
    return asset_sensors

@router.get("/asset_sensors/{id}", response_model=AssetSensorModel)
def get_asset_sensor_by_uuid(id: UUID, db: Session = Depends(get_db)):
    asset_sensor = get_asset_sensor_by_id(db, id)
    if not asset_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return asset_sensor

@router.post("/asset_sensors/single", response_model=AssetSensorModel)
def create_a_new_asset_sensor(asset_sensor: AddAssetSensorModel, db: Session = Depends(get_db)):
    new_asset_sensor = create_asset_sensor(db, asset_sensor)
    if not new_asset_sensor:
        raise HTTPException(status_code=500, detail="Error creating new sensor")
    return new_asset_sensor

@router.post("/asset_sensors/multi", response_model=List[AssetSensorModel])
def create_multiple_new_asset_sensors(asset_sensors: List[AddAssetSensorModel], db: Session = Depends(get_db)):
    new_asset_sensors = create_asset_sensors(db, asset_sensors)
    if not new_asset_sensors:
        raise HTTPException(status_code=500, detail="Error creating new sensors")
    return new_asset_sensors