from pydantic import BaseModel
from pydantic import PositiveInt

from openbgpmonitor.core.models.bgp_models import BGPNeighbor


class Config(BaseModel):
    peer_list: list[BGPNeighbor]
    local_as: PositiveInt
    influxdb_url: str
    influxdb_token: str
    influxdb_org: str
    influxdb_bucket: str
    probe_name: str
