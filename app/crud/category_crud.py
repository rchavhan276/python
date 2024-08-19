import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.category_model import Category
from ..schemas.category_schema import CategoryModel

# Standard CRUD

def get_categories(db: Session) -> List[Category]:
    try:
        return db.query(Category).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_category_by_id(db: Session, id: UUID ) -> Union[Category, None]:
    try:
        return db.query(Category).filter(Category.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_category(db: Session, category: CategoryModel) -> Category:
    try:
        new_category = Category(**category.model_dump())
        # Generate UUID for new category
        unique_data = str(new_category.category_name)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}categories",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_category.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new category: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_category.created_at = datetime.now()
        new_category.updated_at = new_category.created_at        
        
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_categories(db: Session, categories: List[CategoryModel]) -> List[Category]:
    try:
        new_categories = []
        # Prepare payload for batch UUID generation
        items = []
        for category in categories:
            unique_data = str(category.category_name)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}categories",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()

        # Map generated UUIDs to categories
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(categories):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_categories = []
        for category, uuid_item in zip(categories, uuid_items):
            # Convert CategoryModel to a dictionary and add the generated UUID
            category_dict = category.model_dump()
            category_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            category_dict['created_at'] = datetime.now()
            category_dict['updated_at'] = category_dict['created_at']
            
            
            # Create Category instance with the new id and add to list
            new_category = Category(**category_dict)
            new_categories.append(new_category)
        
        #Add new categories to database
        db.add_all(new_categories)
        db.commit()
        for new_category in new_categories:
            db.refresh(new_category)
        return new_categories
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

def get_category_by_name(db: Session, category_name: str) -> Union[Category, None]:
    try:
        return db.query(Category).filter(Category.category_name == category_name).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise