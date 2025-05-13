from typing import Literal
from pydantic import BaseModel

class TeamSpec(BaseModel):
    slug: str
    name: str

class Team(BaseModel):
    api_version: Literal["v1/config"]
    kind: Literal["Team"]
    spec: TeamSpec