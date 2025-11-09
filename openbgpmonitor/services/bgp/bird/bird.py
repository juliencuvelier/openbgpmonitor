from openbgpmonitor.config.models.config_model import Config
from openbgpmonitor.core.ports.bgp_interface import BGPInterface
from openbgpmonitor.core.models.bgp_models import (
    BGPNeighbor,
    BGPNeighborState,
    BGPPeeringStateEnum,
)
from pybird import PyBird
from openbgpmonitor.config.config import CONFIG
from jinja2 import Environment, FileSystemLoader

# Initialiser l'environnement avec un dossier de templates
env = Environment(
    loader=FileSystemLoader("./openbgpmonitor/services/bgp/bird/templates"),
    autoescape=True,
)


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
            state=BGPPeeringStateEnum(bgp_peer_state.get("state").lower()),
            received_prefix_number=int(bgp_peer_state.get("import_updates_received")),
        )

    def get_bgp_prefixes_received_from_neighbor(self, neighbor):
        return self.bird_socket.get_peer_prefixes_accepted(peer_name=neighbor.name)

    def apply_config(self, config: Config) -> bool | None:
        template = env.get_template("config.j2")
        rendered_config = template.render(
            neighbors=self.neighbors, local_as=config.local_as
        )
        self.bird_socket.config_file = "/etc/bird/bird.conf"
        self.bird_socket.put_config(rendered_config)
        try:
            self.bird_socket.check_config()
            self.bird_socket.commit_config()
            return True
        except ValueError as err:
            print(f"error in generated config: {err}")
