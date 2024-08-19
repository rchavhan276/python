from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from ..utils.validators import json_validator, split_str_validator, ip_address_validator, mac_address_validator

class AssetTechRefModel(BaseModel):
    id: UUID
    is_current: bool
    asset_id: UUID
    device_class_id: UUID
    lcm_source_id: UUID
    asset_source_info: Optional[dict] = {}
    technical_datasheet_id: Optional[UUID] = None
    make: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    dimension: Optional[dict] = {}
    weight_with_unit: Optional[dict] = {}
    environmental_specifications: Optional[dict] = {}
    environmental_compliance: Optional[dict] = {}
    is_rackmount: bool
    other_mounting_type: Optional[str] = None
    rack_unit: Optional[int] = None
    rack_tag: Optional[str] = None
    is_inside_enclosure: bool
    enclosure_tag: Optional[str] = None
    is_hazloc_rated: bool
    hazloc_compliance: Optional[dict] = {}
    is_active_device: bool
    power_supply_type: Optional[str] = None
    power_supply_voltage: Optional[int] = None
    psu_redundancy: bool
    psu_redundancy_type: Optional[str] = None
    is_monitored: bool
    connectivity_type: Optional[str] = None
    mgmt_protocol: Optional[str] = None
    mgmt_ip_address: Optional[str] = None
    mgmt_subnet_mask: Optional[str] = None
    mgmt_default_gateway: Optional[str] = None
    mgmt_if_mac_id: Optional[str] = None
    additional_technical_properties: Optional[dict] = {}
    user_tags: Union[None, List[str]]
    created_at: datetime
    updated_at: datetime

class AddAssetTechRefModel(BaseModel):
    is_current: bool = Field(alias="isCurrent")
    asset_id: UUID = Field(alias="assetId")
    device_class_id: UUID = Field(alias="deviceClassId")
    lcm_source_id: UUID = Field(alias="lcmSourceId")
    asset_source_info: Optional[dict] = Field(default={}, alias="assetSourceInfo")
    technical_datasheet_id: Optional[UUID] = Field(default=None, alias="technicalDatasheetId")
    make: str = Field(alias="make")
    model: str = Field(alias="model")
    serial_number: str = Field(alias="serialNumber")
    dimension: Optional[dict] = Field(default={}, alias="dimension")
    weight_with_unit: Optional[dict] = Field(default={}, alias="weightWithUnit")
    environmental_specifications: Optional[dict] = Field(default={}, alias="environmentalSpecifications")
    environmental_compliance: Optional[dict] = Field(default={}, alias="environmentalCompliance")
    is_rackmount: bool = Field(alias="isRackMount")
    other_mounting_type: Optional[str] = Field(default=None, alias="otherMountingType")
    rack_unit: Optional[int] = Field(default=None, alias="rackUnit")
    rack_tag: Optional[str] = Field(default=None, alias="rackTag")
    is_inside_enclosure: bool = Field(alias="isInsideEnclosure")
    enclosure_tag: Optional[str] = Field(default=None, alias="enclosureTag")
    is_hazloc_rated: bool = Field(alias="isHazLocRated")
    hazloc_compliance: Optional[dict] = Field(default={}, alias="hazLocCompliance")
    is_active_device: bool = Field(alias="isActiveDevice")
    power_supply_type: Optional[str] = Field(default=None, alias="powerSupplyType")
    power_supply_voltage: Optional[int] = Field(default=None, alias="powerSupplyVoltage")
    psu_redundancy: bool = Field(alias="psuRedundancy")
    psu_redundancy_type: Optional[str] = Field(default=None, alias="psuRedundancyType")
    is_monitored: bool = Field(alias="isMonitored")
    connectivity_type: Optional[str] = Field(default=None, alias="connectivityType")
    mgmt_protocol: Optional[str] = Field(default=None, alias="mgmtProtocol")
    mgmt_ip_address: Optional[str] = Field(default=None, alias="mgmtIPAddr")
    mgmt_subnet_mask: Optional[str] = Field(default=None, alias="mgmtSubnetMask")
    mgmt_default_gateway: Optional[str] = Field(default=None, alias="mgmtDefaultGateway")
    mgmt_if_mac_id: Optional[str] = Field(default=None, alias="mgmtIFMacAddr")
    additional_technical_properties: Optional[dict] = Field(default={}, alias="additionalTechProperties")
    user_tags: Optional[list[str]] = Field(default=[], alias="userTags")

    _validate_ip_addresses = ip_address_validator("mgmt_ip_address", "mgmt_subnet_mask", "mgmt_default_gateway")
    _validate_mac_address = mac_address_validator("mgmt_if_mac_id")
    _parse_json_properties = json_validator("asset_source_info", "dimension", "weight_with_unit", "environmental_specifications", "environmental_compliance", "hazloc_compliance", "additional_technical_properties")
    _convert_user_tags = split_str_validator("user_tags")
   