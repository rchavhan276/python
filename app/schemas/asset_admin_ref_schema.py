from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime, date
from uuid import UUID
from ..utils.validators import split_str_validator


class AssetAdminRefModel(BaseModel):
    id: UUID
    is_current: bool
    asset_id: UUID
    device_class_id: UUID
    asset_owner_id: UUID
    asset_lifecycle_status: str
    client_erp_ref: Optional[str] = None
    client_erp_supplier_ref: Optional[str] = None
    project_spir_ref: Optional[str] = None
    cn_erp_ref: Optional[str] = None
    purchase_date: Optional[date] = None
    client_purchase_order_ref: Optional[str] = None
    cn_purchase_order_ref: Optional[str] = None
    asset_price: Optional[float] = None
    asset_currency: Optional[str] = None
    depreciation_rate: Optional[float] = None
    installation_date: date
    under_lcm_contract: Optional[bool] = None
    lcm_contract_tier: Optional[str] = None
    under_oem_warranty: Optional[bool] = None
    oem_warranty_start_date: Optional[date] = None
    oem_warranty_expiry_date: Optional[date] = None
    oem_service_contract_ref: Optional[str] = None
    oem_service_contract_start_date: Optional[date] = None
    oem_service_contract_expiry_date: Optional[date] = None
    oem_contact_details: Optional[str] = None
    end_of_sale_date: Optional[date] = None
    end_of_support_date: Optional[date] = None
    estimated_asset_life_in_yrs: Optional[int] = None
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime


class AddAssetAdminRefModel(BaseModel):
    is_current: bool = Field(alias="isCurrent")
    asset_id: UUID = Field(alias="assetId")
    device_class_id: UUID = Field(alias="deviceClassId")
    asset_owner_id: UUID = Field(alias="assetOwnerId")
    asset_lifecycle_status: str = Field(alias="assetLifecycleStatus")
    client_erp_ref: Optional[str] = Field(default=None, alias="clientERPRef")
    client_erp_supplier_ref: Optional[str] = Field(default=None, alias="clientERPSupplierRef")
    project_spir_ref: Optional[str] = Field(default=None, alias="projectSPIRRef")
    cn_erp_ref: Optional[str] = Field(default=None, alias="cnERPRef")
    purchase_date: Optional[date] = Field(default=None, alias="purchaseDate")
    client_purchase_order_ref: Optional[str] = Field(default=None, alias="clientPurchaseOrderRef")
    cn_purchase_order_ref: Optional[str] = Field(default=None, alias="cnPurchaseOrderRef")
    asset_price: Optional[float] = Field(default=None, alias="assetPrice")
    asset_currency: Optional[str] = Field(default=None, alias="assetCurrency")
    depreciation_rate: Optional[float] = Field(default=None, alias="depreciationRate")
    installation_date: date = Field(alias="installationDate")
    under_lcm_contract: Optional[bool] = Field(default=None, alias="underLCMContract")
    lcm_contract_tier: Optional[str] = Field(default=None, alias="lcmContractTier")
    under_oem_warranty: Optional[bool] = Field(default=None, alias="underOEMWarranty")
    oem_warranty_start_date: Optional[date] = Field(default=None, alias="oemWarrantyStartDate")
    oem_warranty_expiry_date: Optional[date] = Field(default=None, alias="oemWarrantyExpiryDate")
    oem_service_contract_ref: Optional[str] = Field(default=None, alias="oemServiceContractRef")
    oem_service_contract_start_date: Optional[date] = Field(default=None, alias="oemServiceContractStartDate")
    oem_service_contract_expiry_date: Optional[date] = Field(default=None, alias="oemServiceContractExpiryDate")
    oem_contact_details: Optional[str] = Field(default=None, alias="oemContactDetails")
    end_of_sale_date: Optional[date] = Field(default=None, alias="endOfSaleDate")
    end_of_support_date: Optional[date] = Field(default=None, alias="endOfSupportDate")
    estimated_asset_life_in_yrs: Optional[int] = Field(default=None, alias="estimatedAssetLifeInYrs")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")

    _convert_user_tags = split_str_validator('user_tags')


