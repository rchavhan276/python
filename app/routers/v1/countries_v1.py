from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.country_crud import get_countries, get_country_by_id, create_country, create_countries, get_countries_by_region_id
from ...schemas.country_schema import CountryModel, AddCountryModel

router = APIRouter()

# Stadard Routes

@router.get("/countries/all", response_model=List[CountryModel])
def get_all_countries(db: Session = Depends(get_db)):
    countries = get_countries(db)
    if not countries:
        raise HTTPException(status_code=404, detail="Countries not found")
    return countries

@router.get("/countries/{id}", response_model=CountryModel)
def get_country_by_uuid(id: UUID, db: Session = Depends(get_db)):
    country = get_country_by_id(db, id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@router.post("/countries/single", response_model=CountryModel)
def create_a_new_country(country: AddCountryModel, db: Session = Depends(get_db)):
    new_country = create_country(db, country)
    if not new_country:
        raise HTTPException(status_code=500, detail="Error creating new country")
    return new_country

@router.post("/countries/multi", response_model=List[CountryModel])
def create_multiple_new_countries(countries: List[AddCountryModel], db: Session = Depends(get_db)):
    new_countries = create_countries(db, countries)
    if not new_countries:
        raise HTTPException(status_code=500, detail="Error creating new countries")
    return new_countries

# Specific Routes

@router.get("/countries/region/{region_id}", response_model=List[CountryModel])
def get_all_countries_by_region(region_id: UUID, db: Session = Depends(get_db)):
    countries = get_countries_by_region_id(db, region_id)
    if not countries:
        raise HTTPException(status_code=404, detail="Countries not found")
    return countries