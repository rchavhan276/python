import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.category_system_model import CategorySystem
from ..schemas.category_system_schema import CategorySystemModel

def get_categories_systems(db: Session) -> List[CategorySystem]:
    try:
        return db.query(CategorySystem).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_category_system_by_id(db: Session, id: UUID ) -> Union[CategorySystem, None]:
    try:
        return db.query(CategorySystem).filter(CategorySystem.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_category_system(db: Session, category_system: CategorySystemModel) -> CategorySystem:
    try:
        new_category_system = CategorySystem(**category_system.model_dump())
        # Generate UUID for new category_system
        unique_data = str(new_category_system.category_id) + str(new_category_system.system_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}categories_systems",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_category_system.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new category_system: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_category_system.created_at = datetime.now()
        new_category_system.updated_at = new_category_system.created_at        
        
        db.add(new_category_system)
        db.commit()
        db.refresh(new_category_system)
        return new_category_system
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_categories_systems(db: Session, categories_systems: List[CategorySystemModel]) -> List[CategorySystem]:
    try:
        new_categories_systems = []
        # Prepare payload for batch UUID generation
        items = []
        for category_system in categories_systems:
            unique_data = str(category_system.category_id) + str(category_system.system_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}categories_systems",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to category_systems
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(categories_systems):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_categories_systems = []
        for category_system, uuid_item in zip(categories_systems, uuid_items):
            # Convert CategorySystemModel to a dictionary and add the generated UUID
            category_system_dict = category_system.model_dump()
            category_system_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            category_system_dict['created_at'] = datetime.now()
            category_system_dict['updated_at'] = category_system_dict['created_at']
            
            
            # Create CategorySystem instance with the new id and add to list
            new_category_system = CategorySystem(**category_system_dict)
            new_categories_systems.append(new_category_system)
        
        #Add new category_systems to database
        db.add_all(new_categories_systems)
        db.commit()
        for new_category_system in new_categories_systems:
            db.refresh(new_category_system)
        return new_categories_systems
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise