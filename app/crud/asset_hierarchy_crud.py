import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.asset_hierarchy_model import AssetHierarchy
from ..schemas.asset_hierarchy_schema import AssetHierarchyModel

def get_asset_hierarchies(db: Session) -> List[AssetHierarchy]:
    try:
        return db.query(AssetHierarchy).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_hierarchy_by_id(db: Session, id: UUID ) -> Union[AssetHierarchy, None]:
    try:
        return db.query(AssetHierarchy).filter(AssetHierarchy.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_hierarchy(db: Session, asset_hierarchy: AssetHierarchyModel) -> AssetHierarchy:
    try:
        new_asset_hierarchy = AssetHierarchy(**asset_hierarchy.model_dump())
        # Generate UUID for new asset_hierarchy
        unique_data = str(new_asset_hierarchy.parent_asset_id) + str(new_asset_hierarchy.child_asset_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_hierarchy",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_asset_hierarchy.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new asset_hierarchy: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_asset_hierarchy.created_at = datetime.now()
        new_asset_hierarchy.updated_at = new_asset_hierarchy.created_at        
        
        db.add(new_asset_hierarchy)
        db.commit()
        db.refresh(new_asset_hierarchy)
        return new_asset_hierarchy
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_hierarchies(db: Session, asset_hierarchies: List[AssetHierarchyModel]) -> List[AssetHierarchy]:
    try:
        new_asset_hierarchies = []
        # Prepare payload for batch UUID generation
        items = []
        for asset_hierarchy in asset_hierarchies:
            unique_data = str(asset_hierarchy.parent_asset_id) + str(asset_hierarchy.child_asset_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_hierarchy",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to assets
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(asset_hierarchies):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_asset_hierarchies = []
        for asset_hierarchy, uuid_item in zip(asset_hierarchies, uuid_items):
            # Convert AssetHierarchyModel to a dictionary and add the generated UUID
            asset_hierarchy_dict = asset_hierarchy.model_dump()
            asset_hierarchy_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            asset_hierarchy_dict['created_at'] = datetime.now()
            asset_hierarchy_dict['updated_at'] = asset_hierarchy_dict['created_at']
            
            
            # Create Asset instance with the new id and add to list
            new_asset_hierarchy = AssetHierarchy(**asset_hierarchy_dict)
            new_asset_hierarchies.append(new_asset_hierarchy)
        
        #Add new assets to database
        db.add_all(new_asset_hierarchies)
        db.commit()
        for new_asset_hierarchy in new_asset_hierarchies:
            db.refresh(new_asset_hierarchy)
        return new_asset_hierarchies
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise