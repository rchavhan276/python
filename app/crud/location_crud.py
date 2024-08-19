import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.location_model import Location
from ..schemas.location_schema import LocationModel
from ..models.project_location_model import ProjectLocation

# Standard CRUD

def get_locations(db: Session) -> List[Location]:
    try:
        return db.query(Location).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_location_by_id(db: Session, id: UUID ) -> Union[Location, None]:
    try:
        return db.query(Location).filter(Location.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_location(db: Session, location: LocationModel) -> Location:
    try:
        new_location = Location(**location.model_dump())
        # Generate UUID for new location
        unique_data = str(new_location.client_id) + str(new_location.location_code)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}locations",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_location.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new location: {response.json()}")
        
        #Convert geo-coordinates to required format
        if new_location.geo_coordinates:
            lat = new_location.geo_coordinates["latitude"]
            lon = new_location.geo_coordinates["longitude"]
            new_location.geo_coordinates = f"({lat},{lon})"
        else:
            new_location.geo_coordinates = None
        
        # Add created_at and updated_at timestamp fields
        new_location.created_at = datetime.now()
        new_location.updated_at = new_location.created_at

        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        return new_location
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise    
        
def create_locations(db: Session, locations: List[LocationModel]) -> List[Location]:
    try:
        new_locations = []
        # Prepare payload for batch UUID generation
        items = []
        for location in locations:
            unique_data = str(location.client_id) + str(location.location_code)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}locations",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to locations
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(locations):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_locations = []
        for location, uuid_item in zip(locations, uuid_items):
            # Convert LocationModel to a dictionary and add the generated UUID
            location_dict = location.model_dump()
            location_dict['id'] = uuid_item.get('uuid')

            # Convert geo-coordinates to required format
            if isinstance(location_dict.get('geo_coordinates'), dict):
                lat = location_dict["geo_coordinates"]["latitude"]
                lon = location_dict["geo_coordinates"]["longitude"]
                location_dict["geo_coordinates"] = f"({lat},{lon})"
            else:
                location_dict["geo_coordinates"] = None
            
            # Add created_at and updated_at timestamp fields
            location_dict['created_at'] = datetime.now()
            location_dict['updated_at'] = location_dict['created_at']
            
            
            # Create Location instance with the new id and add to list
            new_location = Location(**location_dict)
            new_locations.append(new_location)
        
        #Add new locations to database
        db.add_all(new_locations)
        db.commit()
        for new_location in new_locations:
            db.refresh(new_location)
        return new_locations
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
def get_locations_by_client_id(db: Session, client_id: UUID) -> List[Location]:
    try:
        return db.query(Location).filter(Location.client_id == client_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_locations_by_location_code(db: Session, location_code: str) -> Union[Location, None]:
    try:
        return db.query(Location).filter(Location.location_code == location_code).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_locations_by_location_name(db: Session, location_name: str) -> Union[Location, None]:
    try:
        return db.query(Location).filter(Location.location_name == location_name).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_locations_by_location_type(db: Session, location_type: str) -> List[Location]:
    try:
        return db.query(Location).filter(Location.location_type == location_type).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

# Get locations associated with a project (join on projects_locations table)
def get_locations_by_project_id(db: Session, project_id: UUID) -> List[Location]:
    try:
        return db.query(Location).join(ProjectLocation).filter(ProjectLocation.project_id == project_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise


        