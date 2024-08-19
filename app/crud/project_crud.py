import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.project_model import Project
from ..schemas.project_schema import ProjectModel

# Standard CRUD

def get_projects(db: Session) -> List[Project]:
    try:
        return db.query(Project).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_project_by_id(db: Session, id: UUID ) -> Union[Project, None]:
    try:
        return db.query(Project).filter(Project.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise
    
def create_project(db: Session, project: ProjectModel) -> Project:
    try:
        new_project = Project(**project.model_dump())
        # Generate UUID for new project
        unique_data = str(new_project.client_id) + str(new_project.project_code)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}projects",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_project.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new project: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_project.created_at = datetime.now()
        new_project.updated_at = new_project.created_at        
        
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_projects(db: Session, projects: List[ProjectModel]) -> List[Project]:
    try:
        new_projects = []
        # Prepare payload for batch UUID generation
        items = []
        for project in projects:
            unique_data = str(project.client_id) + str(project.project_code)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}projects",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()
        
        # Map generated UUIDs to projects
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(projects):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_projects = []
        for project, uuid_item in zip(projects, uuid_items):
            # Convert ProjectModel to a dictionary and add the generated UUID
            project_dict = project.model_dump()
            project_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            project_dict['created_at'] = datetime.now()
            project_dict['updated_at'] = project_dict['created_at']

            # Create Project instance with the new id and add to list
            new_project = Project(**project_dict)
            new_projects.append(new_project)
        
        # Add new projects to database
        db.add_all(new_projects)
        db.commit()
        # Refresh each new project from the database
        for new_project in new_projects:
            db.refresh(new_project)
        return new_projects
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
def get_projects_by_client_id(db: Session, client_id: UUID) -> List[Project]:
    try:
        return db.query(Project).filter(Project.client_id == client_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_project_by_project_code(db: Session, project_code: str) -> Union[Project, None]:
    try:
        return db.query(Project).filter(Project.project_code == project_code).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise


def get_project_by_project_name(db: Session, project_name: str) -> Union[Project, None]:
    try:
        return db.query(Project).filter(Project.project_name == project_name).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

        