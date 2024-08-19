import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.client_model import Client
from ..schemas.client_schema import ClientModel

# Standard CRUD

def get_clients(db: Session) -> List[Client]:
    try:
        return db.query(Client).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_client_by_id(db: Session, id: UUID ) -> Union[Client, None]:
    try:
        return db.query(Client).filter(Client.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise
    
def create_client(db: Session, client: ClientModel) -> Client:
    try:
        new_client = Client(**client.model_dump())
        # Generate UUID for new client
        unique_data = str(new_client.client_code)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}clients",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_client.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new client: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_client.created_at = datetime.now()
        new_client.updated_at = new_client.created_at        
        
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_clients(db: Session, clients: List[ClientModel]) -> List[Client]:
    try:
        new_clients = []
        # Prepare payload for batch UUID generation
        items = []
        for client in clients:
            unique_data = str(client.client_code)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}clients",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()
        
        # Map generated UUIDs to clients
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(clients):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_clients = []
        for client, uuid_item in zip(clients, uuid_items):
            # Convert ClientModel to a dictionary and add the generated UUID
            client_dict = client.model_dump()
            client_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            client_dict['created_at'] = datetime.now()
            client_dict['updated_at'] = client_dict['created_at']

            # Create Client instance with the new id and add to list
            new_client = Client(**client_dict)
            new_clients.append(new_client)
        
        # Add new clients to database
        db.add_all(new_clients)
        db.commit()
        # Refresh each new client from the database
        for new_client in new_clients:
            db.refresh(new_client)
        return new_clients
    except requests.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        raise
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

# Specific CRUD

def get_client_by_client_code(db: Session, client_code: str) -> Union[Client, None]:
    try:
        return db.query(Client).filter(Client.client_code == client_code).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_client_by_client_name(db: Session, client_name: str) -> Union[Client, None]:
    try:
        return db.query(Client).filter(Client.client_name == client_name).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise




        