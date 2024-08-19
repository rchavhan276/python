from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.project_location_crud import get_projects_locations, get_project_location_by_id, create_project_location, create_projects_locations
from ...schemas.project_location_schema import ProjectLocationModel, AddProjectLocationModel

router = APIRouter()

@router.get("/projects_locations/all", response_model=List[ProjectLocationModel])
def get_all_projects_locations(db: Session = Depends(get_db)):
    projects_locations = get_projects_locations(db)
    if not projects_locations:
        raise HTTPException(status_code=404, detail="Category System relationships not found")
    return projects_locations

@router.get("/projects_locations/{id}", response_model=ProjectLocationModel)
def get_project_location_by_uuid(id: UUID, db: Session = Depends(get_db)):
    project_location = get_project_location_by_id(db, id)
    if not project_location:
        raise HTTPException(status_code=404, detail="Category System relationship not found")
    return project_location

@router.post("/projects_locations/single", response_model=ProjectLocationModel)
def create_a_new_project_location(project_location: AddProjectLocationModel, db: Session = Depends(get_db)):
    new_project_location = create_project_location(db, project_location)
    if not new_project_location:
        raise HTTPException(status_code=500, detail="Error creating new Category System relationship")
    return new_project_location

@router.post("/projects_locations/multi", response_model=List[ProjectLocationModel])
def create_multiple_new_projects_locations(projects_locations: List[AddProjectLocationModel], db: Session = Depends(get_db)):
    new_projects_locations = create_projects_locations(db, projects_locations)
    if not new_projects_locations:
        raise HTTPException(status_code=500, detail="Error creating new Category System relationships")
    return new_projects_locations