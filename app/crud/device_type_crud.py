import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.device_type_model import DeviceType
from ..schemas.device_type_schema import DeviceTypeModel
from ..models.system_device_type_model import SystemDeviceType

# Standard CRUD

def get_device_types(db: Session) -> List[DeviceType]:
    try:
        return db.query(DeviceType).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_device_type_by_id(db: Session, id: UUID ) -> Union[DeviceType, None]:
    try:
        return db.query(DeviceType).filter(DeviceType.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_device_type(db: Session, device_type: DeviceTypeModel) -> DeviceType:
    try:
        new_device_type = DeviceType(**device_type.model_dump())
        # Generate UUID for new device_type
        unique_data = str(new_device_type.asset_device_type_name)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_device_types",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_device_type.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new device_type: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_device_type.created_at = datetime.now()
        new_device_type.updated_at = new_device_type.created_at        
        
        db.add(new_device_type)
        db.commit()
        db.refresh(new_device_type)
        return new_device_type
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_device_types(db: Session, device_types: List[DeviceTypeModel]) -> List[DeviceType]:
    try:
        new_device_types = []
        # Prepare payload for batch UUID generation
        items = []
        for device_type in device_types:
            unique_data = str(device_type.asset_device_type_name)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_device_types",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to device_types
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(device_types):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_device_types = []
        for device_type, uuid_item in zip(device_types, uuid_items):
            # Convert DeviceTypeModel to a dictionary and add the generated UUID
            device_type_dict = device_type.model_dump()
            device_type_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            device_type_dict['created_at'] = datetime.now()
            device_type_dict['updated_at'] = device_type_dict['created_at']
            
            
            # Create DeviceType instance with the new id and add to list
            new_device_type = DeviceType(**device_type_dict)
            new_device_types.append(new_device_type)
        
        #Add new device_types to database
        db.add_all(new_device_types)
        db.commit()
        for new_device_type in new_device_types:
            db.refresh(new_device_type)
        return new_device_types
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

def get_device_type_by_device_type_name(db: Session, device_type_name: str) -> Union[DeviceType, None]:
    try:
        return db.query(DeviceType).filter(DeviceType.asset_device_type_name == device_type_name).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

# Get device_types associated with a system (join on systems_device_types table)
def get_device_types_by_system_id(db: Session, system_id: UUID) -> List[DeviceType]:
    try:
        return db.query(DeviceType).join(SystemDeviceType).filter(SystemDeviceType.system_id == system_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise