from pydantic import BaseModel
from typing import Optional, Union

class AssetLocationModel(BaseModel):
    asset_tag: str
    longitude: Optional[Union[float, None]]
    latitude: Optional[Union[float, None]]
    is_active: bool