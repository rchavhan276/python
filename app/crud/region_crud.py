import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.region_model import Region
from ..schemas.region_schema import RegionModel

def get_regions(db: Session) -> List[Region]:
    try:
        return db.query(Region).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_region_by_id(db: Session, id: UUID ) -> Union[Region, None]:
    try:
        return db.query(Region).filter(Region.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise
    
def create_region(db: Session, region: RegionModel) -> Region:
    try:
        new_region = Region(**region.model_dump())
        # Generate UUID for new region
        unique_data = str(new_region.region_code)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}regions",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_region.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new region: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_region.created_at = datetime.now()
        new_region.updated_at = new_region.created_at        
        
        db.add(new_region)
        db.commit()
        db.refresh(new_region)
        return new_region
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_regions(db: Session, regions: List[RegionModel]) -> List[Region]:
    try:
        new_regions = []
        # Prepare payload for batch UUID generation
        items = []
        for region in regions:
            unique_data = str(region.region_code)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}regions",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()
        
        # Map generated UUIDs to regions
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(regions):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_regions = []
        for region, uuid_item in zip(regions, uuid_items):
            # Convert RegionModel to a dictionary and add the generated UUID
            region_dict = region.model_dump()
            region_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            region_dict['created_at'] = datetime.now()
            region_dict['updated_at'] = region_dict['created_at']

            # Create Region instance with the new id and add to list
            new_region = Region(**region_dict)
            new_regions.append(new_region)
        
        # Add new regions to database
        db.add_all(new_regions)
        db.commit()
        # Refresh each new region from the database
        for new_region in new_regions:
            db.refresh(new_region)
        return new_regions
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise     