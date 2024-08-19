from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.asset_alarm_crud import get_asset_alarms, get_asset_alarm_by_id, create_asset_alarm, create_asset_alarms
from ...schemas.asset_alarm_schema import AssetAlarmModel, AddAssetAlarmModel

router = APIRouter()

@router.get("/asset_alarms/all", response_model=List[AssetAlarmModel])
def get_all_asset_alarms(db: Session = Depends(get_db)):
    asset_alarms = get_asset_alarms(db)
    if not asset_alarms:
        raise HTTPException(status_code=404, detail="Alarms not found")
    return asset_alarms

@router.get("/asset_alarms/{id}", response_model=AssetAlarmModel)
def get_asset_alarm_by_uuid(id: UUID, db: Session = Depends(get_db)):
    asset_alarm = get_asset_alarm_by_id(db, id)
    if not asset_alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return asset_alarm

@router.post("/asset_alarms/single", response_model=AssetAlarmModel)
def create_a_new_asset_alarm(asset_alarm: AddAssetAlarmModel, db: Session = Depends(get_db)):
    new_asset_alarm = create_asset_alarm(db, asset_alarm)
    if not new_asset_alarm:
        raise HTTPException(status_code=500, detail="Error creating new alarm")
    return new_asset_alarm

@router.post("/asset_alarms/multi", response_model=List[AssetAlarmModel])
def create_multiple_new_asset_alarms(asset_alarms: List[AddAssetAlarmModel], db: Session = Depends(get_db)):
    new_asset_alarms = create_asset_alarms(db, asset_alarms)
    if not new_asset_alarms:
        raise HTTPException(status_code=500, detail="Error creating new alarms")
    return new_asset_alarms