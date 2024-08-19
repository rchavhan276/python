from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from ..config import settings
from ..models.asset_summary_model import AssetSummary
from ..schemas.asset_summary_schema import AssetSummaryModel

# Standard CRUD

def get_asset_summary(db: Session) -> List[AssetSummary]:
    try:
        return db.query(AssetSummary).all()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise

def get_asset_summary_by_asset_tag(db: Session, asset_tag: str) -> Union[AssetSummary, None]:
    try:
        return db.query(AssetSummary).filter(AssetSummary.asset_tag == asset_tag).first()
    except exc.SQLAlchemyError as e:
        print(f"SQL Alchemy Error: {e}")
        raise
    except Exception as e:
        print(e)
        raise
