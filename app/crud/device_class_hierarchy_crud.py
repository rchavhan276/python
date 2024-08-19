import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.device_class_hierarchy_model import DeviceClassHierarchy
from ..schemas.device_class_hierarchy_schema import DeviceClassHierarchyModel

def get_device_class_hierarchies(db: Session) -> List[DeviceClassHierarchy]:
    try:
        return db.query(DeviceClassHierarchy).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_device_class_hierarchy_by_id(db: Session, id: UUID ) -> Union[DeviceClassHierarchy, None]:
    try:
        return db.query(DeviceClassHierarchy).filter(DeviceClassHierarchy.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_device_class_hierarchy(db: Session, device_class_hierarchy: DeviceClassHierarchyModel) -> DeviceClassHierarchy:
    try:
        new_device_class_hierarchy = DeviceClassHierarchy(**device_class_hierarchy.model_dump())
        # Generate UUID for new device_class_hierarchy
        unique_data = str(new_device_class_hierarchy.parent_device_class_id) + str(new_device_class_hierarchy.child_device_class_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}device_class_hierarchy",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_device_class_hierarchy.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new device_class_hierarchy: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_device_class_hierarchy.created_at = datetime.now()
        new_device_class_hierarchy.updated_at = new_device_class_hierarchy.created_at        
        
        db.add(new_device_class_hierarchy)
        db.commit()
        db.refresh(new_device_class_hierarchy)
        return new_device_class_hierarchy
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_device_class_hierarchies(db: Session, device_class_hierarchies: List[DeviceClassHierarchyModel]) -> List[DeviceClassHierarchy]:
    try:
        new_device_class_hierarchies = []
        # Prepare payload for batch UUID generation
        items = []
        for device_class_hierarchy in device_class_hierarchies:
            unique_data = str(device_class_hierarchy.parent_device_class_id) + str(device_class_hierarchy.child_device_class_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}device_class_hierarchy",
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
        if len(uuid_items) != len(device_class_hierarchies):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_device_class_hierarchies = []
        for device_class_hierarchy, uuid_item in zip(device_class_hierarchies, uuid_items):
            # Convert DeviceClassHierarchyModel to a dictionary and add the generated UUID
            device_class_hierarchy_dict = device_class_hierarchy.model_dump()
            device_class_hierarchy_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            device_class_hierarchy_dict['created_at'] = datetime.now()
            device_class_hierarchy_dict['updated_at'] = device_class_hierarchy_dict['created_at']
            
            
            # Create DeviceClass instance with the new id and add to list
            new_device_class_hierarchy = DeviceClassHierarchy(**device_class_hierarchy_dict)
            new_device_class_hierarchies.append(new_device_class_hierarchy)
        
        #Add new device_classs to database
        db.add_all(new_device_class_hierarchies)
        db.commit()
        for new_device_class_hierarchy in new_device_class_hierarchies:
            db.refresh(new_device_class_hierarchy)
        return new_device_class_hierarchies
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise