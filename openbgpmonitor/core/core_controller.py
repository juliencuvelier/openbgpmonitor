from openbgpmonitor.config.config import CONFIG, Config
from openbgpmonitor.core.ports.bgp_interface import BGPInterface
from time import sleep


class CoreController:
    config: Config
    bgp_service: BGPInterface

    def __init__(self, bgp_service: BGPInterface, config: Config = CONFIG):
        self.bgp_service = bgp_service
        self.config = CONFIG
        self.bgp_service.apply_config(config=self.config)

    def run(self):
        while True:
            for bgp_neighbor in self.config.peer_list:
                self.bgp_service.get_bgp_neighbor_state(bgp_neighbor)
                self.bgp_service.get_bgp_prefixes_received_from_neighbor(bgp_neighbor)
            sleep(1)
