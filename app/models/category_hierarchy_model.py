from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .category_model import Category


Base = declarative_base()

class CategoryHierarchy(Base):
    __tablename__ = 'category_hierarchy'

    id = Column(UUID , primary_key=True)
    parent_category_id = Column(UUID, ForeignKey(Category.id))
    child_category_id = Column(UUID, ForeignKey(Category.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')