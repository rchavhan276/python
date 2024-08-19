from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.category_hierarchy_crud import get_category_hierarchies, get_category_hierarchy_by_id, create_category_hierarchy, create_category_hierarchies
from ...schemas.category_hierarchy_schema import CategoryHierarchyModel, AddCategoryHierarchyModel

router = APIRouter()

@router.get("/category_hierarchies/all", response_model=List[CategoryHierarchyModel])
def get_all_category_hierarchies(db: Session = Depends(get_db)):
    category_hierarchies = get_category_hierarchies(db)
    if not category_hierarchies:
        raise HTTPException(status_code=404, detail="Category hierarchies not found")
    return category_hierarchies

@router.get("/category_hierarchies/{id}", response_model=CategoryHierarchyModel)
def get_category_hierarchy_by_uuid(id: UUID, db: Session = Depends(get_db)):
    category_hierarchy = get_category_hierarchy_by_id(db, id)
    if not category_hierarchy:
        raise HTTPException(status_code=404, detail="Category hierarchy not found")
    return category_hierarchy

@router.post("/category_hierarchies/single", response_model=CategoryHierarchyModel)
def create_a_new_category_hierarchy(category_hierarchy: AddCategoryHierarchyModel, db: Session = Depends(get_db)):
    new_category_hierarchy = create_category_hierarchy(db, category_hierarchy)
    if not new_category_hierarchy:
        raise HTTPException(status_code=500, detail="Error creating new category hierarchy")
    return new_category_hierarchy

@router.post("/category_hierarchies/multi", response_model=List[CategoryHierarchyModel])
def create_multiple_new_category_hierarchies(category_hierarchies: List[AddCategoryHierarchyModel], db: Session = Depends(get_db)):
    new_category_hierarchies = create_category_hierarchies(db, category_hierarchies)
    if not new_category_hierarchies:
        raise HTTPException(status_code=500, detail="Error creating new category hierarchies")
    return new_category_hierarchies