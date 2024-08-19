from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .category_model import Category
from .system_model import System

Base = declarative_base()

class CategorySystem(Base):
    __tablename__ = 'categories_systems'
    
    id = Column(UUID , primary_key=True)
    category_id = Column(UUID, ForeignKey(Category.id))
    system_id = Column(UUID, ForeignKey(System.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')  