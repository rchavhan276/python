import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.system_hierarchy_model import SystemHierarchy
from ..schemas.system_hierarchy_schema import SystemHierarchyModel

def get_system_hierarchies(db: Session) -> List[SystemHierarchy]:
    try:
        return db.query(SystemHierarchy).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_system_hierarchy_by_id(db: Session, id: UUID ) -> Union[SystemHierarchy, None]:
    try:
        return db.query(SystemHierarchy).filter(SystemHierarchy.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_system_hierarchy(db: Session, system_hierarchy: SystemHierarchyModel) -> SystemHierarchy:
    try:
        new_system_hierarchy = SystemHierarchy(**system_hierarchy.model_dump())
        # Generate UUID for new system_hierarchy
        unique_data = str(new_system_hierarchy.parent_system_id) + str(new_system_hierarchy.child_system_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}system_hierarchy",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_system_hierarchy.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new system_hierarchy: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_system_hierarchy.created_at = datetime.now()
        new_system_hierarchy.updated_at = new_system_hierarchy.created_at        
        
        db.add(new_system_hierarchy)
        db.commit()
        db.refresh(new_system_hierarchy)
        return new_system_hierarchy
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_system_hierarchies(db: Session, system_hierarchies: List[SystemHierarchyModel]) -> List[SystemHierarchy]:
    try:
        new_system_hierarchies = []
        # Prepare payload for batch UUID generation
        items = []
        for system_hierarchy in system_hierarchies:
            unique_data = str(system_hierarchy.parent_system_id) + str(system_hierarchy.child_system_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}system_hierarchy",
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
        if len(uuid_items) != len(system_hierarchies):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_system_hierarchies = []
        for system_hierarchy, uuid_item in zip(system_hierarchies, uuid_items):
            # Convert SystemHierarchyModel to a dictionary and add the generated UUID
            system_hierarchy_dict = system_hierarchy.model_dump()
            system_hierarchy_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            system_hierarchy_dict['created_at'] = datetime.now()
            system_hierarchy_dict['updated_at'] = system_hierarchy_dict['created_at']
            
            
            # Create System instance with the new id and add to list
            new_system_hierarchy = SystemHierarchy(**system_hierarchy_dict)
            new_system_hierarchies.append(new_system_hierarchy)
        
        #Add new device_classs to database
        db.add_all(new_system_hierarchies)
        db.commit()
        for new_system_hierarchy in new_system_hierarchies:
            db.refresh(new_system_hierarchy)
        return new_system_hierarchies
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise