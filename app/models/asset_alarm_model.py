from sqlalchemy import Column, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from .asset_model import Asset


Base = declarative_base()

class AssetAlarm(Base):
    __tablename__ = 'asset_alarms'

    id = Column(UUID , primary_key=True)
    asset_id = Column(UUID, ForeignKey(Asset.id))
    alarm_name = Column(String)
    alarm_scope = Column(JSONB)
    alarm_source_info = Column(JSONB)
    description = Column(String)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')