import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.lcm_source_model import LcmSource
from ..schemas.lcm_source_schema import LcmSourceModel

def get_lcm_sources(db: Session) -> List[LcmSource]:
    try:
        return db.query(LcmSource).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_lcm_source_by_id(db: Session, id: UUID ) -> Union[LcmSource, None]:
    try:
        return db.query(LcmSource).filter(LcmSource.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_lcm_source(db: Session, lcm_source: LcmSourceModel) -> LcmSource:
    try:
        new_lcm_source = LcmSource(**lcm_source.model_dump())
        # Generate UUID for new lcm_source
        unique_data = ""
        payload = {
            "url": f"{new_lcm_source.namespace}",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_lcm_source.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new lcm_source: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_lcm_source.created_at = datetime.now()
        new_lcm_source.updated_at = new_lcm_source.created_at        
        
        db.add(new_lcm_source)
        db.commit()
        db.refresh(new_lcm_source)
        return new_lcm_source
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_lcm_sources(db: Session, lcm_sources: List[LcmSourceModel]) -> List[LcmSource]:
    try:
        new_lcm_sources = []
        # Prepare payload for batch UUID generation
        items = []
        for lcm_source in lcm_sources:
            unique_data = ""
            items.append({
                "url": f"{lcm_source.namespace}",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to lcm_sources
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(lcm_sources):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_lcm_sources = []
        for lcm_source, uuid_item in zip(lcm_sources, uuid_items):
            # Convert LcmSourceModel to a dictionary and add the generated UUID
            lcm_source_dict = lcm_source.model_dump()
            lcm_source_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            lcm_source_dict['created_at'] = datetime.now()
            lcm_source_dict['updated_at'] = lcm_source_dict['created_at']
            
            
            # Create LcmSource instance with the new id and add to list
            new_lcm_source = LcmSource(**lcm_source_dict)
            new_lcm_sources.append(new_lcm_source)
        
        #Add new lcm_sources to database
        db.add_all(new_lcm_sources)
        db.commit()
        for new_lcm_source in new_lcm_sources:
            db.refresh(new_lcm_source)
        return new_lcm_sources
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise