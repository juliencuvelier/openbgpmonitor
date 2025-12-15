from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """Enumeration of possible BGP event types."""

    ADDED_PREFIX = "added_prefix"
    REMOVED_PREFIX = "removed_prefix"


class Event(BaseModel):
    """Model representing a BGP event.

    Attributes:
        timestamp (datetime): Date and time of the event.
        details (list): Event-specific details.
        event_type (EventType): Type of event (added or removed prefix).
        neighbor_name (str): Name of the BGP neighbor involved.
        measurement (str): Type of measurement, default is "bgp_events".
    """

    timestamp: datetime
    details: list
    event_type: EventType
    neighbor_name: str
    measurement: str = "bgp_events"
