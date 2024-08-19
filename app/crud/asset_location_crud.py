from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List
from ..models.asset_location_model import AssetLocation

# Standard CRUD

def get_asset_location(db: Session) -> List[AssetLocation]:
    try:
        return db.query(AssetLocation).all()
    except exc.SQLAlchemyError as e:
        raise Exception(str(e))
    except Exception as e:
        raise Exception(str(e))
