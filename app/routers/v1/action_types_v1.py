from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.action_type_crud import get_action_types, get_action_type_by_id, create_action_type, create_action_types
from ...schemas.action_type_schema import ActionTypeModel, AddActionTypeModel

router = APIRouter()

@router.get("/action_types/all", response_model=List[ActionTypeModel])
def get_all_action_types(db: Session = Depends(get_db)):
    action_types = get_action_types(db)
    if not action_types:
        raise HTTPException(status_code=404, detail="Action Types not found")
    return action_types

@router.get("/action_types/{id}", response_model=ActionTypeModel)
def get_action_type_by_uuid(id: UUID, db: Session = Depends(get_db)):
    action_type = get_action_type_by_id(db, id)
    if not action_type:
        raise HTTPException(status_code=404, detail="Action Type not found")
    return action_type

@router.post("/action_types/single", response_model=ActionTypeModel)
def create_a_new_action_type(action_type: AddActionTypeModel, db: Session = Depends(get_db)):
    new_action_type = create_action_type(db, action_type)
    if not new_action_type:
        raise HTTPException(status_code=500, detail="Error creating new action type")
    return new_action_type

@router.post("/action_types/multi", response_model=List[ActionTypeModel])
def create_multiple_new_action_types(action_types: List[AddActionTypeModel], db: Session = Depends(get_db)):
    new_action_types = create_action_types(db, action_types)
    if not new_action_types:
        raise HTTPException(status_code=500, detail="Error creating new action types")
    return new_action_types