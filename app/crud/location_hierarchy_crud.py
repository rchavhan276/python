import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.location_hierarchy_model import LocationHierarchy
from ..schemas.location_hierarchy_schema import LocationHierarchyModel

def get_location_hierarchies(db: Session) -> List[LocationHierarchy]:
    try:
        return db.query(LocationHierarchy).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_location_hierarchy_by_id(db: Session, id: UUID ) -> Union[LocationHierarchy, None]:
    try:
        return db.query(LocationHierarchy).filter(LocationHierarchy.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_location_hierarchy(db: Session, location_hierarchy: LocationHierarchyModel) -> LocationHierarchy:
    try:
        new_location_hierarchy = LocationHierarchy(**location_hierarchy.model_dump())
        # Generate UUID for new location_hierarchy
        unique_data = str(new_location_hierarchy.parent_location_id) + str(new_location_hierarchy.child_location_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}location_hierarchy",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_location_hierarchy.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new location_hierarchy: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_location_hierarchy.created_at = datetime.now()
        new_location_hierarchy.updated_at = new_location_hierarchy.created_at        
        
        db.add(new_location_hierarchy)
        db.commit()
        db.refresh(new_location_hierarchy)
        return new_location_hierarchy
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_location_hierarchies(db: Session, location_hierarchies: List[LocationHierarchyModel]) -> List[LocationHierarchy]:
    try:
        new_location_hierarchies = []
        # Prepare payload for batch UUID generation
        items = []
        for location_hierarchy in location_hierarchies:
            unique_data = str(location_hierarchy.parent_location_id) + str(location_hierarchy.child_location_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}location_hierarchy",
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
        if len(uuid_items) != len(location_hierarchies):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_location_hierarchies = []
        for location_hierarchy, uuid_item in zip(location_hierarchies, uuid_items):
            # Convert LocationHierarchyModel to a dictionary and add the generated UUID
            location_hierarchy_dict = location_hierarchy.model_dump()
            location_hierarchy_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            location_hierarchy_dict['created_at'] = datetime.now()
            location_hierarchy_dict['updated_at'] = location_hierarchy_dict['created_at']
            
            
            # Create Location instance with the new id and add to list
            new_location_hierarchy = LocationHierarchy(**location_hierarchy_dict)
            new_location_hierarchies.append(new_location_hierarchy)
        
        #Add new device_classs to database
        db.add_all(new_location_hierarchies)
        db.commit()
        for new_location_hierarchy in new_location_hierarchies:
            db.refresh(new_location_hierarchy)
        return new_location_hierarchies
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise