from sqlalchemy import Column, String, ForeignKey, ARRAY, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .client_model import Client


Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(UUID , primary_key=True)
    client_id = Column(UUID, ForeignKey(Client.id))
    project_code = Column(String)
    project_name = Column(String)
    description = Column(String)
    cn_project_code = Column(String)
    lcm_contract_ref = Column(String)
    lcm_contract_tier = Column(String)
    lcm_contract_startdate = Column(Date)
    lcm_contract_enddate = Column(Date)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')  
    