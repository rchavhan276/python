import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.project_location_model import ProjectLocation
from ..schemas.project_location_schema import ProjectLocationModel

def get_projects_locations(db: Session) -> List[ProjectLocation]:
    try:
        return db.query(ProjectLocation).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_project_location_by_id(db: Session, id: UUID ) -> Union[ProjectLocation, None]:
    try:
        return db.query(ProjectLocation).filter(ProjectLocation.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_project_location(db: Session, project_location: ProjectLocationModel) -> ProjectLocation:
    try:
        new_project_location = ProjectLocation(**project_location.model_dump())
        # Generate UUID for new project_location
        unique_data = str(new_project_location.project_id) + str(new_project_location.location_id)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}projects_locations",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_project_location.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new project_location: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_project_location.created_at = datetime.now()
        new_project_location.updated_at = new_project_location.created_at        
        
        db.add(new_project_location)
        db.commit()
        db.refresh(new_project_location)
        return new_project_location
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_projects_locations(db: Session, projects_locations: List[ProjectLocationModel]) -> List[ProjectLocation]:
    try:
        new_projects_locations = []
        # Prepare payload for batch UUID generation
        items = []
        for project_location in projects_locations:
            unique_data = str(project_location.project_id) + str(project_location.location_id)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}projects_locations",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to project_locations
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(projects_locations):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_projects_locations = []
        for project_location, uuid_item in zip(projects_locations, uuid_items):
            # Convert ProjectLocationModel to a dictionary and add the generated UUID
            project_location_dict = project_location.model_dump()
            project_location_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            project_location_dict['created_at'] = datetime.now()
            project_location_dict['updated_at'] = project_location_dict['created_at']
            
            
            # Create ProjectLocation instance with the new id and add to list
            new_project_location = ProjectLocation(**project_location_dict)
            new_projects_locations.append(new_project_location)
        
        #Add new project_locations to database
        db.add_all(new_projects_locations)
        db.commit()
        for new_project_location in new_projects_locations:
            db.refresh(new_project_location)
        return new_projects_locations
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise