from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from ...dependencies import get_db
from ...crud.project_crud import get_projects, get_project_by_id, create_project, create_projects, get_projects_by_client_id, get_project_by_project_code, get_project_by_project_name
from ...schemas.project_schema import ProjectModel, AddProjectModel

router = APIRouter()

# Standard Routers

@router.get("/projects/all", response_model=List[ProjectModel])
def get_all_projects(db: Session = Depends(get_db)):
    projects = get_projects(db)
    if not projects:
        raise HTTPException(status_code=404, detail="Projects not found")
    return projects

@router.get("/projects/{id}", response_model=ProjectModel)
def get_project_by_uuid(id: UUID, db: Session = Depends(get_db)):
    project = get_project_by_id(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/projects/single", response_model=ProjectModel)
def create_a_new_project(project: AddProjectModel, db: Session = Depends(get_db)):
    new_project = create_project(db, project)
    if not new_project:
        raise HTTPException(status_code=500, detail="Error creating new project")
    return new_project

@router.post("/projects/multi", response_model=List[ProjectModel])
def create_multiple_new_projects(projects: List[AddProjectModel], db: Session = Depends(get_db)):
    new_projects = create_projects(db, projects)
    if not new_projects:
        raise HTTPException(status_code=500, detail="Error creating new projects")
    return new_projects

# Specific Routers

@router.get("/projects/client/{client_id}", response_model=List[ProjectModel])
def get_all_projects_for_client_id(client_id: UUID, db: Session = Depends(get_db)):
    print(client_id)
    projects = get_projects_by_client_id(db, client_id)
    if not projects:
        raise HTTPException(status_code=404, detail="Projects not found")
    return projects

@router.get("/projects/code/{project_code}", response_model=ProjectModel)
def get_all_projects_by_project_code(project_code: str, db: Session = Depends(get_db)):
    projects = get_project_by_project_code(db, project_code)
    if not projects:
        raise HTTPException(status_code=404, detail="Projects not found")
    return projects


@router.get("/projects/name/{project_name}", response_model=ProjectModel)
def get_all_projects_by_project_name(project_name: str, db: Session = Depends(get_db)):
    projects = get_project_by_project_name(db, project_name)
    if not projects:
        raise HTTPException(status_code=404, detail="Projects not found")
    return projects