import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.asset_model import Asset
from ..schemas.asset_schema import AssetModel

# Standard CRUD

def get_assets(db: Session) -> List[Asset]:
    try:
        return db.query(Asset).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_by_id(db: Session, id: UUID ) -> Union[Asset, None]:
    try:
        return db.query(Asset).filter(Asset.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_asset(db: Session, asset: AssetModel) -> Asset:
    try:
        new_asset = Asset(**asset.model_dump())
        # Generate UUID for new asset
        unique_data = str(new_asset.client_id) + str(new_asset.project_id) + str(new_asset.location_id) + str(new_asset.asset_tag)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}assets",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_asset.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new asset: {response.json()}")
        
        #Convert geo-coordinates to required format
        if new_asset.geo_coordinates:
            lat = new_asset.geo_coordinates["latitude"]
            lon = new_asset.geo_coordinates["longitude"]
            new_asset.geo_coordinates = f"({lat},{lon})"
        else:
            new_asset.geo_coordinates = None
        
        # Add created_at and updated_at timestamp fields
        new_asset.created_at = datetime.now()
        new_asset.updated_at = new_asset.created_at

        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
        return new_asset
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise    
        
def create_assets(db: Session, assets: List[AssetModel]) -> List[Asset]:
    try:
        new_assets = []
        # Prepare payload for batch UUID generation
        items = []
        for asset in assets:
            unique_data = str(asset.client_id) + str(asset.project_id) + str(asset.location_id) + str(asset.asset_tag)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}assets",
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
        if len(uuid_items) != len(assets):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_assets = []
        for asset, uuid_item in zip(assets, uuid_items):
            # Convert AssetModel to a dictionary and add the generated UUID
            asset_dict = asset.model_dump()
            asset_dict['id'] = uuid_item.get('uuid')

            # Convert geo-coordinates to required format
            if isinstance(asset_dict.get('geo_coordinates'), dict):
                lat = asset_dict["geo_coordinates"]["latitude"]
                lon = asset_dict["geo_coordinates"]["longitude"]
                asset_dict["geo_coordinates"] = f"({lat},{lon})"
            else:
                asset_dict["geo_coordinates"] = None
            
            # Add created_at and updated_at timestamp fields
            asset_dict['created_at'] = datetime.now()
            asset_dict['updated_at'] = asset_dict['created_at']
            
            
            # Create Asset instance with the new id and add to list
            new_asset = Asset(**asset_dict)
            new_assets.append(new_asset)
        
        #Add new assets to database
        db.add_all(new_assets)
        db.commit()
        for new_asset in new_assets:
            try:
                db.refresh(new_asset)
            except Exception as e:
                print(f"Error refreshing client instance: {e}")
        return new_assets
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
def get_assets_by_client_id(db: Session, client_id: UUID) -> List[Asset]:
    try:
        return db.query(Asset).filter(Asset.client_id == client_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_assets_by_project_id(db: Session, project_id: UUID) -> List[Asset]:
    try:
        return db.query(Asset).filter(Asset.project_id == project_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_assets_by_location_id(db: Session, location_id: UUID) -> List[Asset]:
    try:
        return db.query(Asset).filter(Asset.location_id == location_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_assets_by_category_id(db: Session, category_id: UUID) -> List[Asset]:
    try:
        return db.query(Asset).filter(Asset.category_id == category_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e) 
        raise

def get_assets_by_system_id(db: Session, system_id: UUID) -> List[Asset]:
    try:
        return db.query(Asset).filter(Asset.system_id == system_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e: 
        print(e)
        raise

def get_assets_by_device_type_id(db: Session, device_type_id: UUID) -> List[Asset]:
    try:
        return db.query(Asset).filter(Asset.device_type_id == device_type_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e: 
        print(e)
        raise

def get_asset_by_asset_tag(db: Session, asset_tag: str) -> Union[Asset, None]:
    try:
        return db.query(Asset).filter(Asset.asset_tag == asset_tag).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise
    


        