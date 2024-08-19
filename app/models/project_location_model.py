from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .project_model import Project
from .location_model import Location


Base = declarative_base()

class ProjectLocation(Base):
    __tablename__ = 'projects_locations'
    
    id = Column(UUID , primary_key=True)
    project_id = Column(UUID, ForeignKey(Project.id))
    location_id = Column(UUID, ForeignKey(Location.id))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')  