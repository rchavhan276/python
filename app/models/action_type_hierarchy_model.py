from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .action_type_model import ActionType


Base = declarative_base()

class ActionTypeHierarchy(Base):
    __tablename__ = 'action_type_hierarchy'

    id = Column(UUID , primary_key=True)
    parent_action_type_id = Column(UUID, ForeignKey(ActionType.id))
    child_action_type_id = Column(UUID, ForeignKey(ActionType.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')