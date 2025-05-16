from typing import Literal, Dict, Any
from pydantic import BaseModel

class NotificationPolicyRoutes(BaseModel):
    warn: Dict[str, Any]
    critical: Dict[str, Any]

class NotificationPolicyRoutes(BaseModel):
    defaults: Dict

class NotificationPolicySpec(BaseModel):
    slug: str
    name: str
    team_slug: str
    routes: NotificationPolicyRoutes

class NotificationPolicy(BaseModel):
    api_version: Literal["v1/config"]
    kind: Literal["NotificationPolicy"]
    spec: NotificationPolicySpec