from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .asset_model import Asset


Base = declarative_base()

class AssetHierarchy(Base):
    __tablename__ = 'asset_hierarchy'

    id = Column(UUID , primary_key=True)
    parent_asset_id = Column(UUID, ForeignKey(Asset.id))
    child_asset_id = Column(UUID, ForeignKey(Asset.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')