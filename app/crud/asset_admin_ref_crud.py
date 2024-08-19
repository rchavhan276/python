import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.asset_admin_ref_model import AssetAdminRef
from ..schemas.asset_admin_ref_schema import AssetAdminRefModel

def get_asset_admin_refs(db: Session) -> List[AssetAdminRef]:
    try:
        return db.query(AssetAdminRef).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_admin_ref_by_id(db: Session, id: UUID ) -> Union[AssetAdminRef, None]:
    try:
        return db.query(AssetAdminRef).filter(AssetAdminRef.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise
    
def create_asset_admin_ref(db: Session, asset_admin_ref: AssetAdminRefModel) -> AssetAdminRef:
    try:
        new_asset_admin_ref = AssetAdminRef(**asset_admin_ref.model_dump())
        # Generate UUID for new asset_admin_ref
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        unique_data = str(asset_admin_ref.asset_id) + str(asset_admin_ref.device_class_id) + now_str
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_administrative_ref",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_asset_admin_ref.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new asset_admin_ref: {response.json()}")
                
        # Add created_at and updated_at timestamp fields
        new_asset_admin_ref.created_at = datetime.now()
        new_asset_admin_ref.updated_at = new_asset_admin_ref.created_at
        
        db.add(new_asset_admin_ref)
        db.commit()
        db.refresh(new_asset_admin_ref)
        return new_asset_admin_ref
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise    
        
def create_asset_admin_refs(db: Session, asset_admin_refs: List[AssetAdminRefModel]) -> List[AssetAdminRef]:
    try:
        new_asset_admin_refs = []
        # Prepare payload for batch UUID generation
        items = []
        for asset_admin_ref in asset_admin_refs:
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d %H:%M:%S")
            unique_data = str(asset_admin_ref.asset_id) + str(asset_admin_ref.device_class_id) + now_str
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_administrative_ref",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to asset_admin_ref admin refs
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(asset_admin_refs):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_asset_admin_refs = []
        for asset_admin_ref, uuid_item in zip(asset_admin_refs, uuid_items):
            # Convert AssetAdminRefModel to a dictionary and add the generated UUID
            asset_admin_ref_dict = asset_admin_ref.model_dump()
            asset_admin_ref_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            asset_admin_ref_dict['created_at'] = datetime.now()
            asset_admin_ref_dict['updated_at'] = asset_admin_ref_dict['created_at']
            
            # Create AssetAdminRef Admin Ref instance with the new id and add to list
            new_asset_admin_ref = AssetAdminRef(**asset_admin_ref_dict)
            new_asset_admin_refs.append(new_asset_admin_ref)
        
        #Add new asset_admin_ref admin refs to database
        db.add_all(new_asset_admin_refs)
        db.commit()
        for new_asset_admin_ref in new_asset_admin_refs:
            db.refresh(new_asset_admin_ref)
        return new_asset_admin_refs
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise