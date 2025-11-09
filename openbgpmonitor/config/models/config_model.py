from pydantic import BaseModel
from pydantic import PositiveInt

from openbgpmonitor.core.models.bgp_models import BGPNeighbor


class Config(BaseModel):
    peer_list: list[BGPNeighbor]
    local_as: PositiveInt
