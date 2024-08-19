import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.system_model import System
from ..schemas.system_schema import SystemModel
from ..models.category_system_model import CategorySystem

# Standard CRUD

def get_systems(db: Session) -> List[System]:
    try:
        return db.query(System).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_system_by_id(db: Session, id: UUID ) -> Union[System, None]:
    try:
        return db.query(System).filter(System.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise
    
def create_system(db: Session, system: SystemModel) -> System:
    try:
        new_system = System(**system.model_dump())
        # Generate UUID for new system
        unique_data = str(new_system.system_name)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_systems",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_system.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new system: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_system.created_at = datetime.now()
        new_system.updated_at = new_system.created_at        
        
        db.add(new_system)
        db.commit()
        db.refresh(new_system)
        return new_system
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_systems(db: Session, systems: List[SystemModel]) -> List[System]:
    try:
        new_systems = []
        # Prepare payload for batch UUID generation
        items = []
        for system in systems:
            unique_data = str(system.system_name)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_systems",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()
        
        # Map generated UUIDs to systems
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(systems):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_systems = []
        for system, uuid_item in zip(systems, uuid_items):
            # Convert SystemModel to a dictionary and add the generated UUID
            system_dict = system.model_dump()
            system_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            system_dict['created_at'] = datetime.now()
            system_dict['updated_at'] = system_dict['created_at']

            # Create System instance with the new id and add to list
            new_system = System(**system_dict)
            new_systems.append(new_system)
        
        # Add new systems to database
        db.add_all(new_systems)
        db.commit()
        # Refresh each new system from the database
        for new_system in new_systems:
            db.refresh(new_system)
        return new_systems
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

def get_system_by_system_name(db: Session, system_name: str) -> Union[System, None]:
    try:
        return db.query(System).filter(System.system_name == system_name).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

# Get systems associated with a category (join on categories_systems table)
def get_systems_by_category_id(db: Session, category_id: UUID) -> List[System]:
    try:
        return db.query(System).join(CategorySystem).filter(CategorySystem.category_id == category_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise