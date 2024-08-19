import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.device_class_model import DeviceClass
from ..schemas.device_class_schema import DeviceClassModel

# Standard CRUD

def get_device_classes(db: Session) -> List[DeviceClass]:
    try:
        return db.query(DeviceClass).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_device_class_by_id(db: Session, id: UUID ) -> Union[DeviceClass, None]:
    try:
        return db.query(DeviceClass).filter(DeviceClass.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_device_class(db: Session, device_class: DeviceClassModel) -> DeviceClass:
    try:
        new_device_class = DeviceClass(**device_class.model_dump())
        # Generate UUID for new device_class
        unique_data = str(new_device_class.asset_device_class_name)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_device_classes",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_device_class.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new device_class: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_device_class.created_at = datetime.now()
        new_device_class.updated_at = new_device_class.created_at        
        
        db.add(new_device_class)
        db.commit()
        db.refresh(new_device_class)
        return new_device_class
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_device_classes(db: Session, device_classes: List[DeviceClassModel]) -> List[DeviceClass]:
    try:
        new_device_classes = []
        # Prepare payload for batch UUID generation
        items = []
        for device_class in device_classes:
            unique_data = str(device_class.asset_device_class_name)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_device_classes",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()
        
        # Map generated UUIDs to device_classes
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(device_classes):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_device_classes = []
        for device_class, uuid_item in zip(device_classes, uuid_items):
            # Convert DeviceClassModel to a dictionary and add the generated UUID
            device_class_dict = device_class.model_dump()
            device_class_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            device_class_dict['created_at'] = datetime.now()
            device_class_dict['updated_at'] = device_class_dict['created_at']

            # Create DeviceClass instance with the new id and add to list
            new_device_class = DeviceClass(**device_class_dict)
            new_device_classes.append(new_device_class)
        
        # Add new device_classes to database
        db.add_all(new_device_classes)
        db.commit()
        # Refresh each new device_class from the database
        for new_device_class in new_device_classes:
            db.refresh(new_device_class)
        return new_device_classes
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

# Specific CRUD

def get_device_class_by_device_class_name(db: Session, asset_device_class_name: str) -> Union[DeviceClass, None]:
    try:
        return db.query(DeviceClass).filter(DeviceClass.asset_device_class_name == asset_device_class_name).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise