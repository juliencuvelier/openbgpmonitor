from enum import Enum

from pydantic import BaseModel, IPvAnyAddress
from pydantic import PositiveInt


class BGPNeighbor(BaseModel):
    remote_ip: IPvAnyAddress
    remote_as: PositiveInt
    name: str
    keepalive_timer: int = 60
    hold_timer: int = 180
    password: str | None = None
    vrf: str = "default"
    afi: str = "ipv4-unicast"


class BGPPeeringStateEnum(Enum):
    OPEN = "open"
    ESTABLISHED = "established"
    CONNECT = "connect"
    ACTIVE = "active"
    OPENSENT = "opensent"
    OPENCONFIRM = "openconfirm"


class BGPNeighborState(BaseModel):
    state: BGPPeeringStateEnum
    received_prefix_number: int
