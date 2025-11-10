from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class EventType(Enum):
    ADDED_PREFIX = "added_prefix"
    REMOVED_PREFIX = "removed_prefix"


class Event(BaseModel):
    timestamp: datetime
    details: list
    event_type: EventType
    neighbor_name: str
    measurement: str = "bgp_events"
