import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.asset_action_model import AssetAction
from ..schemas.asset_action_schema import AssetActionModel

def get_asset_actions(db: Session) -> List[AssetAction]:
    try:
        return db.query(AssetAction).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_action_by_id(db: Session, id: UUID ) -> Union[AssetAction, None]:
    try:
        return db.query(AssetAction).filter(AssetAction.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_action(db: Session, asset_action: AssetActionModel) -> AssetAction:
    try:
        new_asset_action = AssetAction(**asset_action.model_dump())
        # Generate UUID for new asset_action
        unique_data = str(new_asset_action.asset_id) + str(new_asset_action.action_type_id) + str(new_asset_action.action_name)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_actions",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_asset_action.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new asset_action: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_asset_action.created_at = datetime.now()
        new_asset_action.updated_at = new_asset_action.created_at        
        
        db.add(new_asset_action)
        db.commit()
        db.refresh(new_asset_action)
        return new_asset_action
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_actions(db: Session, asset_actions: List[AssetActionModel]) -> List[AssetAction]:
    try:
        new_asset_actions = []
        # Prepare payload for batch UUID generation
        items = []
        for asset_action in asset_actions:
            unique_data = str(asset_action.asset_id) + str(asset_action.action_type_id) + str(asset_action.action_name)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_actions",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to asset_actions
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(asset_actions):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_asset_actions = []
        for asset_action, uuid_item in zip(asset_actions, uuid_items):
            # Convert AssetActionModel to a dictionary and add the generated UUID
            asset_action_dict = asset_action.model_dump()
            asset_action_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            asset_action_dict['created_at'] = datetime.now()
            asset_action_dict['updated_at'] = asset_action_dict['created_at']
            
            
            # Create AssetAction instance with the new id and add to list
            new_asset_action = AssetAction(**asset_action_dict)
            new_asset_actions.append(new_asset_action)
        
        #Add new asset_actions to database
        db.add_all(new_asset_actions)
        db.commit()
        for new_asset_action in new_asset_actions:
            db.refresh(new_asset_action)
        return new_asset_actions
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise