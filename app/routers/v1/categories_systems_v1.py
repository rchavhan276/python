from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.category_system_crud import get_categories_systems, get_category_system_by_id, create_category_system, create_categories_systems
from ...schemas.category_system_schema import CategorySystemModel, AddCategorySystemModel

router = APIRouter()

@router.get("/categories_systems/all", response_model=List[CategorySystemModel])
def get_all_categories_systems(db: Session = Depends(get_db)):
    categories_systems = get_categories_systems(db)
    if not categories_systems:
        raise HTTPException(status_code=404, detail="Category System relationships not found")
    return categories_systems

@router.get("/categories_systems/{id}", response_model=CategorySystemModel)
def get_category_system_by_uuid(id: UUID, db: Session = Depends(get_db)):
    category_system = get_category_system_by_id(db, id)
    if not category_system:
        raise HTTPException(status_code=404, detail="Category System relationship not found")
    return category_system

@router.post("/categories_systems/single", response_model=CategorySystemModel)
def create_a_new_category_system(category_system: AddCategorySystemModel, db: Session = Depends(get_db)):
    new_category_system = create_category_system(db, category_system)
    if not new_category_system:
        raise HTTPException(status_code=500, detail="Error creating new Category System relationship")
    return new_category_system

@router.post("/categories_systems/multi", response_model=List[CategorySystemModel])
def create_multiple_new_categories_systems(categories_systems: List[AddCategorySystemModel], db: Session = Depends(get_db)):
    new_categories_systems = create_categories_systems(db, categories_systems)
    if not new_categories_systems:
        raise HTTPException(status_code=500, detail="Error creating new Category System relationships")
    return new_categories_systems