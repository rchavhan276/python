import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.action_type_model import ActionType
from ..schemas.action_type_schema import ActionTypeModel

def get_action_types(db: Session) -> List[ActionType]:
    try:
        return db.query(ActionType).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_action_type_by_id(db: Session, id: UUID ) -> Union[ActionType, None]:
    try:
        return db.query(ActionType).filter(ActionType.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_action_type(db: Session, action_type: ActionTypeModel) -> ActionType:
    try:
        new_action_type = ActionType(**action_type.model_dump())
        # Generate UUID for new action_type
        unique_data = str(new_action_type.action_type)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_action_types",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_action_type.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new action_type: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_action_type.created_at = datetime.now()
        new_action_type.updated_at = new_action_type.created_at        
        
        db.add(new_action_type)
        db.commit()
        db.refresh(new_action_type)
        return new_action_type
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_action_types(db: Session, action_types: List[ActionTypeModel]) -> List[ActionType]:
    try:
        new_action_types = []
        # Prepare payload for batch UUID generation
        items = []
        for action_type in action_types:
            unique_data = str(action_type.action_type)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_action_types",
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
        if len(uuid_items) != len(action_types):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_action_types = []
        for action_type, uuid_item in zip(action_types, uuid_items):
            # Convert ActionTypeModel to a dictionary and add the generated UUID
            action_type_dict = action_type.model_dump()
            action_type_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            action_type_dict['created_at'] = datetime.now()
            action_type_dict['updated_at'] = action_type_dict['created_at']
            
            
            # Create ActionType instance with the new id and add to list
            new_action_type = ActionType(**action_type_dict)
            new_action_types.append(new_action_type)
        
        #Add new action_types to database
        db.add_all(new_action_types)
        db.commit()
        for new_action_type in new_action_types:
            db.refresh(new_action_type)
        return new_action_types
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise