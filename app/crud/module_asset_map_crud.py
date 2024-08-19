import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.module_asset_map_model import ModuleAssetMap
from ..schemas.module_asset_map_schema import ModuleAssetMapModel

def get_module_asset_maps(db: Session) -> List[ModuleAssetMap]:
    try:
        return db.query(ModuleAssetMap).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_module_asset_map_by_id(db: Session, id: UUID ) -> Union[ModuleAssetMap, None]:
    try:
        return db.query(ModuleAssetMap).filter(ModuleAssetMap.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_module_asset_map(db: Session, module_asset_map: ModuleAssetMapModel) -> ModuleAssetMap:
    try:
        new_module_asset_map = ModuleAssetMap(**module_asset_map.model_dump())
        # Generate UUID for new module_asset_map
        unique_data = str(new_module_asset_map.module_id) + str(new_module_asset_map.asset_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}module_asset_map",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_module_asset_map.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new module_asset_map: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_module_asset_map.created_at = datetime.now()
        new_module_asset_map.updated_at = new_module_asset_map.created_at        
        
        db.add(new_module_asset_map)
        db.commit()
        db.refresh(new_module_asset_map)
        return new_module_asset_map
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_module_asset_maps(db: Session, module_asset_maps: List[ModuleAssetMapModel]) -> List[ModuleAssetMap]:
    try:
        new_module_asset_maps = []
        # Prepare payload for batch UUID generation
        items = []
        for module_asset_map in module_asset_maps:
            unique_data = str(module_asset_map.module_id) + str(module_asset_map.asset_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}module_asset_map",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to module_asset_maps
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(module_asset_maps):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_module_asset_maps = []
        for module_asset_map, uuid_item in zip(module_asset_maps, uuid_items):
            # Convert ModuleAssetMapModel to a dictionary and add the generated UUID
            module_asset_map_dict = module_asset_map.model_dump()
            module_asset_map_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            module_asset_map_dict['created_at'] = datetime.now()
            module_asset_map_dict['updated_at'] = module_asset_map_dict['created_at']
            
            
            # Create ModuleAssetMap instance with the new id and add to list
            new_module_asset_map = ModuleAssetMap(**module_asset_map_dict)
            new_module_asset_maps.append(new_module_asset_map)
        
        #Add new module_asset_maps to database
        db.add_all(new_module_asset_maps)
        db.commit()
        for new_module_asset_map in new_module_asset_maps:
            db.refresh(new_module_asset_map)
        return new_module_asset_maps
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise