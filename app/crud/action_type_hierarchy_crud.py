import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.action_type_hierarchy_model import ActionTypeHierarchy
from ..schemas.action_type_hierarchy_schema import ActionTypeHierarchyModel

def get_action_type_hierarchies(db: Session) -> List[ActionTypeHierarchy]:
    try:
        return db.query(ActionTypeHierarchy).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_action_type_hierarchy_by_id(db: Session, id: UUID ) -> Union[ActionTypeHierarchy, None]:
    try:
        return db.query(ActionTypeHierarchy).filter(ActionTypeHierarchy.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_action_type_hierarchy(db: Session, action_type_hierarchy: ActionTypeHierarchyModel) -> ActionTypeHierarchy:
    try:
        new_action_type_hierarchy = ActionTypeHierarchy(**action_type_hierarchy.model_dump())
        # Generate UUID for new action_type_hierarchy
        unique_data = str(new_action_type_hierarchy.parent_action_type_id) + str(new_action_type_hierarchy.child_action_type_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}action_type_hierarchy",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_action_type_hierarchy.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new action_type_hierarchy: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_action_type_hierarchy.created_at = datetime.now()
        new_action_type_hierarchy.updated_at = new_action_type_hierarchy.created_at        
        
        db.add(new_action_type_hierarchy)
        db.commit()
        db.refresh(new_action_type_hierarchy)
        return new_action_type_hierarchy
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_action_type_hierarchies(db: Session, action_type_hierarchies: List[ActionTypeHierarchyModel]) -> List[ActionTypeHierarchy]:
    try:
        new_action_type_hierarchies = []
        # Prepare payload for batch UUID generation
        items = []
        for action_type_hierarchy in action_type_hierarchies:
            unique_data = str(action_type_hierarchy.parent_action_type_id) + str(action_type_hierarchy.child_action_type_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}action_type_hierarchy",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to action_types
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(action_type_hierarchies):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_action_type_hierarchies = []
        for action_type_hierarchy, uuid_item in zip(action_type_hierarchies, uuid_items):
            # Convert ActionTypeHierarchyModel to a dictionary and add the generated UUID
            action_type_hierarchy_dict = action_type_hierarchy.model_dump()
            action_type_hierarchy_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            action_type_hierarchy_dict['created_at'] = datetime.now()
            action_type_hierarchy_dict['updated_at'] = action_type_hierarchy_dict['created_at']
            
            
            # Create ActionType instance with the new id and add to list
            new_action_type_hierarchy = ActionTypeHierarchy(**action_type_hierarchy_dict)
            new_action_type_hierarchies.append(new_action_type_hierarchy)
        
        #Add new action_types to database
        db.add_all(new_action_type_hierarchies)
        db.commit()
        for new_action_type_hierarchy in new_action_type_hierarchies:
            db.refresh(new_action_type_hierarchy)
        return new_action_type_hierarchies
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise