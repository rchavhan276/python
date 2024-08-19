from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.action_type_hierarchy_crud import get_action_type_hierarchies, get_action_type_hierarchy_by_id, create_action_type_hierarchy, create_action_type_hierarchies
from ...schemas.action_type_hierarchy_schema import ActionTypeHierarchyModel, AddActionTypeHierarchyModel

router = APIRouter()

@router.get("/action_type_hierarchies/all", response_model=List[ActionTypeHierarchyModel])
def get_all_action_type_hierarchies(db: Session = Depends(get_db)):
    action_type_hierarchies = get_action_type_hierarchies(db)
    if not action_type_hierarchies:
        raise HTTPException(status_code=404, detail="Action Type Hierarchies not found")
    return action_type_hierarchies

@router.get("/action_type_hierarchies/{id}", response_model=ActionTypeHierarchyModel)
def get_action_type_hierarchy_by_uuid(id: UUID, db: Session = Depends(get_db)):
    action_type_hierarchy = get_action_type_hierarchy_by_id(db, id)
    if not action_type_hierarchy:
        raise HTTPException(status_code=404, detail="Action Type Hierarchy not found")
    return action_type_hierarchy

@router.post("/action_type_hierarchies/single", response_model=ActionTypeHierarchyModel)
def create_a_new_action_type_hierarchy(action_type_hierarchy: AddActionTypeHierarchyModel, db: Session = Depends(get_db)):
    new_action_type_hierarchy = create_action_type_hierarchy(db, action_type_hierarchy)
    if not new_action_type_hierarchy:
        raise HTTPException(status_code=500, detail="Error creating new action type hierarchy")
    return new_action_type_hierarchy

@router.post("/action_type_hierarchies/multi", response_model=List[ActionTypeHierarchyModel])
def create_multiple_new_action_type_hierarchies(action_type_hierarchies: List[AddActionTypeHierarchyModel], db: Session = Depends(get_db)):
    new_action_type_hierarchies = create_action_type_hierarchies(db, action_type_hierarchies)
    if not new_action_type_hierarchies:
        raise HTTPException(status_code=500, detail="Error creating new action type hierarchies")
    return new_action_type_hierarchies