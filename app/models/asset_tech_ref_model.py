from sqlalchemy import Column, String, Boolean, ForeignKey, ARRAY, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, INET, MACADDR, JSONB
from sqlalchemy.ext.declarative import declarative_base
from .asset_model import Asset
from .device_class_model import DeviceClass
from .lcm_source_model import LcmSource


Base = declarative_base()

class AssetTechRef(Base):
    __tablename__ = 'asset_technical_ref'

    id = Column(UUID , primary_key=True)
    is_current = Column(Boolean)
    asset_id = Column(UUID, ForeignKey(Asset.id))
    device_class_id = Column(UUID, ForeignKey(DeviceClass.id))
    lcm_source_id = Column(UUID, ForeignKey(LcmSource.id))
    asset_source_info = Column(JSONB)
    technical_datasheet_id = Column(UUID)
    make = Column(String)
    model = Column(String)
    serial_number = Column(String)
    dimension = Column(JSONB)
    weight_with_unit = Column(JSONB)
    environmental_specifications = Column(JSONB)
    environmental_compliance = Column(JSONB)
    is_rackmount = Column(Boolean)
    other_mounting_type = Column(String)
    rack_unit = Column(Integer)
    rack_tag = Column(String)
    is_inside_enclosure = Column(Boolean)
    enclosure_tag = Column(String)
    is_hazloc_rated = Column(Boolean)
    hazloc_compliance = Column(JSONB)
    is_active_device = Column(Boolean)
    power_supply_type = Column(String)
    power_supply_voltage = Column(Integer)
    psu_redundancy = Column(Boolean)
    psu_redundancy_type = Column(String)
    is_monitored = Column(Boolean)
    connectivity_type = Column(String)
    mgmt_protocol = Column(String)
    mgmt_ip_address = Column(INET)
    mgmt_subnet_mask = Column(INET)
    mgmt_default_gateway = Column(INET)
    mgmt_if_mac_id = Column(MACADDR)
    additional_technical_properties = Column(JSONB)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')