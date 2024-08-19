from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...crud.client_crud import get_clients, get_client_by_id, create_client, create_clients, get_client_by_client_code, get_client_by_client_name
from ...schemas.client_schema import ClientModel, AddClientModel


router = APIRouter()

# Stadard Routes

@router.get("/clients/all", response_model=List[ClientModel])
def get_all_clients(db: Session = Depends(get_db)):
    clients = get_clients(db)
    if not clients:
        raise HTTPException(status_code=404, detail="Clients not found")
    return clients

@router.get("/clients/{id}", response_model=ClientModel)
def get_client_by_uuid(id: UUID, db: Session = Depends(get_db)):
    client = get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/clients/single", response_model=ClientModel)
def create_a_new_client(client: AddClientModel, db: Session = Depends(get_db)):
    new_client = create_client(db, client)
    if not new_client:
        raise HTTPException(status_code=500, detail="Error creating new client")
    return new_client

@router.post("/clients/multi", response_model=List[ClientModel])
def create_multiple_new_clients(clients: List[AddClientModel], db: Session = Depends(get_db)):
    new_clients = create_clients(db, clients)
    if not new_clients:
        raise HTTPException(status_code=500, detail="Error creating new clients")
    return new_clients

# Specific Routes

@router.get("/clients/code/{client_code}", response_model=ClientModel)
def get_a_client_by_client_code(client_code: str, db: Session = Depends(get_db)):
    client = get_client_by_client_code(db, client_code)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/clients/name/{client_name}", response_model=ClientModel)
def get_a_client_by_client_name(client_name: str, db: Session = Depends(get_db)):
    client = get_client_by_client_name(db, client_name)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client