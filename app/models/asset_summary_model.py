from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# This is not an actual table; it is a meterialized view combining assets, asset_administrative_ref and asset_technical_ref tables.
class AssetSummary(Base):
    __tablename__ = 'asset_summary_new' # check the view name in the database
    # __tablename__ = 'asset_summary' # for testing
    
    asset_id = Column(UUID, primary_key=True)
    asset_tag = Column(String)
    asset_owner = Column(String)
    email = Column(String)
    client_name = Column(String)
    project_name = Column(String)
    location = Column(String)
    is_active = Column(Boolean)
    asset_lifecycle_status = Column(String)
    installation_date = Column(Date)
    make = Column(String)
    model = Column(String)
    serial_number = Column(String)