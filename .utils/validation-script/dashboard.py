from typing import Literal
from pydantic import BaseModel

class DashboardSpec(BaseModel):
    slug: str
    name: str
    collection_slug: str
    dashboard_json: str

class Dashboard(BaseModel):
    api_version: Literal["v1/config"]
    kind: Literal["Dashboard"]
    spec: DashboardSpec