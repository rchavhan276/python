import requests
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from uuid import UUID
from ..config import settings
from ..models.country_model import Country
from ..schemas.country_schema import CountryModel

# Standard CRUD

def get_countries(db: Session) -> List[Country]:
    try:
        return db.query(Country).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_country_by_id(db: Session, id: UUID ) -> Union[Country, None]:
    try:
        return db.query(Country).filter(Country.id == id).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_country(db: Session, country: CountryModel) -> Country:
    try:
        new_country = Country(**country.model_dump())
        # Generate UUID for new country
        unique_data = str(new_country.country_code)
        payload = {
            "url": f"{settings.UUID_NAMESPACE_BASE_URL}countries",
            "unique_data": unique_data
        }
        response = requests.post(settings.UUID_URL, json=payload)
        if response.status_code == 200:
            new_country.id = response.json()["uuid"]
        else:
            raise Exception(f"Error generating UUID for new country: {response.json()}")
        
        # Add created_at and updated_at timestamp fields
        new_country.created_at = datetime.now()
        new_country.updated_at = new_country.created_at        
        
        db.add(new_country)
        db.commit()
        db.refresh(new_country)
        return new_country
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def create_countries(db: Session, countries: List[CountryModel]) -> List[Country]:
    try:
        new_countries = []
        # Prepare payload for batch UUID generation
        items = []
        for country in countries:
            unique_data = str(country.country_code)
            items.append({
                "url": f"{settings.UUID_NAMESPACE_BASE_URL}countries",
                "unique_data": unique_data
            })
        # Make batch UUID generation request
        payload = {
            "items": items
        }
        response = requests.post(settings.UUID_BATCH_URL, json=payload)
        response.raise_for_status()
        
        # Map generated UUIDs to countries
        uuid_items = response.json().get("items", [])
        if len(uuid_items) != len(countries):
            raise ValueError("Mismatch in number of UUIDs received from external service")
        new_countries = []
        for country, uuid_item in zip(countries, uuid_items):
            # Convert CountryModel to a dictionary and add the generated UUID
            country_dict = country.model_dump()
            country_dict['id'] = uuid_item.get('uuid')

            # Add created_at and updated_at timestamp fields
            country_dict['created_at'] = datetime.now()
            country_dict['updated_at'] = country_dict['created_at']

            # Create Country instance with the new id and add to list
            new_country = Country(**country_dict)
            new_countries.append(new_country)
        
        # Add new countries to database
        db.add_all(new_countries)
        db.commit()
        # Refresh each new country from the database
        for new_country in new_countries:
            db.refresh(new_country)
        return new_countries
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

def get_countries_by_region_id(db: Session, region_id: UUID) -> List[Country]:
    try:
        return db.query(Country).filter(Country.region_id == region_id).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise