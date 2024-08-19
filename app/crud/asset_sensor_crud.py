import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.asset_sensor_model import AssetSensor
from ..schemas.asset_sensor_schema import AssetSensorModel

def get_asset_sensors(db: Session) -> List[AssetSensor]:
    try:
        return db.query(AssetSensor).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_sensor_by_id(db: Session, id: UUID ) -> Union[AssetSensor, None]:
    try:
        return db.query(AssetSensor).filter(AssetSensor.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_sensor(db: Session, asset_sensor: AssetSensorModel) -> AssetSensor:
    try:
        new_asset_sensor = AssetSensor(**asset_sensor.model_dump())
        # Generate UUID for new asset_sensor
        unique_data = str(new_asset_sensor.asset_id) + str(new_asset_sensor.sensor_name)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_sensors",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_asset_sensor.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new asset_sensor: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_asset_sensor.created_at = datetime.now()
        new_asset_sensor.updated_at = new_asset_sensor.created_at        
        
        db.add(new_asset_sensor)
        db.commit()
        db.refresh(new_asset_sensor)
        return new_asset_sensor
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_sensors(db: Session, asset_sensors: List[AssetSensorModel]) -> List[AssetSensor]:
    try:
        new_asset_sensors = []
        # Prepare payload for batch UUID generation
        items = []
        for asset_sensor in asset_sensors:
            unique_data = str(asset_sensor.asset_id) + str(asset_sensor.sensor_name)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_sensors",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to asset_sensors
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(asset_sensors):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_asset_sensors = []
        for asset_sensor, uuid_item in zip(asset_sensors, uuid_items):
            # Convert AssetSensorModel to a dictionary and add the generated UUID
            asset_sensor_dict = asset_sensor.model_dump()
            asset_sensor_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            asset_sensor_dict['created_at'] = datetime.now()
            asset_sensor_dict['updated_at'] = asset_sensor_dict['created_at']
            
            
            # Create AssetSensor instance with the new id and add to list
            new_asset_sensor = AssetSensor(**asset_sensor_dict)
            new_asset_sensors.append(new_asset_sensor)
        
        #Add new asset_sensors to database
        db.add_all(new_asset_sensors)
        db.commit()
        for new_asset_sensor in new_asset_sensors:
            db.refresh(new_asset_sensor)
        return new_asset_sensors
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise