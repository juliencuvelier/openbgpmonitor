from openbgpmonitor.config.config import CONFIG, Config
from openbgpmonitor.core.models.event_models import Event, EventType
from openbgpmonitor.core.ports.bgp_interface import BGPInterface
from openbgpmonitor.core.ports.tsdb_interface import TSDBInterface
from time import sleep
from datetime import datetime
from datetime import UTC
from openbgpmonitor.services.logger import get_logger

LOG = get_logger(__name__)


def analyse_change(
    new_prefixes: list, existing_prefixes: list, neighbor_name: str
) -> list[Event]:
    added_prefixes = []
    removed_prefixes = []
    now = datetime.now(UTC)
    for new_prefix in new_prefixes:
        if new_prefix not in existing_prefixes:
            added_prefixes.append(new_prefix)
    for existing_prefix in existing_prefixes:
        if existing_prefix not in new_prefixes:
            removed_prefixes.append(existing_prefix)
    result = []
    if len(added_prefixes) > 0:
        result.append(
            Event(
                timestamp=now,
                details=added_prefixes,
                event_type=EventType.ADDED_PREFIX,
                neighbor_name=neighbor_name,
            )
        )
    if len(removed_prefixes) > 0:
        result.append(
            Event(
                timestamp=now,
                details=removed_prefixes,
                event_type=EventType.REMOVED_PREFIX,
                neighbor_name=neighbor_name,
            )
        )
    if len(result) > 0:
        return result
    else:
        return []


class CoreController:
    config: Config
    bgp_service: BGPInterface
    tsdb_service: TSDBInterface
    prefix_per_neighbor: dict

    def __init__(
        self,
        bgp_service: BGPInterface,
        tsdb_service: TSDBInterface,
        config: Config = CONFIG,
    ):
        self.bgp_service = bgp_service
        self.tsdb_service = tsdb_service
        self.config = config
        self.prefix_per_neighbor = {}
        self.bgp_service.apply_config(config=self.config)

    def run(self):
        while True:
            for bgp_neighbor in self.config.peer_list:
                LOG.debug(f"Fetching prefix from {bgp_neighbor.name}")
                LOG.debug(f"Existing prefixes dict = {self.prefix_per_neighbor}")
                existing_prefixes = self.prefix_per_neighbor.get(bgp_neighbor.name)
                prefixes = self.bgp_service.get_bgp_prefixes_received_from_neighbor(
                    bgp_neighbor
                )
                LOG.debug(
                    f"existing prefixes of neighbor {bgp_neighbor.name} = {existing_prefixes}"
                )
                LOG.debug(
                    f"fetched prefixes of neighbor {bgp_neighbor.name} = {prefixes}"
                )
                if existing_prefixes is not None:
                    events = analyse_change(
                        new_prefixes=prefixes,
                        existing_prefixes=existing_prefixes,
                        neighbor_name=bgp_neighbor.name,
                    )
                    LOG.debug(
                        f"Events generated for neighbor {bgp_neighbor.name} : {events}"
                    )
                    self.tsdb_service.send_event_list(event_list=events)
                else:
                    LOG.debug(
                        f"updating existing prefixes list for key {bgp_neighbor.name} with value {prefixes}"
                    )
                    self.prefix_per_neighbor[bgp_neighbor.name] = prefixes
            sleep(1)
