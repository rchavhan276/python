import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.category_hierarchy_model import CategoryHierarchy
from ..schemas.category_hierarchy_schema import CategoryHierarchyModel

def get_category_hierarchies(db: Session) -> List[CategoryHierarchy]:
    try:
        return db.query(CategoryHierarchy).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_category_hierarchy_by_id(db: Session, id: UUID ) -> Union[CategoryHierarchy, None]:
    try:
        return db.query(CategoryHierarchy).filter(CategoryHierarchy.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_category_hierarchy(db: Session, category_hierarchy: CategoryHierarchyModel) -> CategoryHierarchy:
    try:
        new_category_hierarchy = CategoryHierarchy(**category_hierarchy.model_dump())
        # Generate UUID for new category_hierarchy
        unique_data = str(new_category_hierarchy.parent_category_id) + str(new_category_hierarchy.child_category_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}category_hierarchy",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_category_hierarchy.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new category_hierarchy: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_category_hierarchy.created_at = datetime.now()
        new_category_hierarchy.updated_at = new_category_hierarchy.created_at        
        
        db.add(new_category_hierarchy)
        db.commit()
        db.refresh(new_category_hierarchy)
        return new_category_hierarchy
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_category_hierarchies(db: Session, category_hierarchies: List[CategoryHierarchyModel]) -> List[CategoryHierarchy]:
    try:
        new_category_hierarchies = []
        # Prepare payload for batch UUID generation
        items = []
        for category_hierarchy in category_hierarchies:
            unique_data = str(category_hierarchy.parent_category_id) + str(category_hierarchy.child_category_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}category_hierarchy",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to categorys
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(category_hierarchies):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_category_hierarchies = []
        for category_hierarchy, uuid_item in zip(category_hierarchies, uuid_items):
            # Convert CategoryHierarchyModel to a dictionary and add the generated UUID
            category_hierarchy_dict = category_hierarchy.model_dump()
            category_hierarchy_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            category_hierarchy_dict['created_at'] = datetime.now()
            category_hierarchy_dict['updated_at'] = category_hierarchy_dict['created_at']
            
            
            # Create Category instance with the new id and add to list
            new_category_hierarchy = CategoryHierarchy(**category_hierarchy_dict)
            new_category_hierarchies.append(new_category_hierarchy)
        
        #Add new categorys to database
        db.add_all(new_category_hierarchies)
        db.commit()
        for new_category_hierarchy in new_category_hierarchies:
            db.refresh(new_category_hierarchy)
        return new_category_hierarchies
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise