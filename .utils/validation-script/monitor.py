from typing import Literal, List, Optional, Any
from pydantic import BaseModel, root_validator

class SeriesCondition(BaseModel):
    op: Literal["GEQ", "GT", "LEQ", "LT", "EQ", "NEQ", "EXISTS", "NOT_EXISTS"]
    value: Optional[float] = None
    sustain_secs: Optional[int] = None

    @root_validator(pre=True)
    def check_value_required(cls, values):
        op = values.get("op")
        value = values.get("value")
        
        if op in ["GEQ", "GT", "LEQ", "LT", "EQ", "NEQ"] and value is None:
                raise ValueError(f"value must be provided for op '{op}'")
        
        return values

class SeriesConditionList(BaseModel):
    conditions: List[SeriesCondition]

    @root_validator(pre=True)
    def check_non_empty(cls, values):
        if not values.get("conditions"):
            raise ValueError("'conditions' list must not be empty.")
        return values

class SeriesConditionDefaults(BaseModel):
    warn: Optional[SeriesConditionList] = None
    critical: Optional[SeriesConditionList] = None

    @root_validator(pre=True)
    def check_warn_or_critical(cls, values):
        warn = values.get("warn")
        critical = values.get("critical")
        
        if not warn and not critical:
            raise ValueError("At least one of 'warn' or 'critical' must be provided.")
        
        return values

class SeriesConditions(BaseModel):
    defaults: SeriesConditionDefaults

class SignalGrouping(BaseModel):
    label_names: Optional[List[str]] = None
    signal_per_series: Optional[bool] = None

    @root_validator(pre=True)
    def check_signal_grouping(cls, values):
        signal_per_series = values.get('signal_per_series')
        label_names = values.get('label_names')

        if signal_per_series is False and not label_names:
            raise ValueError("label_names must be provided if signal_per_series is False.")

        if signal_per_series is True and label_names:
            raise ValueError("label_names cannot be provided if signal_per_series is True.")
        
        return values

class MonitorSpec(BaseModel):
    slug: str
    name: str
    collection_slug: str
    signal_grouping: Optional[SignalGrouping] = None
    series_conditions: SeriesConditions
    notification_policy_slug: str
    interval_secs: Optional[int] = None
    prometheus_query: str

class Monitor(BaseModel):
    api_version: Literal["v1/config"]
    kind: Literal["Monitor"]
    spec: MonitorSpec