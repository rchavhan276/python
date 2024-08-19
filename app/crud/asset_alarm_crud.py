import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.asset_alarm_model import AssetAlarm
from ..schemas.asset_alarm_schema import AssetAlarmModel

def get_asset_alarms(db: Session) -> List[AssetAlarm]:
    try:
        return db.query(AssetAlarm).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_alarm_by_id(db: Session, id: UUID ) -> Union[AssetAlarm, None]:
    try:
        return db.query(AssetAlarm).filter(AssetAlarm.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_alarm(db: Session, asset_alarm: AssetAlarmModel) -> AssetAlarm:
    try:
        new_asset_alarm = AssetAlarm(**asset_alarm.model_dump())
        # Generate UUID for new asset_alarm
        unique_data = str(new_asset_alarm.asset_id) + str(new_asset_alarm.alarm_name)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_alarms",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_asset_alarm.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new asset_alarm: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_asset_alarm.created_at = datetime.now()
        new_asset_alarm.updated_at = new_asset_alarm.created_at        
        
        db.add(new_asset_alarm)
        db.commit()
        db.refresh(new_asset_alarm)
        return new_asset_alarm
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_alarms(db: Session, asset_alarms: List[AssetAlarmModel]) -> List[AssetAlarm]:
    try:
        new_asset_alarms = []
        # Prepare payload for batch UUID generation
        items = []
        for asset_alarm in asset_alarms:
            unique_data = str(asset_alarm.asset_id) + str(asset_alarm.alarm_name)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_alarms",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to asset_alarms
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(asset_alarms):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_asset_alarms = []
        for asset_alarm, uuid_item in zip(asset_alarms, uuid_items):
            # Convert AssetAlarmModel to a dictionary and add the generated UUID
            asset_alarm_dict = asset_alarm.model_dump()
            asset_alarm_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            asset_alarm_dict['created_at'] = datetime.now()
            asset_alarm_dict['updated_at'] = asset_alarm_dict['created_at']
            
            
            # Create AssetAlarm instance with the new id and add to list
            new_asset_alarm = AssetAlarm(**asset_alarm_dict)
            new_asset_alarms.append(new_asset_alarm)
        
        #Add new asset_alarms to database
        db.add_all(new_asset_alarms)
        db.commit()
        for new_asset_alarm in new_asset_alarms:
            db.refresh(new_asset_alarm)
        return new_asset_alarms
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise