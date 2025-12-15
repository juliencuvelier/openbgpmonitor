from enum import Enum
from ipaddress import IPv4Network

from pydantic import BaseModel, IPvAnyAddress
from pydantic import PositiveInt
from dataclasses import dataclass


class BGPNeighbor(BaseModel):
    """
    Model representing a BGP neighbor.

    Attributes:
        remote_ip (IPvAnyAddress): Remote neighbor IP address.
        remote_as (PositiveInt): Neighbor Autonomous System (AS) number.
        name (str): Neighbor name.
        keepalive_timer (int): Keepalive timer interval in seconds. Default: 60.
        hold_timer (int): Hold timer interval in seconds. Default: 180.
        password (str | None): Authentication password (optional).
        vrf (str): Virtual Routing and Forwarding (VRF) name. Default: "default".
        afi (str): Address Family Identifier. Default: "ipv4-unicast".
    """

    remote_ip: IPvAnyAddress
    remote_as: PositiveInt
    name: str
    keepalive_timer: int = 60
    hold_timer: int = 180
    password: str | None = None
    vrf: str = "default"
    afi: str = "ipv4-unicast"


class BGPPeeringStateEnum(Enum):
    """
    Enumeration representing the different states of a BGP session.

    Attributes:
        OPEN: Session is open.
        ESTABLISHED: Session is established.
        CONNECT: Connection attempt in progress.
        ACTIVE: Session is active but not established.
        OPENSENT: OPEN message sent.
        OPENCONFIRM: OPEN confirmation received.
    """

    OPEN = "open"
    ESTABLISHED = "established"
    CONNECT = "connect"
    ACTIVE = "active"
    OPENSENT = "opensent"
    OPENCONFIRM = "openconfirm"


class BGPNeighborState(BaseModel):
    """
    Model representing the state of a BGP neighbor.

    Attributes:
        state (BGPPeeringStateEnum): Current state of the BGP session.
        received_prefix_number (int): Number of prefixes received from the neighbor.
    """

    state: BGPPeeringStateEnum
    received_prefix_number: int


@dataclass(frozen=True)
class BGPPrefix:
    """
    Class representing a BGP prefix.

    Attributes:
        local_preference (int): Local preference for routing.
        origin (str): Origin of the prefix (e.g., IGP, EGP).
        as_path (str): Autonomous System path to reach the prefix.
        next_hop (str): IP address of the next hop.
        prefix (IPv4Network): Network prefix.
        med (int, optional): Multi-Exit Discriminator.
        weight (int, optional): Weight for routing.
        route_distinguisher (str, optional): Route distinguisher.
        communities (list[str], optional): List of communities associated with the prefix.
        extended_communities (list[str], optional): List of extended communities associated with the prefix.
    """

    local_preference: int
    origin: str
    as_path: str
    next_hop: str
    prefix: IPv4Network
    med: int | None = None
    weight: int | None = None
    route_distinguisher: str | None = None
    communities: list[str] | None = None
    extended_communities: list[str] | None = None
