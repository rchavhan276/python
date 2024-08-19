from sqlalchemy import Column, String, Boolean, ForeignKey, ARRAY, Integer, Date, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from .asset_model import Asset
from .device_class_model import DeviceClass
from .asset_owner_model import AssetOwner


Base = declarative_base()

class AssetAdminRef(Base):
    __tablename__ = 'asset_administrative_ref'

    id = Column(UUID , primary_key=True)
    is_current = Column(Boolean)
    asset_id = Column(UUID, ForeignKey(Asset.id))
    device_class_id = Column(UUID, ForeignKey(DeviceClass.id))
    asset_owner_id = Column(UUID, ForeignKey(AssetOwner.id))
    asset_lifecycle_status = Column(String)
    client_erp_ref = Column(String)
    client_erp_supplier_ref = Column(String)
    project_spir_ref = Column(String)
    cn_erp_ref = Column(String)
    purchase_date = Column(Date)
    client_purchase_order_ref = Column(String)
    cn_purchase_order_ref = Column(String)
    asset_price = Column(Numeric(precision=10, scale=2))
    asset_currency = Column(String, server_default='USD')
    depreciation_rate = Column(Numeric(precision=5, scale=3))
    installation_date = Column(Date)
    under_lcm_contract = Column(Boolean)
    lcm_contract_tier = Column(String)
    under_oem_warranty = Column(Boolean)
    oem_warranty_start_date = Column(Date)
    oem_warranty_expiry_date = Column(Date)
    oem_service_contract_ref = Column(String)
    oem_service_contract_start_date = Column(Date)
    oem_service_contract_expiry_date = Column(Date)
    oem_contact_details = Column(String)
    end_of_sale_date = Column(Date)
    end_of_support_date = Column(Date)
    estimated_asset_life_in_yrs = Column(Integer)
    user_tags = Column(ARRAY(String))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')