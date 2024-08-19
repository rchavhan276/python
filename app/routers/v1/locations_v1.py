from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.location_crud import get_locations, get_location_by_id, create_location, create_locations, get_locations_by_client_id, get_locations_by_location_code, get_locations_by_location_name, get_locations_by_location_type, get_locations_by_project_id
from ...schemas.location_schema import LocationModel, AddLocationModel

router = APIRouter()

# Standard Routers

@router.get("/locations/all", response_model=List[LocationModel])
def get_all_locations(db: Session = Depends(get_db)):
    locations = get_locations(db)
    if not locations:
        raise HTTPException(status_code=404, detail="Locations not found")
    return locations

@router.get("/locations/{id}", response_model=LocationModel)
def get_location_by_uuid(id: UUID, db: Session = Depends(get_db)):
    location = get_location_by_id(db, id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.post("/locations/single", response_model=LocationModel)
def create_a_new_location(location: AddLocationModel, db: Session = Depends(get_db)):
    new_location = create_location(db, location)
    if not new_location:
        raise HTTPException(status_code=500, detail="Error creating new location")
    return new_location

@router.post("/locations/multi", response_model=List[LocationModel])
def create_multiple_new_locations(locations: List[AddLocationModel], db: Session = Depends(get_db)):
    new_locations = create_locations(db, locations)
    if not new_locations:
        raise HTTPException(status_code=500, detail="Error creating new locations")
    return new_locations

# Specific Routers

@router.get("/locations/client/{client_id}", response_model=List[LocationModel])
def get_all_locations_for_client_id(client_id: UUID, db: Session = Depends(get_db)):
    locations = get_locations_by_client_id(db, client_id)
    if not locations:
        raise HTTPException(status_code=404, detail="Locations not found")
    return locations

@router.get("/locations/code/{location_code}", response_model=LocationModel)
def get_a_location_by_location_code(location_code: str, db: Session = Depends(get_db)):
    locations = get_locations_by_location_code(db, location_code)
    if not locations:
        raise HTTPException(status_code=404, detail="Locations not found")
    return locations

@router.get("/locations/name/{location_name}", response_model=LocationModel)
def get_a_location_by_location_name(location_name: str, db: Session = Depends(get_db)):
    locations = get_locations_by_location_name(db, location_name)
    if not locations:
        raise HTTPException(status_code=404, detail="Locations not found")
    return locations

@router.get("/locations/type/{location_type}", response_model=List[LocationModel])
def get_all_locations_by_location_type(location_type: str, db: Session = Depends(get_db)):
    locations = get_locations_by_location_type(db, location_type)
    if not locations:
        raise HTTPException(status_code=404, detail="Locations not found")
    return locations

# Get locations associated with a project (join on projects_locations table)
@router.get("/locations/project/{project_id}", response_model=List[LocationModel])
def get_all_locations_for_project_id(project_id: UUID, db: Session = Depends(get_db)):
    locations = get_locations_by_project_id(db, project_id)
    if not locations:
        raise HTTPException(status_code=404, detail="Locations not found")
    return locations