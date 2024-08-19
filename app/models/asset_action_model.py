from sqlalchemy import Column, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from .asset_model import Asset
from .action_type_model import ActionType


Base = declarative_base()

class AssetAction(Base):
    __tablename__ = 'asset_actions'

    id = Column(UUID , primary_key=True)
    asset_id = Column(UUID, ForeignKey(Asset.id))
    action_type_id = Column(UUID, ForeignKey(ActionType.id))
    action_name = Column(String)
    action_scope = Column(JSONB)
    action_source_info = Column(JSONB)
    description = Column(String)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')