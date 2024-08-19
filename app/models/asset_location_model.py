from sqlalchemy import Column, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# This is not an actual table; it is a meterialized view.
class AssetLocation(Base):
    __tablename__ = 'asset_location' 
    
    asset_tag = Column(String, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    is_active = Column(Boolean)
