import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.asset_owner_model import AssetOwner
from ..schemas.asset_owner_schema import AssetOwnerModel

def get_asset_owners(db: Session) -> List[AssetOwner]:
    try:
        return db.query(AssetOwner).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_owner_by_id(db: Session, id: UUID ) -> Union[AssetOwner, None]:
    try:
        return db.query(AssetOwner).filter(AssetOwner.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_owner(db: Session, asset_owner: AssetOwnerModel) -> AssetOwner:
    try:
        new_asset_owner = AssetOwner(**asset_owner.model_dump())
        # Generate UUID for new asset_owner
        unique_data = str(new_asset_owner.client_id) + str(new_asset_owner.employee_code)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_owners",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_asset_owner.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new asset_owner: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_asset_owner.created_at = datetime.now()
        new_asset_owner.updated_at = new_asset_owner.created_at        
        
        db.add(new_asset_owner)
        db.commit()
        db.refresh(new_asset_owner)
        return new_asset_owner
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset_owners(db: Session, asset_owners: List[AssetOwnerModel]) -> List[AssetOwner]:
    try:
        new_asset_owners = []
        # Prepare payload for batch UUID generation
        items = []
        for asset_owner in asset_owners:
            unique_data = str(asset_owner.client_id) + str(asset_owner.employee_code)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_owners",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to asset_owners
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(asset_owners):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_asset_owners = []
        for asset_owner, uuid_item in zip(asset_owners, uuid_items):
            # Convert AssetOwnerModel to a dictionary and add the generated UUID
            asset_owner_dict = asset_owner.model_dump()
            asset_owner_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            asset_owner_dict['created_at'] = datetime.now()
            asset_owner_dict['updated_at'] = asset_owner_dict['created_at']
            
            
            # Create AssetOwner instance with the new id and add to list
            new_asset_owner = AssetOwner(**asset_owner_dict)
            new_asset_owners.append(new_asset_owner)
        
        #Add new asset_owners to database
        db.add_all(new_asset_owners)
        db.commit()
        for new_asset_owner in new_asset_owners:
            db.refresh(new_asset_owner)
        return new_asset_owners
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise