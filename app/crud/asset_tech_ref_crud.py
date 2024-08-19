import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.asset_tech_ref_model import AssetTechRef
from ..schemas.asset_tech_ref_schema import AssetTechRefModel

def get_asset_tech_refs(db: Session) -> List[AssetTechRef]:
    try:
        return db.query(AssetTechRef).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_tech_ref_by_id(db: Session, id: UUID ) -> Union[AssetTechRef, None]:
    try:
        return db.query(AssetTechRef).filter(AssetTechRef.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

# New CRUP OP for SOP SVC
def get_asset_tech_ref_by_asset_id(db: Session, asset_id: UUID ) -> Union[AssetTechRef, None]:
    try:
        return db.query(AssetTechRef).filter(AssetTechRef.asset_id == asset_id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

    
def create_asset_tech_ref(db: Session, asset_tech_ref: AssetTechRefModel) -> AssetTechRef:
    try:
        new_asset_tech_ref = AssetTechRef(**asset_tech_ref.model_dump())
        # Generate UUID for new asset_tech_ref
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        unique_data = str(asset_tech_ref.asset_id) + str(asset_tech_ref.device_class_id) + now_str
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_technical_ref",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_asset_tech_ref.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new asset_tech_ref: {response.json()}")
                
        # Add created_at and updated_at timestamp fields
        new_asset_tech_ref.created_at = datetime.now()
        new_asset_tech_ref.updated_at = new_asset_tech_ref.created_at
        
        db.add(new_asset_tech_ref)
        db.commit()
        db.refresh(new_asset_tech_ref)
        return new_asset_tech_ref
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise    
        
def create_asset_tech_refs(db: Session, asset_tech_refs: List[AssetTechRefModel]) -> List[AssetTechRef]:
    try:
        new_asset_tech_refs = []
        # Prepare payload for batch UUID generation
        items = []
        for asset_tech_ref in asset_tech_refs:
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d %H:%M:%S")
            unique_data = str(asset_tech_ref.asset_id) + str(asset_tech_ref.device_class_id) + now_str
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}asset_technical_ref",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to asset_tech_ref tech refs
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(asset_tech_refs):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_asset_tech_refs = []
        for asset_tech_ref, uuid_item in zip(asset_tech_refs, uuid_items):
            # Convert AssetTechRefModel to a dictionary and add the generated UUID
            asset_tech_ref_dict = asset_tech_ref.model_dump()
            asset_tech_ref_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            asset_tech_ref_dict['created_at'] = datetime.now()
            asset_tech_ref_dict['updated_at'] = asset_tech_ref_dict['created_at']

            # Create AssetTechRef Tech Ref instance with the new id and add to list
            new_asset_tech_ref = AssetTechRef(**asset_tech_ref_dict)
            new_asset_tech_refs.append(new_asset_tech_ref)
        
        #Add new asset_tech_ref tech refs to database
        db.add_all(new_asset_tech_refs)
        db.commit()
        for new_asset_tech_ref in new_asset_tech_refs:
            db.refresh(new_asset_tech_ref)
        return new_asset_tech_refs
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise