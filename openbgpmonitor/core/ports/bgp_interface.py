from abc import ABC

from openbgpmonitor.config.models.config_model import Config
from openbgpmonitor.core.models.bgp_models import BGPNeighbor, BGPNeighborState


class BGPInterface(ABC):
    def get_bgp_neighbor_state(self, neighbor: BGPNeighbor) -> BGPNeighborState:
        raise NotImplementedError

    def get_bgp_prefixes_received_from_neighbor(self, neighbor: BGPNeighbor):
        raise NotImplementedError

    def apply_config(self, config: Config) -> bool:
        raise NotImplementedError
