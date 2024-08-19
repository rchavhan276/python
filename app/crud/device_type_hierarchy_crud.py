import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.device_type_hierarchy_model import DeviceTypeHierarchy
from ..schemas.device_type_hierarchy_schema import DeviceTypeHierarchyModel

def get_device_type_hierarchies(db: Session) -> List[DeviceTypeHierarchy]:
    try:
        return db.query(DeviceTypeHierarchy).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_device_type_hierarchy_by_id(db: Session, id: UUID ) -> Union[DeviceTypeHierarchy, None]:
    try:
        return db.query(DeviceTypeHierarchy).filter(DeviceTypeHierarchy.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_device_type_hierarchy(db: Session, device_type_hierarchy: DeviceTypeHierarchyModel) -> DeviceTypeHierarchy:
    try:
        new_device_type_hierarchy = DeviceTypeHierarchy(**device_type_hierarchy.model_dump())
        # Generate UUID for new device_type_hierarchy
        unique_data = str(new_device_type_hierarchy.parent_device_type_id) + str(new_device_type_hierarchy.child_device_type_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}device_type_hierarchy",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_device_type_hierarchy.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new device_type_hierarchy: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_device_type_hierarchy.created_at = datetime.now()
        new_device_type_hierarchy.updated_at = new_device_type_hierarchy.created_at        
        
        db.add(new_device_type_hierarchy)
        db.commit()
        db.refresh(new_device_type_hierarchy)
        return new_device_type_hierarchy
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_device_type_hierarchies(db: Session, device_type_hierarchies: List[DeviceTypeHierarchyModel]) -> List[DeviceTypeHierarchy]:
    try:
        new_device_type_hierarchies = []
        # Prepare payload for batch UUID generation
        items = []
        for device_type_hierarchy in device_type_hierarchies:
            unique_data = str(device_type_hierarchy.parent_device_type_id) + str(device_type_hierarchy.child_device_type_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}device_type_hierarchy",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to device_classs
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(device_type_hierarchies):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_device_type_hierarchies = []
        for device_type_hierarchy, uuid_item in zip(device_type_hierarchies, uuid_items):
            # Convert DeviceTypeHierarchyModel to a dictionary and add the generated UUID
            device_type_hierarchy_dict = device_type_hierarchy.model_dump()
            device_type_hierarchy_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            device_type_hierarchy_dict['created_at'] = datetime.now()
            device_type_hierarchy_dict['updated_at'] = device_type_hierarchy_dict['created_at']
            
            
            # Create DeviceType instance with the new id and add to list
            new_device_type_hierarchy = DeviceTypeHierarchy(**device_type_hierarchy_dict)
            new_device_type_hierarchies.append(new_device_type_hierarchy)
        
        #Add new device_classs to database
        db.add_all(new_device_type_hierarchies)
        db.commit()
        for new_device_type_hierarchy in new_device_type_hierarchies:
            db.refresh(new_device_type_hierarchy)
        return new_device_type_hierarchies
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise