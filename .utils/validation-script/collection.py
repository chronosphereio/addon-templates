from typing import Literal
from pydantic import BaseModel

class CollectionSpec(BaseModel):
    slug: str
    name: str
    team_slug: str

class Collection(BaseModel):
    api_version: Literal["v1/config"]
    kind: Literal["Collection"]
    spec: CollectionSpec