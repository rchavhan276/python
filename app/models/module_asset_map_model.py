from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .lcm_source_model import LcmSource
from .asset_model import Asset


Base = declarative_base()

class ModuleAssetMap(Base):
    __tablename__ = 'module_asset_map'

    id = Column(UUID , primary_key=True)
    module_id = Column(UUID, ForeignKey(LcmSource.id))
    asset_id = Column(UUID, ForeignKey(Asset.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')