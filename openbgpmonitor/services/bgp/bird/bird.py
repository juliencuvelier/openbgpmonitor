from openbgpmonitor.config.models.config_model import Config
from openbgpmonitor.core.ports.bgp_interface import BGPInterface
from openbgpmonitor.core.models.bgp_models import (
    BGPNeighbor,
    BGPNeighborState,
    BGPPeeringStateEnum,
)
from pybird import PyBird
from openbgpmonitor.config.config import CONFIG
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Initialiser l'environnement avec un dossier de templates
env = Environment(loader=FileSystemLoader("templates"), autoescape=True)


class BGPPybird(BGPInterface):
    bird_socket: PyBird
    neighbors = BGPNeighbor

    def __init__(
        self, bird_socket_path: str = "/var/run/bird/bird.ctl", config: Config = CONFIG
    ):
        self.bird_socket = PyBird(bird_socket_path)
        self.neighbors = config.peer_list

    def get_bgp_neighbor_state(self, neighbor: BGPNeighbor) -> BGPNeighborState:
        bgp_peer_state = self.bird_socket.get_peer_status(peer_name=neighbor.name)
        return BGPNeighborState(
            state=BGPPeeringStateEnum(bgp_peer_state.get("status")),
            received_prefix_number=bgp_peer_state.get("received_prefix_number"),
        )

    def get_bgp_prefixes_received_from_neighbor(self, neighbor):
        return self.bird_socket.get_peer_prefixes_accepted(peer_name=neighbor.name)

    def apply_config(self, config: Config) -> bool:
        current_time = datetime.now()
        template = env.get_template("config.j2")
        rendered_config = template.render(
            neighbors=self.neighbors, local_as=config.local_as
        )
        last_reconfiguration_time: datetime = self.bird_socket.get_bird_status().get(
            "last_reconfiguration"
        )
        self.bird_socket.config_file = "/etc/bird/bird.conf"
        self.bird_socket.put_config(rendered_config)
        try:
            self.bird_socket.check_config()
            self.bird_socket.commit_config()
        except ValueError as err:
            print(f"error in generated config: {err}")
        if last_reconfiguration_time > current_time:
            return True
        raise ValueError("Generated configuration is not correctly applied")
