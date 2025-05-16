from typing import List, Optional
from pydantic import BaseModel, validator

class DataSourceAndDoc(BaseModel):
    title: str
    url: str

class Asset(BaseModel):
    asset_type: str
    name: str
    slug: str
    file: str
    config_required: str
    description: Optional[str] = None
    screenshot: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None

class Manifest(BaseModel):
    tech_type: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    icon: Optional[str] = None
    data_source_and_docs: Optional[List[DataSourceAndDoc]] = None
    asset_list: Optional[List[Asset]] = None

    @validator('asset_list')
    def validate_asset_list(cls, v):
        if v is not None and not v:
            raise ValueError("'asset_list' must not be empty if provided")
        return v

