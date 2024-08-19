import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.system_device_type_model import SystemDeviceType
from ..schemas.system_device_type_schema import SystemDeviceTypeModel

def get_systems_device_types(db: Session) -> List[SystemDeviceType]:
    try:
        return db.query(SystemDeviceType).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_system_device_type_by_id(db: Session, id: UUID ) -> Union[SystemDeviceType, None]:
    try:
        return db.query(SystemDeviceType).filter(SystemDeviceType.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_system_device_type(db: Session, system_device_type: SystemDeviceTypeModel) -> SystemDeviceType:
    try:
        new_system_device_type = SystemDeviceType(**system_device_type.model_dump())
        # Generate UUID for new system_device_type
        unique_data = str(new_system_device_type.system_id) + str(new_system_device_type.device_type_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}systems_device_types",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_system_device_type.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new system_device_type: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_system_device_type.created_at = datetime.now()
        new_system_device_type.updated_at = new_system_device_type.created_at        
        
        db.add(new_system_device_type)
        db.commit()
        db.refresh(new_system_device_type)
        return new_system_device_type
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_systems_device_types(db: Session, systems_device_types: List[SystemDeviceTypeModel]) -> List[SystemDeviceType]:
    try:
        new_systems_device_types = []
        # Prepare payload for batch UUID generation
        items = []
        for system_device_type in systems_device_types:
            unique_data = str(system_device_type.system_id) + str(system_device_type.device_type_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}systems_device_types",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to system_device_types
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(systems_device_types):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_systems_device_types = []
        for system_device_type, uuid_item in zip(systems_device_types, uuid_items):
            # Convert SystemDeviceTypeModel to a dictionary and add the generated UUID
            system_device_type_dict = system_device_type.model_dump()
            system_device_type_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            system_device_type_dict['created_at'] = datetime.now()
            system_device_type_dict['updated_at'] = system_device_type_dict['created_at']
            
            
            # Create SystemDeviceType instance with the new id and add to list
            new_system_device_type = SystemDeviceType(**system_device_type_dict)
            new_systems_device_types.append(new_system_device_type)
        
        #Add new system_device_types to database
        db.add_all(new_systems_device_types)
        db.commit()
        for new_system_device_type in new_systems_device_types:
            db.refresh(new_system_device_type)
        return new_systems_device_types
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise