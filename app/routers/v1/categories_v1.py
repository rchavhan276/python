from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.category_crud import get_categories, get_category_by_id, create_category, create_categories, get_category_by_name
from ...schemas.category_schema import CategoryModel, AddCategoryModel

router = APIRouter()

# Standard Routes

@router.get("/categories/all", response_model=List[CategoryModel])
def get_all_categories(db: Session = Depends(get_db)):
    categories = get_categories(db)
    if not categories:
        raise HTTPException(status_code=404, detail="Categorys not found")
    return categories

@router.get("/categories/{id}", response_model=CategoryModel)
def get_category_by_uuid(id: UUID, db: Session = Depends(get_db)):
    category = get_category_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories/single", response_model=CategoryModel)
def create_a_new_category(category: AddCategoryModel, db: Session = Depends(get_db)):
    new_category = create_category(db, category)
    if not new_category:
        raise HTTPException(status_code=500, detail="Error creating new category")
    return new_category

@router.post("/categories/multi", response_model=List[CategoryModel])
def create_multiple_new_categories(categories: List[AddCategoryModel], db: Session = Depends(get_db)):
    new_categories = create_categories(db, categories)
    if not new_categories:
        raise HTTPException(status_code=500, detail="Error creating new categories")
    return new_categories

# Specific Routes

@router.get("/categories/name/{category_name}", response_model=CategoryModel)
def get_a_category_by_category_name(category_name: str, db: Session = Depends(get_db)):
    category = get_category_by_name(db, category_name)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category